---
name: 高级安全
description: "资深安全工程：威胁建模、防护、审计。当用户要求安全架构/评审时使用。"
---

# Senior Security Engineer — Threat Modeling + Security Router

This skill does exactly one job itself — **STRIDE/DREAD threat modeling** (plus a quick secret scan) — and routes every other security request to the specialist skill that owns that lane. Do not duplicate sibling content here; route instead.

## Routing Table (read this first)

| The user wants... | Route to | Why that skill owns it |
|---|---|---|
| Vulnerability assessment, pen-test methodology, OWASP Top 10 testing | `../渗透测试/` | Ships `vulnerability_scanner.py` + `dependency_auditor.py` with exit-code contracts |
| Incident triage, SEV classification, forensics, containment | `../事故响应/` | SEV1–SEV4 taxonomy, NIST SP 800-61 phases, `incident_triage.py` |
| Production outage command (non-security incidents) | `../事故指挥官/` | Severity classifier + timeline + postmortem tools |
| Security monitoring, CVE triage SLAs, compliance checks (SOC 2 etc.), security headers | `../高级安全运营/` | `security_scanner.py` + `compliance_checker.py`, CVE SLA table |
| Hostile/adversarial code review | `../对抗审查/` | 3-persona review with BLOCK/CONCERNS/CLEAN verdict |
| Secure code review as part of general review | `../代码审查/` | Language dispatch + regression fixtures |
| Cloud IAM escalation paths, S3 exposure, security groups | `../云安全/` | `cloud_posture_check.py` with per-check exit codes |
| Threat hunting, IOC sweeps, anomaly detection | `../威胁检测/` | z-score anomaly + IOC staleness tooling |
| Red-team engagement planning, ATT&CK kill chains | `../红队/` | `engagement_planner.py` with authorization gate |
| LLM/AI attack surface (prompt injection, poisoning) | `../AI安全/` | ATLAS-mapped `ai_threat_scanner.py` |

If the request spans lanes (e.g., "secure this new architecture"), do the threat model here first — its output (prioritized threats + mitigations) tells you which siblings to load next. Never bulk-load multiple security skills speculatively.

## What This Skill Owns: STRIDE Threat Modeling

### Workflow

1. **Scope:** assets to protect, trust boundaries, data flows (external entities, processes, data stores, flows).
2. **Generate the threat model** per component:
   ```bash
   python3 scripts/threat_modeler.py --component "User Authentication" --assets "credentials,sessions" --json --output threats.json
   ```
   Output: per-threat STRIDE category, DREAD score (Damage, Reproducibility, Exploitability, Affected users, Discoverability — each 1–10), and suggested mitigations. Repeat per DFD element; `--interactive` walks scoping questions; `--list-threats` shows the threat database.
3. **Consume the output:** sort `threats.json` by DREAD score descending; everything ≥ 7 average needs a named mitigation owner before the design ships. Map each mitigation to the responsible sibling lane (e.g., IAM threats → `cloud-security`, injection threats → `code-reviewer`).
4. **Quick secret sweep** while you have the codebase open:
   ```bash
   python3 scripts/secret_scanner.py /path/to/project --format json --severity high
   ```
   20+ patterns (AWS keys, GitHub tokens, private keys, generic credentials). Any critical/high finding blocks merge until rotated and moved to a secret manager.
5. **Verification gate:** every DFD element has ≥ 1 STRIDE row considered, every threat with DREAD ≥ 7 has an owner + mitigation, and the secret scan exits with zero high/critical findings. Re-run both tools after mitigations land — that re-run is the done signal, not the document.

### STRIDE per Element Matrix

| DFD Element | S | T | R | I | D | E |
|-------------|---|---|---|---|---|---|
| External Entity | X | | X | | | |
| Process | X | X | X | X | X | X |
| Data Store | | X | X | X | X | |
| Data Flow | | X | | X | X | |

(S=Spoofing→authn, T=Tampering→integrity, R=Repudiation→audit logs, I=Info Disclosure→encryption/access control, D=DoS→rate limiting/redundancy, E=Elevation→least privilege.)

## References (load on demand)

| Document | Content |
|----------|---------|
| [references/threat-modeling-guide.md](references/threat-modeling-guide.md) | STRIDE methodology, attack trees, DREAD scoring, DFD creation |
| [references/security-architecture-patterns.md](references/security-architecture-patterns.md) | Zero Trust, defense-in-depth, authentication patterns, API security |
| [references/cryptography-implementation.md](references/cryptography-implementation.md) | AES-GCM, Ed25519, password hashing (Argon2id), key management |

The architecture and crypto references are kept because no sibling ships them; for *operating* those controls (scanning, compliance, monitoring) still route to `senior-secops`.
