# Architecture — v0.0.4

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

The renderer is a replaceable frontend: the core does not import Qt.
Each note/rest/chord is tagged with a tuple
`(part_index, staff_index, measure_index, voice_index, event_index)`.
Clicking an event maps that tuple to `EventPath`, and `ScoreEditor` validates
changes transactionally before mutating the original score. The Qt view redraws
but preserves zoom; the selected paths are highlighted. Clicking with Add Note
snaps both rhythmic offset and diatonic staff position. The rendering engine
remains intentionally simple until the post-v0.1.0 styles/glyphs refactor.
A score can contain incomplete measures while editing; errors are not
silently repaired.

## Data validation

`Score.validate()` reports missing voices/bar regions; it does not invent rests
or change score contents. Unsupported display details in v0.0.4 are marked
as limitations, never interpreted as valid professionally engraved results.

## Next milestones

- v0.0.4: selection, keyboard/mouse note entry, model mutation, renderer refresh (complete).
- v0.0.5: undo/redo command system.
- v0.0.6: fuller notation rules / proper layout.
- v0.0.7+: project persistence and MusicXML exchange.
- v0.1.1: separate glyphs, layout and reusable score styles.
- Later: MIDI transcriber, readable arrangement, PDF export, reverse OMR and AI.
