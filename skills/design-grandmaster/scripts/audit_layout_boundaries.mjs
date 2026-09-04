#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const SKILL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const DEFAULT_VIEWPORTS = "1440x1000,900x900,390x844,320x700";
const DEFAULT_ZONES = [
    "[data-boundary-zone]",
    "main > header",
    "main > section",
    "main > footer",
    "body > header",
    "body > footer",
    "nav",
    "aside",
    "[role='dialog']",
    "[role='navigation']",
].join(",");
const DEFAULT_IGNORE = ".svg-sprite,.skip-link,[hidden],[data-edge-audit-ignore]";

function printHelp() {
    process.stdout.write(`Layout boundary and safe-area audit

Usage:
  node scripts/audit_layout_boundaries.mjs --target <file-or-url> [options]

Options:
  --viewports <list>  Comma-separated WIDTHxHEIGHT values
                      Default: ${DEFAULT_VIEWPORTS}
  --zones <selector>  CSS selector for responsible audit zones
  --min-inset <px>    Fallback safe inset when no zone override exists
                      Default: 16
  --ignore <selector> CSS selector for approved exclusions
  --browser <path>    Chrome or Chromium executable path
  --wait <ms>         Stabilization delay after load/state changes
                      Default: 500
  --output <path>     Write JSON report to a file as well as stdout
  --help              Show this help

Zone overrides:
  data-safe-inset="20"
  --audit-safe-inset: 20px;
`);
}

function parseArguments(argv) {
    const options = {
        target: "",
        viewports: DEFAULT_VIEWPORTS,
        zones: DEFAULT_ZONES,
        minInset: 16,
        ignore: DEFAULT_IGNORE,
        browser: process.env.CHROME_PATH || "",
        wait: 500,
        output: "",
    };

    for (let index = 0; index < argv.length; index += 1) {
        const argument = argv[index];
        if (argument === "--help") {
            printHelp();
            process.exit(0);
        }

        const value = argv[index + 1];
        if (!value || value.startsWith("--")) {
            throw new Error(`Missing value for ${argument}`);
        }

        switch (argument) {
            case "--target":
                options.target = value;
                break;
            case "--viewports":
                options.viewports = value;
                break;
            case "--zones":
                options.zones = value;
                break;
            case "--min-inset":
                options.minInset = Number(value);
                break;
            case "--ignore":
                options.ignore = value;
                break;
            case "--browser":
                options.browser = value;
                break;
            case "--wait":
                options.wait = Number(value);
                break;
            case "--output":
                options.output = value;
                break;
            default:
                throw new Error(`Unknown option: ${argument}`);
        }
        index += 1;
    }

    if (!options.target) {
        throw new Error("--target is required");
    }
    if (!Number.isFinite(options.minInset) || options.minInset < 0) {
        throw new Error("--min-inset must be a non-negative number");
    }
    if (!Number.isFinite(options.wait) || options.wait < 0) {
        throw new Error("--wait must be a non-negative number");
    }

    options.viewports = options.viewports.split(",").map((entry) => {
        const match = entry.trim().match(/^(\d+)x(\d+)$/i);
        if (!match) {
            throw new Error(`Invalid viewport: ${entry}`);
        }
        return { width: Number(match[1]), height: Number(match[2]) };
    });

    return options;
}

function resolveTarget(target) {
    if (/^(https?|file):\/\//i.test(target)) {
        return target;
    }
    const resolved = path.resolve(target);
    if (!fs.existsSync(resolved)) {
        throw new Error(`Target does not exist: ${resolved}`);
    }
    return pathToFileURL(resolved).href;
}

function detectBrowser(explicitPath) {
    const candidates = [
        explicitPath,
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ].filter(Boolean);
    return candidates.find((candidate) => fs.existsSync(candidate)) || "";
}

function dependencyAuthorization({ id, name, kind, capability, purpose, command, target, scope, changes, impact, fallback, error }) {
    return {
        schema_version: "2.0",
        status: "authorization_required",
        authorization_required: true,
        authorization_id: `install:${kind}:${id}`,
        dependency: { id, name, kind },
        blocked_capability: capability,
        purpose,
        environment: { os: process.platform, architecture: process.arch },
        installation_options: [{
            scope,
            target,
            command,
            changes,
            recommended: true,
        }],
        impact,
        fallback: {
            available: true,
            quality_loss: fallback,
            requires_user_choice: true,
        },
        next_action: "ask_user_before_install",
        user_prompt: `缺少 ${name}，因此无法完成“${capability}”。是否授权我按上述范围安装依赖并在安装后重新执行验证？`,
        rules: [
            "Do not install before explicit user authorization.",
            "Do not report the blocked capability as passed.",
            "Use the fallback only after the user declines or defers installation.",
        ],
        detected_error: String(error?.message || error || "").slice(0, 2000),
    };
}

function emitAuthorization(payload, outputPath) {
    const rendered = `${JSON.stringify(payload, null, 2)}\n`;
    if (outputPath) {
        const resolved = path.resolve(outputPath);
        fs.mkdirSync(path.dirname(resolved), { recursive: true });
        fs.writeFileSync(resolved, rendered, "utf8");
    }
    process.stdout.write(rendered);
    process.exitCode = 3;
}

function summarize(violations) {
    const bySeverity = {};
    const byType = {};
    for (const violation of violations) {
        bySeverity[violation.severity] = (bySeverity[violation.severity] || 0) + 1;
        byType[violation.type] = (byType[violation.type] || 0) + 1;
    }
    return { total: violations.length, bySeverity, byType };
}

async function settle(page, wait) {
    await page.evaluate(async () => {
        if (!document.fonts?.ready) {
            return;
        }
        await Promise.race([
            document.fonts.ready,
            new Promise((resolve) => window.setTimeout(resolve, 3000)),
        ]);
    });
    await page.waitForTimeout(wait);
}

async function collectGeometry(page, state, config) {
    return page.evaluate(({ stateName, zoneSelector, ignoreSelector, fallbackInset }) => {
        const tolerance = 1;
        const clippingValues = new Set(["auto", "scroll", "hidden", "clip"]);
        const violations = [];
        const measured = [];

        function round(value) {
            return Math.round(value * 10) / 10;
        }

        function rectObject(rect) {
            return {
                left: rect.left,
                right: rect.right,
                top: rect.top,
                bottom: rect.bottom,
                width: rect.width,
                height: rect.height,
            };
        }

        function intersect(first, second, clipX = true, clipY = true) {
            const result = { ...first };
            if (clipX) {
                result.left = Math.max(first.left, second.left);
                result.right = Math.min(first.right, second.right);
            }
            if (clipY) {
                result.top = Math.max(first.top, second.top);
                result.bottom = Math.min(first.bottom, second.bottom);
            }
            result.width = Math.max(0, result.right - result.left);
            result.height = Math.max(0, result.bottom - result.top);
            return result;
        }

        function clippedGeometry(element, sourceRect) {
            let visible = { ...sourceRect };
            const ancestors = [];
            let ancestor = element.parentElement;

            while (ancestor && ancestor !== document.documentElement) {
                const style = getComputedStyle(ancestor);
                const clipX = clippingValues.has(style.overflowX);
                const clipY = clippingValues.has(style.overflowY);
                if (clipX || clipY) {
                    const ancestorRect = rectObject(ancestor.getBoundingClientRect());
                    visible = intersect(visible, ancestorRect, clipX, clipY);
                    ancestors.push({
                        selector: describeElement(ancestor),
                        overflowX: style.overflowX,
                        overflowY: style.overflowY,
                    });
                }
                ancestor = ancestor.parentElement;
            }

            return { visible, ancestors };
        }

        function describeElement(element) {
            const id = element.id ? `#${element.id}` : "";
            const classes = typeof element.className === "string" && element.className.trim()
                ? `.${element.className.trim().split(/\s+/).slice(0, 3).join(".")}`
                : "";
            return `${element.tagName.toLowerCase()}${id}${classes}`;
        }

        function isIgnored(element) {
            return Boolean(ignoreSelector && element.closest(ignoreSelector));
        }

        function isRendered(element) {
            const style = getComputedStyle(element);
            return style.display !== "none"
                && style.visibility !== "hidden"
                && Number(style.opacity) > 0;
        }

        function resolveZone(element) {
            let zone = zoneSelector ? element.closest(zoneSelector) : null;
            if (zone === element) {
                zone = element.parentElement?.closest(zoneSelector) || zone;
            }
            return zone;
        }

        function resolveInset(zone) {
            if (!zone) {
                return fallbackInset;
            }
            const attributeValue = Number(zone.dataset.safeInset);
            if (Number.isFinite(attributeValue) && attributeValue >= 0) {
                return attributeValue;
            }
            const customValue = parseFloat(getComputedStyle(zone).getPropertyValue("--audit-safe-inset"));
            return Number.isFinite(customValue) && customValue >= 0 ? customValue : fallbackInset;
        }

        function pushViolation(violation) {
            violations.push({ state: stateName, ...violation });
        }

        function inspectRect(element, sourceRect, object, kind) {
            const { visible, ancestors } = clippedGeometry(element, sourceRect);
            if (visible.width <= tolerance || visible.height <= tolerance) {
                return;
            }

            const viewportVisibleLeft = Math.max(visible.left, 0);
            const viewportVisibleRight = Math.min(visible.right, window.innerWidth);
            if (viewportVisibleRight - viewportVisibleLeft <= tolerance) {
                return;
            }

            const partialByAncestor = visible.width < sourceRect.width - tolerance
                || visible.height < sourceRect.height - tolerance;
            const partialByViewport = viewportVisibleLeft > visible.left + tolerance
                || viewportVisibleRight < visible.right - tolerance;
            const zone = resolveZone(element);
            const zoneRect = zone ? rectObject(zone.getBoundingClientRect()) : null;
            const inset = resolveInset(zone);
            const gaps = zoneRect ? {
                left: round(sourceRect.left - zoneRect.left),
                right: round(zoneRect.right - sourceRect.right),
                top: round(sourceRect.top - zoneRect.top),
                bottom: round(zoneRect.bottom - sourceRect.bottom),
            } : null;
            const viewportGaps = {
                left: round(sourceRect.left),
                right: round(window.innerWidth - sourceRect.right),
            };

            measured.push({
                kind,
                object,
                zone: zone ? describeElement(zone) : null,
                inset,
                gaps,
                viewportGaps,
            });

            if (partialByAncestor || partialByViewport) {
                pushViolation({
                    severity: "high",
                    type: "partial-clipping",
                    kind,
                    object,
                    zone: zone ? describeElement(zone) : null,
                    clippingAncestors: ancestors,
                    source: {
                        width: round(sourceRect.width),
                        height: round(sourceRect.height),
                    },
                    visible: {
                        width: round(Math.max(0, viewportVisibleRight - viewportVisibleLeft)),
                        height: round(visible.height),
                    },
                });
            }

            if (zoneRect && Math.min(gaps.left, gaps.right, gaps.top, gaps.bottom) < inset - tolerance) {
                pushViolation({
                    severity: "medium",
                    type: "safe-inset",
                    kind,
                    object,
                    zone: describeElement(zone),
                    expectedInset: inset,
                    gaps,
                });
            }

            if (Math.min(viewportGaps.left, viewportGaps.right) < -tolerance) {
                pushViolation({
                    severity: "high",
                    type: "viewport-clipping",
                    kind,
                    object,
                    viewportGaps,
                });
            }
        }

        const documentWidth = Math.max(document.body.scrollWidth, document.documentElement.scrollWidth);
        const overflow = round(documentWidth - window.innerWidth);
        if (overflow > tolerance) {
            pushViolation({
                severity: "blocker",
                type: "document-horizontal-overflow",
                expectedWidth: window.innerWidth,
                measuredWidth: documentWidth,
                overflow,
            });
        }

        const textWalker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
            acceptNode(node) {
                const element = node.parentElement;
                if (!node.textContent.trim() || !element || isIgnored(element) || !isRendered(element)) {
                    return NodeFilter.FILTER_REJECT;
                }
                if (["SCRIPT", "STYLE", "NOSCRIPT", "TEMPLATE"].includes(element.tagName)) {
                    return NodeFilter.FILTER_REJECT;
                }
                return NodeFilter.FILTER_ACCEPT;
            },
        });

        while (textWalker.nextNode()) {
            const node = textWalker.currentNode;
            const element = node.parentElement;
            const range = document.createRange();
            range.selectNodeContents(node);
            const text = node.textContent.trim().replace(/\s+/g, " ").slice(0, 80);
            for (const rectangle of range.getClientRects()) {
                if (rectangle.width <= tolerance || rectangle.height <= tolerance) {
                    continue;
                }
                inspectRect(element, rectObject(rectangle), text, "text");
            }
        }

        const visualSelector = "img,svg:not(.svg-sprite),canvas,video,[data-boundary-content]";
        for (const element of document.querySelectorAll(visualSelector)) {
            if (isIgnored(element) || !isRendered(element)) {
                continue;
            }
            const isPresentation = element.matches("[role='presentation'],img[alt='']");
            const isInteractiveVisual = Boolean(element.closest("a[href],button,[role='button'],[role='link']"));
            if (isPresentation || (element.getAttribute("aria-hidden") === "true" && !isInteractiveVisual)) {
                continue;
            }
            const rectangle = element.getBoundingClientRect();
            if (rectangle.width <= tolerance || rectangle.height <= tolerance) {
                continue;
            }
            inspectRect(element, rectObject(rectangle), describeElement(element), "visual");
        }

        const unique = [];
        const seen = new Set();
        for (const violation of violations) {
            const key = JSON.stringify([
                violation.state,
                violation.type,
                violation.kind,
                violation.object,
                violation.zone,
                violation.gaps,
            ]);
            if (!seen.has(key)) {
                seen.add(key);
                unique.push(violation);
            }
        }

        return {
            state: stateName,
            viewport: { width: window.innerWidth, height: window.innerHeight },
            scroll: {
                x: round(window.scrollX),
                y: round(window.scrollY),
                maximumY: round(document.documentElement.scrollHeight - window.innerHeight),
            },
            documentWidth,
            zoneCount: zoneSelector ? document.querySelectorAll(zoneSelector).length : 0,
            measuredCount: measured.length,
            violations: unique,
        };
    }, {
        stateName: state,
        zoneSelector: config.zones,
        ignoreSelector: config.ignore,
        fallbackInset: config.minInset,
    });
}

async function moveHorizontalScrollersToEnd(page) {
    return page.evaluate(() => {
        let changed = 0;
        for (const element of document.querySelectorAll("*")) {
            const style = getComputedStyle(element);
            const scrollable = ["auto", "scroll"].includes(style.overflowX)
                && element.scrollWidth > element.clientWidth + 1;
            if (scrollable) {
                element.scrollLeft = element.scrollWidth - element.clientWidth;
                changed += 1;
            }
        }
        return changed;
    });
}

async function main() {
    const options = parseArguments(process.argv.slice(2));
    const target = resolveTarget(options.target);
    let playwright;
    try {
        playwright = require("playwright");
    } catch (error) { // Recovery policy: missing package becomes an authorization request because installation mutates the environment.
        emitAuthorization(dependencyAuthorization({
            id: "playwright",
            name: "Playwright for Node.js",
            kind: "node-package",
            capability: "Automated responsive boundary geometry audit",
            purpose: "Open the artifact in a real browser and measure responsive safe areas, clipping, overflow, and scroll endpoints.",
            target: SKILL_ROOT,
            scope: "skill-local",
            command: `npm install --prefix "${SKILL_ROOT}" --no-save --no-package-lock playwright`,
            changes: "Creates a skill-local node_modules directory without changing package manifests.",
            impact: [
                "Requires a network download from the configured npm registry.",
                "Creates a local node_modules directory and consumes disk space.",
                "The package may execute npm lifecycle scripts during installation.",
            ],
            fallback: "Manual screenshots and inspection cannot prove computed geometry with the same repeatability.",
            error,
        }), options.output);
        return;
    }

    const executablePath = detectBrowser(options.browser);
    let browser;
    try {
        browser = await playwright.chromium.launch({
            headless: true,
            ...(executablePath ? { executablePath } : {}),
        });
    } catch (error) { // Recovery policy: dependency failures request authorization because browser installation changes local state.
        const message = String(error?.message || error).toLowerCase();
        if (
            message.includes("executable doesn't exist")
            || message.includes("executable does not exist")
            || message.includes("playwright install")
        ) {
            emitAuthorization(dependencyAuthorization({
                id: "playwright-chromium",
                name: "Playwright Chromium browser",
                kind: "browser-runtime",
                capability: "Automated responsive boundary geometry audit",
                purpose: "Provide a compatible headless browser when no usable installed Chrome, Edge, or Chromium executable is available.",
                target: SKILL_ROOT,
                scope: "current-user-cache",
                command: `npx --prefix "${SKILL_ROOT}" playwright install chromium`,
                changes: "Downloads a compatible Chromium build into the user browser cache.",
                impact: [
                    "Requires a substantial network download and additional disk space.",
                    "Linux hosts may require separately authorized system libraries.",
                ],
                fallback: "Automated geometry remains unproven; only an explicitly accepted manual review is possible.",
                error,
            }), options.output);
            return;
        }
        if (message.includes("host system is missing dependencies")) {
            emitAuthorization(dependencyAuthorization({
                id: "playwright-system-libraries",
                name: "Playwright browser system libraries",
                kind: "system-package",
                capability: "Automated responsive boundary geometry audit",
                purpose: "Provide the operating-system libraries required to launch the headless browser.",
                target: SKILL_ROOT,
                scope: "system",
                command: `npx --prefix "${SKILL_ROOT}" playwright install-deps chromium`,
                changes: "Installs operating-system libraries required by the browser runtime.",
                impact: [
                    "Changes system packages and normally requires administrator privileges.",
                    "Requires a network download from the operating-system package repositories.",
                ],
                fallback: "Automated geometry remains unproven; only an explicitly accepted manual review is possible.",
                error,
            }), options.output);
            return;
        }
        throw error;
    }
    const report = {
        schema_version: "2.0",
        target,
        generatedAt: new Date().toISOString(),
        configuration: {
            viewports: options.viewports,
            zones: options.zones,
            minInset: options.minInset,
            ignore: options.ignore,
            wait: options.wait,
        },
        runs: [],
        runtimeErrors: [],
    };

    try {
        for (const viewport of options.viewports) {
            const context = await browser.newContext({ viewport, reducedMotion: "reduce" });
            const page = await context.newPage();
            const errors = [];
            page.on("console", (message) => {
                if (message.type() === "error") {
                    errors.push(`console: ${message.text()}`);
                }
            });
            page.on("pageerror", (error) => errors.push(`pageerror: ${error.message}`));

            await page.goto(target, { waitUntil: "domcontentloaded", timeout: 30000 });
            await settle(page, options.wait);
            report.runs.push(await collectGeometry(page, "initial", options));

            await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
            await settle(page, options.wait);
            await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
            await page.waitForTimeout(options.wait);
            const pageEnd = await collectGeometry(page, "page-end", options);
            const pageEndDrift = Math.abs(pageEnd.scroll.maximumY - pageEnd.scroll.y);
            if (pageEnd.scroll.maximumY > 0 && pageEndDrift > 2) {
                pageEnd.violations.push({
                    state: "page-end",
                    severity: "high",
                    type: "scroll-axis-drift",
                    expectedY: pageEnd.scroll.maximumY,
                    measuredY: pageEnd.scroll.y,
                    drift: Math.round(pageEndDrift * 10) / 10,
                });
            }
            report.runs.push(pageEnd);

            const pageYBeforeHorizontalAudit = await page.evaluate(() => window.scrollY);
            const horizontalScrollerCount = await moveHorizontalScrollersToEnd(page);
            if (horizontalScrollerCount > 0) {
                await settle(page, options.wait);
                const horizontalEnd = await collectGeometry(page, "horizontal-end", options);
                horizontalEnd.horizontalScrollerCount = horizontalScrollerCount;
                const horizontalAxisDrift = Math.abs(horizontalEnd.scroll.y - pageYBeforeHorizontalAudit);
                if (horizontalAxisDrift > 2) {
                    horizontalEnd.violations.push({
                        state: "horizontal-end",
                        severity: "high",
                        type: "scroll-axis-drift",
                        expectedY: Math.round(pageYBeforeHorizontalAudit * 10) / 10,
                        measuredY: horizontalEnd.scroll.y,
                        drift: Math.round(horizontalAxisDrift * 10) / 10,
                    });
                }
                report.runs.push(horizontalEnd);
            }

            if (errors.length) {
                report.runtimeErrors.push({ viewport, errors });
            }
            await context.close();
        }
    } finally {
        await browser.close();
    }

    const violations = report.runs.flatMap((run) => run.violations.map((violation) => ({
        viewport: run.viewport,
        ...violation,
    })));
    report.summary = summarize(violations);
    report.verdict = violations.length === 0 && report.runtimeErrors.length === 0
        ? "Ready"
        : "Not ready";

    const output = `${JSON.stringify(report, null, 2)}\n`;
    if (options.output) {
        fs.writeFileSync(path.resolve(options.output), output, "utf8");
    }
    process.stdout.write(output);
    process.exitCode = report.verdict === "Ready" ? 0 : 2;
}

main().catch((error) => { // Recovery policy: unexpected failures remain fatal because only known dependency gaps are recoverable.
    process.stderr.write(`${error.stack || error.message}\n`);
    process.exitCode = 1;
});
