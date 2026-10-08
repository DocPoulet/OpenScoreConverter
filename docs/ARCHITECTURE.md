# Architecture — v0.0.3

OpenScore Converter uses its own Qt-independent music representation. Graphical
notation and eventually MusicXML/MIDI/PDF are adapters reading that model.

```text
Score → Part → Staff → Measure → Voice → (Note | Rest | Chord)
                             │
                             └── openscore.engraving.layout (pure functions)
                                        │
                                        ▼
                              ScoreSceneRenderer (Qt)
                                        │
                                        ▼
                               QGraphicsScene/View
                                        │
                                        ▼
                               ScoreWorkspace (GUI)
```

## Written time

Durations and measure-local positions use `Fraction` in **whole-note units**.
`1/4` is a quarter; `1/12` is a triplet eighth. This is distinct from the
future MIDI tick/performance timeline.

## Preview isolation

The read-only renderer is a replaceable frontend: the core does not import Qt,
no data is stored in Qt items, and each note/rest is tagged with a tuple
`(part_index, staff_index, measure_index, voice_index, event_index)`, allowing
future hit testing in v0.0.4. Layout helpers and the rendering scene live in
separate modules. The current scene preview is not a music engraving standard;
later versions may integrate a dedicated engraving backend (e.g., Verovio).

## Data validation

`Score.validate()` reports missing voices/bar regions; it does not invent rests
or change score contents. Unsupported display details in v0.0.3 are marked
as limitations, never interpreted as valid professionally engraved results.

## Next milestones

- v0.0.4: selection, keyboard/mouse note entry, model mutation, renderer refresh.
- v0.0.5: undo/redo command system.
- v0.0.6: fuller notation rules / proper layout.
- v0.0.7+: project persistence and MusicXML exchange.
- Later: MIDI transcriber, readable arrangement, PDF export, reverse OMR and AI.
