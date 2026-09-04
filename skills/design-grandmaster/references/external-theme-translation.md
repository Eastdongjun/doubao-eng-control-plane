# External Theme Translation

Use this module when the user supplies an external theme package, names a separately maintained visual grammar, or approves a researched theme direction. Design Grandmaster ships no theme library, theme assets, or example pages.

## Authority order

1. Approved project design system, brand system, token registry, and component contract
2. Explicit user decisions for the current project
3. The selected external theme package and its dated evidence
4. Project-local proposals and documented exceptions

An external theme never changes shared project tokens without explicit authorization. Map its semantic roles onto approved tokens where possible. If the project system cannot express an important mechanism, propose a scoped extension and wait for authorization before changing shared rules.

## Intake contract

Before applying an external theme, establish:

- Theme id, version, repository or supplied path, maintainer, license, and evidence date
- Design guide, semantic tokens, implementation assets, and representative proof locations
- Why the theme fits the audience, task, content, brand ownership, and desired emotion
- Whether its authority is `binding`, `user-directed`, or `research-derived`
- Governing project system and every conflict with the theme
- Signature mechanisms to retain and mechanisms to reject for usability, accessibility, performance, rights, or brand reasons
- Ordinary product state used to prove that the theme works beyond a showcase moment
- Responsive, localization, reduced-motion, and component-boundary behavior

Treat missing provenance, unclear licensing, unsynchronized versions, broken entrypoints, private local paths, inaccessible proof, or unexplained raw values as intake failures. Do not silently reconstruct a missing theme from its name or from the agent's memory.

## Translation workflow

1. Read the external manifest and design guide before implementation assets.
2. Verify version consistency, provenance, rights, entrypoints, and whether the proof renders.
3. Confirm fit against audience, task, content density, trust, brand ownership, and project constraints.
4. Extract relationships and mechanisms: palette topology, type roles, focal geometry, spacing rhythm, edge logic, component material, icon grammar, motion character, and ordinary-state behavior.
5. Map semantic roles to approved project tokens. Keep raw theme values quarantined from the project until the mapping is accepted.
6. Record retained, adapted, rejected, and unresolved mechanisms.
7. Produce one signature state and one ordinary utility state with real project content. Do not reuse the theme proof's page sequence.
8. Test mobile recomposition, text expansion, focus, contrast, localization, reduced motion, component internal safe areas, and document overflow.
9. Run the boundary audit for runnable multi-viewport work and record the result.

## Dependency boundary

- Reference an external theme by stable repository, release, commit, package version, or supplied immutable artifact when possible.
- Do not vendor its preview, docs, tokens, fonts, images, or CSS into Design Grandmaster.
- Copy assets into a product only when the user's project authorizes that dependency and the license permits it.
- A theme package is evidence and implementation input, not permission to create a second project design system.
- If the external theme becomes unavailable, continue only from project-approved mappings already recorded; do not invent missing rules.

## Anti-convergence rule

Themes are vocabulary, not templates. Preserve justified mechanisms while changing page sequence, information units, density curve, navigation, and component composition to fit the project. Category similarity never activates a theme automatically.
