# Timing, Rhythm, and Choreography

Use this module for UI sequences, scrolling experiences, launch moments, title work, multi-object transitions, or any motion whose quality depends on orchestration.

## Contents

- [Temporal units](#temporal-units)
- [Beat design](#beat-design)
- [Rhythm variables](#rhythm-variables)
- [Temporal hierarchy](#temporal-hierarchy)
- [Duration selection](#duration-selection)
- [Easing and springs](#easing-and-springs)
- [Stagger](#stagger)
- [Scroll choreography](#scroll-choreography)
- [Long-form sequence](#long-form-sequence)

## Temporal units

Think in:

- **Frame:** smallest visible sample
- **Beat:** perceptible event or emphasis
- **Phrase:** group of beats with one intention
- **Scene:** bounded spatial/narrative context
- **Act:** larger change in tension or meaning

Do not tune individual durations before the beat structure is clear.

## Beat design

A useful beat vocabulary:

- Preparation
- Anticipation
- Commitment
- Primary action
- Reaction
- Follow-through
- Settle
- Hold
- Release

Interaction motion often compresses these beats; expressive motion may let them breathe. Include only beats that improve comprehension or emotional precision.

## Rhythm variables

- Tempo: perceived pace
- Meter: recurring temporal grouping
- Accent: moment of strongest emphasis
- Syncopation: controlled displacement from expectation
- Pause: deliberate stillness
- Overlap: one action beginning before another settles
- Stagger: related elements offset in time
- Counterpoint: independent motions that remain coherent
- Density: amount of change per unit time
- Repetition and variation

Avoid mechanically applying the same stagger to every collection. Sequence by hierarchy, causality, reading order, or physical propagation.

## Temporal hierarchy

Define:

1. Primary mover: carries the state change or message
2. Supporting mover: maintains context or reinforces causality
3. Environmental response: light, background, particles, sound, or adjacent objects
4. Stable anchor: gives orientation and contrast

The primary mover generally begins clearly, owns the strongest contrast, or resolves last. Multiple focal movements require deliberate counterpoint.

## Duration selection

Duration depends on:

- Distance and scale change
- Amount of information to perceive
- Frequency and urgency
- Input coupling
- Consequence and emotional weight
- Device and viewport
- Whether the transition can be interrupted
- Motion complexity and frame stability

Short is not automatically responsive; immediate feedback plus a longer non-blocking settle can feel faster than a silent delay.

## Easing and springs

Use duration/easing when:

- The sequence is authored
- Arrival time matters
- The action is not repeatedly interrupted
- Coordination with sound/editing requires deterministic time

Use springs when:

- Motion responds to changing input or target
- Interruption and retargeting are common
- Continuity of velocity matters
- Physical state seeking supports comprehension

Specify the perceptual result before numbers: decisive, gentle, weighty, elastic, overdamped, crisp, floating. Map to approved tokens or tested values.

## Stagger

Define:

- Ordering rule
- Interval or curve
- Maximum total delay
- Group size and wrap behavior
- Behavior on partial/virtualized lists
- Interruption and repeated-entry behavior
- Reduced-motion alternative

Long cascades punish users at scale. Cap the group, compress the interval, or animate the container.

## Scroll choreography

Classify the relationship:

- Scroll-triggered: event starts after a threshold
- Scroll-linked: progress follows scroll continuously
- Sticky scene: viewport becomes a stage for a bounded sequence
- Spatial navigation: scrolling changes position within a world

Specify entry/exit, pinning, progress mapping, reverse behavior, keyboard/page navigation, deep linking, content access without animation, reduced motion, and performance.

Do not hijack scroll physics merely to make a sequence feel cinematic.

## Long-form sequence

Build:

1. Hook
2. Orientation
3. Development
4. Contrast or rupture
5. Climax
6. Resolution
7. Exit or next action

Use animatics with rough timing and sound before expensive production. Judge the sequence without polish to reveal weak structure.
