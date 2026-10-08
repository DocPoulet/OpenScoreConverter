# 🎼 OpenScore Converter

**Free, offline-first, open-source music transcription, score editing and progressive music learning.**

> 🚧 **Current version: v0.0.1 — Project foundation.** This release opens a desktop UI; it does **not** convert MIDI or edit/produce sheet music yet.

## Vision

OpenScore Converter aims to convert music between **MIDI, printable scores (PDF), MusicXML, scans/images and other formats** while favoring results musicians can actually read.

In the long run it will combine an editable score, algorithmic transcription, targeted AI assistance and an optional progressive-difficulty arranger that helps beginners learn their favorite pieces in stages. No accounts, subscriptions, paid API calls or mandatory cloud services.

## What works in v0.0.1?

- Windows-oriented desktop GUI powered by **Python + PySide6**.
- **New** creates an empty *in-memory* project placeholder.
- File / Edit / View / Help menus, About dialog and status bar.
- Open/Save and Undo/Redo are deliberately disabled until implemented.
- Basic automated tests, GitHub Actions and a **C++17/CMake foundation**.

**Not yet supported:** score editing, MIDI or PDF loading, MusicXML, rendering, audio playback, file saving, AI.

## Installation (Windows / PowerShell)

Install [Python 3.12](https://www.python.org/downloads/) (64-bit, with the Python launcher) and have internet access for the initial dependency download.

In the extracted project folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m openscore
```

Alternatively, **double-click `setup_windows.bat` once** and then **`run_windows.bat`**. If Python 3.12 is missing, the setup script will try another installed Python 3 release (3.11–3.14).

After installing, you can also launch with:

```powershell
.\.venv\Scripts\python.exe run.py
```

> This is a **source-code release**, not a compiled standalone `.exe`. The initial `pip install` downloads PySide6; ordinary use does not need a connection.

## Test the Python code

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Optional C++ starter build

C++ is intentionally **not needed to launch the app** yet. If you have CMake and a C++17 compiler (e.g., Visual Studio Build Tools):

```powershell
cmake -S cpp -B cpp/build
cmake --build cpp/build --config Release
ctest --test-dir cpp/build -C Release --output-on-failure
```

There is no Python/C++ bridge in this release; it will be added when needed.

## Development plan

| Milestone | Goal |
| --- | --- |
| **v0.0.1** ✅ | Project structure, UI shell, tests, C++ foundation |
| v0.0.2 | Musical score data model, exact rhythmic fractions |
| v0.0.3 | Render a basic piano staff |
| v0.0.4–0.0.6 | Enter/edit notes, undo/redo, notation |
| v0.0.7–0.1.0 | Save projects, MusicXML, first useful editor |
| v0.2–0.4 | MIDI reading and right-hand piano transcription |
| v0.5–0.7 | More readable transcription, modes, assisted validation |
| v0.8–1.0 | Two hands, voices, PDF output, usable piano transcription |
| Later | Multiple instruments, SF2 playback, PDF/image recognition, AI improvements |

### Four planned transcription modes

- **Faithful:** preserve performance details.
- **Readable:** prioritize conventional musical notation.
- **Simplified:** reduce difficulty while preserving the identity of the piece.
- **Engraving:** aim for publication-quality notation.

### Progressive difficulty (long-term research goal)

Rather than providing only “easy” and “original,” the software aims to generate several gradually harder, **playable** versions of a piece, inspired by progressive-learning tools such as Rocksmith+. Difficulty may account for rhythm, coordination, finger movement, hand span, chord shapes and technical demands — not simply note count. User edits and optional voluntary contributions may eventually help train these models.

### Planned approach

- **Own internal score model** as the source of truth.
- **MusicXML** for exchange with other editors.
- Deterministic logic for unambiguous transformations; AI for difficult musical interpretation or ranking alternatives.
- **Qt / PySide6** for UI, **Python** for orchestration/experimentation, **C++** for performance-sensitive parts later.
- Windows first; cross-platform later.

## Structure

```text
src/openscore/         Python package and GUI
src/openscore/core/    In-memory project session (score model next)
src/openscore/score/   Placeholder for future score model
src/openscore/ui/      Qt windows and widgets
src/openscore/io/      Placeholder for future MIDI/MusicXML/PDF I/O
src/openscore/commands/       Future undo/redo commands
src/openscore/transcription/  Future MIDI transcription
cpp/                   Optional CMake/C++17 starter
setup_windows.bat / run_windows.bat   Windows launcher scripts
tests/                 Python smoke and unit tests
docs/                  Architecture and version scope
```

## License and contributions

**GNU GPL-3.0-only**, see [`LICENSE`](LICENSE). Contributions are welcome; see [`CONTRIBUTING.md`](CONTRIBUTING.md).

This project is **unaffiliated with MuseScore, Ubisoft, or Rocksmith+**.
