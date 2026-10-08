# 🎼 OpenScore Converter

**Free, offline-first, open-source music transcription, score editing and progressive music learning.**

> 🚧 **Current version: v0.0.4 — Interactive note editing.** You can select, create, delete and change notes in a right-hand piano staff. **All edits live only in memory:** saving, Undo/Redo, MIDI/PDF conversion and playback are not available yet.

## Vision

OpenScore Converter aims to convert between **MIDI, readable PDF sheet music, MusicXML and eventually scanned/image scores**. The goal is notation that musicians can actually read, not merely a technically correct file conversion.

A longer-term vision includes a full score editor, hybrid algorithmic/AI-assisted transcription, batch processing and a **progressive difficulty system**: a series of increasingly faithful arrangements to help beginners learn songs they enjoy. The project is designed to remain free, local and open source — no accounts, subscriptions or paid APIs.

## ✨ What's new in v0.0.4?

- **Interactive score editor:** click noteheads, rests or chords to select them; Ctrl+click to select more than one event.
- **Add Note tool:** choose a duration and an accidental, then click inside a displayed staff/measure to insert a snapped single note. The exact measure position is preserved in the score model.
- **Properties inspector:** change a single selected note's pitch letter, octave and accidental, or change a selected event's duration.
- **Delete / Backspace:** remove selected notes, chords or rests; multi-selection deletion is supported.
- **Keyboard note entry:** in Add Note mode, press A–G to append a note to the active measure. Use keys 1–5 to choose whole, half, quarter, eighth or sixteenth notes.
- **Arrow key controls:** ↑/↓ transpose a *single* selected note by one staff position; ←/→ navigate events in the selected measure.
- **More measures:** add a measure with `+ Measure` and continue editing.
- **Validation:** reject note insertion/length changes that overlap another event in the same voice or extend outside the bar. Failed operations leave the existing score unchanged.
- **Safe warnings:** a dirty-document marker and confirmation when leaving/replacing a modified project (because project persistence is not available yet).

The current rendering engine is **kept in its simple v0.0.3 form**, with only hit-testing/selection support added. The planned renderer/glyph/style architectural cleanup remains scheduled **after v0.1.0, in v0.1.1**.

**Limits:** only the first treble-clef staff is editable visually; adding a note creates one note, not a chord. Existing chords/rests can be selected/deleted and their duration adjusted, but you can't modify an individual chord pitch yet. No mouse dragging of notes, ties/slurs/beams or professional page layout. Key signatures other than C major are not fully engraved. No file save or Undo/Redo yet.

## 🚀 Install and launch on Windows

1. Install **Python 3.12** (64-bit recommended).
2. Extract the ZIP containing this repository.
3. Double-click **`setup_windows.bat`** (initial dependency installation requires internet).
4. Double-click **`run_windows.bat`**.
5. Choose **New score** to enter your own notes, or **View example score** to modify existing ones.
6. Click **Add note**, select a note duration, and click a position on the staff; click **Select** to pick an existing note.
7. Use the note-properties panel to change the selected note. To add a bar, click **+ Measure**.
8. **Important:** edited music will be lost after exiting this version; Save remains disabled.

Alternatively in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m openscore
```

This is the source code, not a standalone executable. Once installed, normal usage is offline.

### New score versus example score

`New score` makes a **blank** right-hand piano Score with a visible 4/4 staff. The example loads a separate **in-memory** Score containing quarter/eighth/half/whole notes, a half-note chord, rests, a sharp and a dotted note. **No save/load exists yet**; a confirmation dialog protects against accidental loss when you switch projects or close the app.

## 🏗️ Structure

```text
src/openscore/
  score/                     Qt-free score model + example data
  engraving/layout.py        Exact duration and staff-position calculations
  ui/notation/               QGraphicsScene vector renderer
  ui/widgets/                Welcome page and interactive score editor
  editor/                    Qt-independent validated edit operations
  core/                      Current in-memory project
  io/                        Future format adapters
  transcription/             Future MIDI and AI tools
  commands/                  Future undo/redo framework
cpp/                          C++17 foundation
examples/                     Programmatic model example
tests/                        Pure Python and optional GUI tests
docs/                         Architecture and release notes
```

`MusicXML` is planned as an interchange format, **not** the internal data model. Python handles application/UI and future ML; C++ can later accelerate measured bottlenecks. Event paths used for selection are temporary in-memory indices; the command/history system is a v0.0.5 goal.

## 🧪 Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests include transactional editing checks (overlap, overflow, atomic replacement, note pitch, measures), model validation, engraving helpers and sample-score validation. On a machine with PySide6 installed, they also include offscreen GUI checks; Qt tests are skipped without PySide6.

Optional C++ check (CMake plus a compatible C++17 compiler):

```powershell
cmake -S cpp -B cpp/build
cmake --build cpp/build --config Release
ctest --test-dir cpp/build -C Release --output-on-failure
```

## 🗺️ Roadmap

| Version | Goal |
| --- | --- |
| v0.0.1 ✅ | Windows GUI shell / basic menus |
| v0.0.2 ✅ | Format-independent music model and exact rhythmic times |
| v0.0.3 ✅ | Read-only visual score preview |
| **v0.0.4 ✅** | **Interactive note selection, insertion, deletion, property editing** |
| v0.0.5 | Undo/Redo |
| v0.0.6 | More complete musical notation |
| v0.0.7 | Save/reopen a project |
| v0.0.8–v0.1.0 | MusicXML and initial usable manual editor |
| **v0.1.1** | **Renderer refactor: glyphs, layout and configurable score styles** |
| v0.2–v0.7 | MIDI input, transcription, quantization, readability modes |
| v0.8–v1.0 | Two-handed piano, voices and PDF exports |
| Later | Multi-instrument, SF2 playback, PDF/image recognition, AI refinement and progressive difficulty |

### Planned transcription modes

- **Faithful:** preserve performance timing/details.
- **Readable:** favor conventional legible notation.
- **Simplified:** easier arrangement with retained musical identity.
- **Engraving:** strive for professional notation quality.

### Progressive difficulty (long-term)

Generate a ladder of playable arrangements from a simple skeleton toward the original, progressively restoring rhythm, harmony, left-hand accompaniment, jumps and technical details. An eventual AI could estimate the actual difficulty (hand span, coordination, tempo, rhythmic density, etc.), not just count notes. Inspired by the broad idea of progressive learning in music games, independently developed and fully open source.

## 🤝 Community & license

Licensed under **GNU GPL-3.0-only** (see [`LICENSE`](LICENSE)). Contributions are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). The project is unaffiliated with MuseScore, Rocksmith+ or Ubisoft.

See [`docs/VERSION_0.0.4.md`](docs/VERSION_0.0.4.md) for editing tools, key bindings and known limitations.
