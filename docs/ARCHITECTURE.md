# Architecture (v0.0.1)

## Principles

1. `openscore.core` remains independent from PySide6 and display details.
2. UI widgets signal intent; the application state owns the session.
3. No music parsing, PDF conversion or score engraving is implemented yet.
4. `openscore.score` will become a format-independent musical representation.
5. Future import/export adapters transform external formats into/out of it.
6. Use exact rational fractions for notated rhythmic durations.
7. Keep human-performance timing separate from notated rhythm (not identical concepts).
8. Prefer tests with small, explicit expected results over subjective UI snapshots alone.

## Packages

- `application.py`: starts QApplication and the top-level window.
- `core/project.py`: minimal in-memory project session status.
- `ui/main_window.py`: menus, status bar, window settings and page switching.
- `ui/widgets/`: welcome and empty score placeholder pages.
- `score/`, `io/`, `transcription/`, `commands/`: reserved packages without implementations.
- `cpp/`: independently buildable C++17 placeholder library; no Python binding yet.

## Later flow

```text
MIDI input ─┐
MusicXML ───┼─> Score model <─> Editor ─> MusicXML / PDF / MIDI
PDF / OMR ─┘       ▲
                  │
          Transcription engine
          (algorithms + selective AI)
```

## Next step: v0.0.2

Specify and test `Score`, `Part`, `Staff`, `Measure`, `Voice`, `Note`,
`Rest`, `Chord`, meters, keys, clefs and the rules for exact temporal positions.
Do not couple these types to Qt types or to MusicXML-specific fields.
