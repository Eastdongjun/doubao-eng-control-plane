# Dependency Authorization Protocol

Use this protocol whenever a requested design capability reaches an environment, runtime, browser, package, system library, executable, or permission that is absent. A missing dependency is a decision boundary, not an ordinary tool error.

## 1. Trigger

Trigger `authorization_required` only when all three conditions are true:

1. The dependency is actually missing or inaccessible, based on a read-only check or a captured runtime failure.
2. The dependency blocks a capability needed for the current request or its required proof.
3. Installing, enabling, downloading, authenticating, or changing scope would mutate the user's environment or require new authority.

Do not interrupt work for optional dependencies that were never reached. Do not classify malformed input, a product defect, or an ordinary failed assertion as a dependency problem.

## 2. Required user-facing request

Before installation, tell the user:

- What is missing and how it was detected
- Which requested capability is blocked and why the dependency is needed
- The recommended installation scope and exact command
- Which files, package environments, caches, browsers, or system packages will change
- Network, disk, lifecycle-script, administrator, license, account, secret, or restart implications
- The available fallback and the exact loss of proof or quality
- The verification that will be rerun after installation

Then ask one focused authorization question. Do not install while merely announcing the request. Silence, a prior unrelated installation, or general permission to complete the design is not installation authorization.

## 3. Machine-readable contract

Tools emit JSON with:

- `status: authorization_required`
- `authorization_required: true`
- A stable `authorization_id`
- Dependency id, name, and kind
- Blocked capability and purpose
- Detected environment and sanitized error evidence
- One or more scoped installation options with exact commands and described changes
- Impact, fallback quality loss, and `next_action: ask_user_before_install`
- A ready-to-present `user_prompt`

Use exit code `3` for authorization required, `2` for a completed check that found blocking quality problems, `1` for an unexpected execution failure, and `0` for a completed non-blocking result. Save the authorization JSON to the requested evidence path so an orchestrating Agent can resume deterministically.

Start from [`DEPENDENCY_AUTHORIZATION.example.json`](../templates/DEPENDENCY_AUTHORIZATION.example.json) when another tool needs to implement the contract.

## 4. Agent behavior

When a tool returns `authorization_required`:

1. Stop only the blocked capability; continue independent, non-mutating work when useful.
2. Present the request in plain language, including the recommended scope, command, impact, fallback, and rerun plan.
3. Ask the user for explicit authorization.
4. If authorized, install only the approved dependency in the approved scope, verify that it resolves, rerun the blocked capability, and attach the new evidence.
5. If declined or deferred, use a fallback only when the user accepts its stated limits. Mark the affected gate `unproven`; never translate a manual source review into automated or browser-geometry proof.
6. If the proposed install reveals another dependency or broader privilege, issue a new authorization request. Do not expand the original approval silently.

For external accounts, API keys, licensed fonts, private assets, browser login state, or platform permissions, replace the install command with the precise enablement action the user must take. Never request secrets in a public artifact or write them into the skill.

## 5. Scope rules

Prefer the narrowest reversible scope that can satisfy the proof:

1. Existing project environment
2. Skill-local or project-local package directory
3. Current-user environment or cache
4. System-wide installation only when necessary

Do not choose a system-wide install for convenience. Do not modify lockfiles, manifests, shared runtimes, browser profiles, or global package stores unless that exact change is disclosed and authorized.

## 6. Prohibited behavior

- Barely reporting “dependency missing” and ending the task
- Automatically installing because the package is common or free
- Hiding a missing pixel/browser/runtime dependency behind a silent fallback
- Recommending a command without its target scope and side effects
- Claiming a gate passed because source code appears correct
- Treating one approval as permission for later unrelated dependencies
- Repeating the request after the user declines unless the required scope or evidence has materially changed

The purpose of this protocol is informed continuation: the user can authorize a precise fix, consciously accept reduced evidence, or change the requested proof without losing traceability.
