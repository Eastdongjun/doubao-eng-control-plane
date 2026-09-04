# Design System Conformance and Token Governance

Use this module whenever a project already has an approved design specification, brand system, Design Token set, Figma library, coded component library, or established product patterns. The goal is compatible extension without silent drift.

## Contents

1. Conformance contract
2. Authority and source of truth
3. Baseline classification
4. Design Token immutability
5. Reuse and extension ladder
6. Exception and authorization protocol
7. Token audit
8. Lifecycle checkpoints
9. Output artifacts
10. Quality gates

## 1. Conformance contract

Before designing or coding, record:

- Governing specification names, locations, owners, versions, and effective dates
- Approved Figma libraries, variables/styles, token packages, component packages, and documentation
- Target platforms, themes/modes, brands, densities, breakpoints, and localization variants
- Whether shipped code or documentation is authoritative for behavior and for values
- Locked rules, permitted choices, extensible areas, deprecated items, and known gaps
- Who may approve a local exception, component extension, new shared token, or breaking change
- How decisions and deviations persist across tasks and sessions

If the baseline is unavailable, stale, or contradictory, stop claiming strict conformance. Record the gap, use the least-destructive interpretation, and request a decision when the difference affects the result materially.

## 2. Authority and source of truth

Use the user's declared priority. If none is declared, propose this order and confirm it when stakes are material:

1. User-approved design specification and decision record
2. Released token package and approved variable/style library
3. Released component contract and documentation
4. Shipped code for actual behavior
5. Approved product-specific patterns
6. Local project artifacts
7. Designer judgment and external references

Do not let a popular external design system, trend, generated component, framework default, or personal preference override an approved user system.

Treat code as evidence of actual behavior, not automatic authority to redefine token intent. When code and approved tokens disagree, classify it as drift until an owner decides otherwise.

Maintain this traceability chain:

`specification -> token -> component -> pattern -> screen/flow -> implementation -> QA evidence`

## 3. Baseline classification

Classify every relevant rule or asset:

- **Locked:** must be used as published; change requires explicit authorization
- **Selectable:** choose among approved values, modes, variants, and compositions
- **Extensible:** may be extended inside documented naming, inheritance, and review rules
- **Local-only:** approved for one product or context; must not silently become global
- **Ambiguous/conflicting:** requires interpretation or owner decision
- **Deprecated:** allowed only under the published migration policy
- **Missing:** no rule exists; solve locally first unless shared reuse justifies governance cost

“Existing but inconvenient” is not the same as missing.

## 4. Design Token immutability

### Default lock

Treat shared primitive, semantic, brand, mode, and global tokens as read-only unless the user explicitly authorizes a scoped change. Without authorization, do not:

- Change a value, name, alias, role, description, scale, unit, or mode
- Replace semantic references with raw values
- Create a duplicate token with a slightly different value or spelling
- Insert an arbitrary value between scale steps
- Reinterpret a token for a different semantic purpose
- Change component defaults by mutating a shared token
- Copy tokens into a local file and allow them to drift

Selection is not modification. Using `space.4` instead of `space.3` is a design choice; changing what `space.4` means is a system change.

### Token membership beats arithmetic

If a spacing system uses a 4-unit foundation, `4n` is only a preliminary pattern. The approved token set is the authority.

- `15`, `21`, and `23` fail because they are outside the 4-unit rhythm and are not approved tokens.
- `20` may still fail if the approved system intentionally exposes only `4`, `8`, `12`, `16`, `24`, and `32`.
- `24` may be valid numerically but still wrong semantically if the component requires `space.control.gap` mapped to `16`.

Validate both **membership** and **semantic role**.

Apply the same discipline to:

- Spacing and dimensions
- Typography size, weight, leading, tracking, and measure
- Color, opacity, and gradient stops
- Radius, border, and stroke
- Shadow, elevation, blur, and material
- Motion duration, easing, delay, and spring behavior
- Breakpoints, container widths, and density
- Z-index/layer roles
- Icon size and illustration scale

### Raw-value rule

In token-governed properties, raw values are prohibited unless they are:

1. An approved documented exception
2. A platform or environment value such as safe-area insets
3. A calculated or content-derived value whose endpoints and constraints are tokenized
4. An intrinsic asset measurement or technical hairline explicitly allowed by the system
5. Temporary diagnostic output that cannot ship

Record even valid technical exceptions so they are not copied as precedent.

## 5. Reuse and extension ladder

Use this order:

1. **Reuse:** use the approved component and token combination unchanged
2. **Compose:** combine approved components and patterns
3. **Configure:** use documented properties, variants, slots, modes, and responsive behavior
4. **Permitted local variant:** add a scoped variant only if the system explicitly allows it
5. **Local pattern:** solve a product-specific need without changing the shared system
6. **Proposed shared extension:** submit evidence, contract, states, accessibility, token mapping, ownership, and adoption case
7. **Authorized shared change:** modify the system only after explicit approval and migration planning

Do not jump from a difficult screen directly to a new global token or component.

When a direction cannot work without many exceptions, reject the direction before weakening the system.

## 6. Exception and authorization protocol

Never infer authorization from phrases such as “make it better,” “polish it,” “make it more premium,” or “use your judgment.” Authorization must identify the scope.

Classify approvals:

- **One-instance exception:** one screen or artifact
- **Product-local token/variant:** one product or bounded domain
- **New shared token/component:** reusable system addition
- **Shared token change:** value, role, scale, mode, or naming change
- **Breaking system change:** requires versioning, migration, release notes, and adoption plan

Record:

- Request and reason
- Existing approved options considered
- User/business/accessibility impact
- Exact token/component/value affected
- Scope and surfaces
- Approver and approval date
- Expiry or review date
- Migration and rollback plan
- Whether the exception may be reused

If a locked rule conflicts with accessibility, platform behavior, legal requirements, or functional correctness, do not violate it silently and do not obey it blindly. Identify the conflict and seek the smallest approved correction.

## 7. Token audit

Audit both design artifacts and implementation.

### Inventory

Extract or inspect:

- Figma variables, styles, component properties, detached instances, and local overrides
- CSS custom properties, theme objects, token packages, utility configuration, and literal values
- Native-platform resources and theme definitions
- Component-level defaults and variant-specific values
- Responsive and mode-specific substitutions

### Classify every consequential value

| Status | Meaning | Action |
|---|---|---|
| Exact approved token | correct token and semantic role | keep |
| Approved token, wrong role | value matches but intent is wrong | remap |
| Near-token raw value | visually close but not approved | replace or request exception |
| Duplicate/alias drift | repeats an existing value under another name | consolidate |
| Missing token candidate | recurring justified need | solve locally, then evaluate extension |
| Approved exception | scoped and documented | retain until review |
| Unauthorized shared change | token contract changed | block release and restore baseline |

Examples:

| Property | Output | Verdict | Resolution |
|---|---:|---|---|
| card padding | `15px` | Fail | use approved `space.*` token, commonly `16px` if semantically correct |
| section gap | `21px` | Fail | select an approved spacing token; do not round by eye |
| label offset | `23px` | Fail | restructure alignment or request a documented exception |
| border width | `1px` | Conditional | pass only through an approved border token or technical rule |
| safe-area inset | `env(safe-area-inset-bottom)` | Technical exception | document; do not convert to a global spacing token |
| fluid size | calculated | Conditional | use approved token endpoints and documented interpolation |

Search for near misses, not only completely novel values. Values one or two units away from a token are common evidence of hand-tuned drift.

## 8. Lifecycle checkpoints

### Intake

- Freeze specification and token versions.
- Record source-of-truth order and authorization roles.
- Identify deprecated, missing, and conflicting areas.

### Architecture and wireframes

- Use approved patterns, templates, content structures, and component anatomy.
- Avoid introducing visual exceptions before functional need is proven.

### Visual design

- Bind properties to approved variables/styles/tokens.
- Review every local style, detached instance, raw value, and custom effect.
- Test representative and extreme content without breaking the system.

### Prototype

- Preserve component states, focus, keyboard, motion, responsiveness, and mode behavior.
- Do not simulate unsupported variants that implementation cannot reproduce.

### Handoff

- Include token and component references, not only measurements.
- Deliver a conformance matrix and approved deviation list.
- Block unexplained raw values and detached copies.

### Implementation QA

- Compare token names and semantic mapping, not screenshot similarity alone.
- Treat unauthorized token mutation or raw-value drift as defects.
- Confirm that accepted exceptions remain scoped.

### Project close

- Reconcile design, code, token package, library, and documentation.
- Remove temporary exceptions and duplicate local styles.
- Submit justified system proposals separately from shipped product decisions.

## 9. Output artifacts

### Design Conformance Contract

Include:

- Governing sources, versions, owners, and precedence
- Locked/selectable/extensible/deprecated/missing classification
- Token and component usage rules
- Authorization matrix
- Checkpoints and required evidence

### Token Usage Ledger

| Surface/component | Property | Required role | Approved token | Actual output | Status | Evidence/action |
|---|---|---|---|---|---|---|

### Deviation Register

| ID | Rule/token | Scope | Reason | Alternatives considered | Approval | Expiry/review | Migration |
|---|---|---|---|---|---|---|---|

Keep these artifacts in the project so conformance survives across tasks, agents, and sessions.

## 10. Quality gates

- **Authority gate:** governing sources and versions are explicit.
- **Traceability gate:** consequential decisions resolve through the specification-to-implementation chain.
- **Token gate:** no unauthorized raw, near-token, duplicate, or reinterpreted values remain.
- **Component gate:** approved components and contracts are reused before extension.
- **Exception gate:** every departure is scoped, approved, dated, and reviewable.
- **Accessibility gate:** conformance does not preserve an inaccessible or functionally incorrect rule without escalation.
- **Parity gate:** design, code, tokens, components, and documentation agree.
- **Release gate:** unauthorized shared-token changes block release.

Conformance is not visual similarity. It is traceable use of the approved system, with controlled and authorized exceptions.
