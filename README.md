# 🎼 OpenScore Converter

**Free, offline-first, open-source music transcription, score editing and progressive music learning.**

> 🚧 **Current version: v0.0.3 — First graphical notation preview.** You can create an empty staff and inspect a four-bar example score. **The preview is read-only**: MIDI/PDF conversion, interactive score editing, saving music files and playback are not available yet.

## Vision

OpenScore Converter aims to convert between **MIDI, readable PDF sheet music, MusicXML and eventually scanned/image scores**. The goal is notation that musicians can actually read, not merely a technically correct file conversion.

A longer-term vision includes a full score editor, hybrid algorithmic/AI-assisted transcription, batch processing and a **progressive difficulty system**: a series of increasingly faithful arrangements to help beginners learn songs they enjoy. The project is designed to remain free, local and open source — no accounts, subscriptions or paid APIs.

## ✨ What's new in v0.0.3?

- **Real score preview:** five-line staff, treble clef, 4/4 meter and bar lines.
- **Notes and rests:** filled/hollow noteheads, stems, individual flags, chords, ledger lines, sharps/flats/naturals, dots and basic triplet markers.
- **Example score:** four complete measures to examine without needing note-entry tools.
- **Zoom and scrolling:** clickable controls and a pannable, vector-based score page.
- **Tooltips and item IDs:** hover rendered notes/rests to inspect pitch and duration; IDs prepare future selection/editing.
- **Existing music model unchanged:** exact fractions, multiple independent voices in memory, validation and C++17/CMake foundation from v0.0.2.

**Display limitations:** This is an early preview, not publication-quality notation. It renders the first staff only, targeting right-hand piano in **C major, treble clef**. No beams or complete tuplet engraving; simultaneous voices may collide. Unsupported lengths are labelled explicitly rather than silently drawn as wrong notes. Extended key signatures and meter changes are not fully engraved yet.

## 🚀 Install and launch on Windows

1. Install **Python 3.12** (64-bit recommended).
2. Extract the ZIP containing this repository.
3. Double-click **`setup_windows.bat`** (initial dependency installation requires internet).
4. Double-click **`run_windows.bat`**.
5. On the welcome page, choose **View example score**, or choose **File → Open example score**.
6. Use the **− / + / 100%** controls; hover noteheads to see their pitch and duration.

Alternatively in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m openscore
```

This is the source code, not a standalone executable. Once installed, normal usage is offline.

### New score versus example score

`New score` makes a **blank** right-hand piano Score with a visible 4/4 staff. The example loads a separate **in-memory** Score containing quarter/eighth/half/whole notes, a half-note chord, rests, a sharp, a dotted note and an extra ledger line. Opening either one replaces the previous in-memory project; **saving isn't implemented yet**.

## 🏗️ Structure

```text
src/openscore/
  score/                     Qt-free score model + example data
  engraving/layout.py        Exact duration and staff-position calculations
  ui/notation/               QGraphicsScene vector renderer
  ui/widgets/                Welcome page and score preview workspace
  core/                      Current in-memory project
  io/                        Future format adapters
  transcription/             Future MIDI and AI tools
  commands/                  Future undo/redo framework
cpp/                          C++17 foundation
examples/                     Programmatic model example
tests/                        Pure Python and optional GUI tests
docs/                         Architecture and release notes
```

`MusicXML` is planned as an interchange format, **not** the internal data model. Python handles application/UI and future ML; C++ can later accelerate measured bottlenecks.

## 🧪 Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests include model checks, exact duration classification, staff note positions and sample-score validation. On a machine with PySide6 installed, they also include offscreen GUI checks; Qt tests are skipped without PySide6.

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
| **v0.0.3 ✅** | **Read-only visual score preview** |
| v0.0.4 | Add/select/delete notes directly in the staff |
| v0.0.5 | Undo/Redo |
| v0.0.6 | More complete musical notation |
| v0.0.7 | Save/reopen a project |
| v0.0.8–v0.1.0 | MusicXML and initial usable manual editor |
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

See [`docs/VERSION_0.0.3.md`](docs/VERSION_0.0.3.md) for feature details and known rendering limitations.
