# OpenScore Converter v0.0.4 — Interactive note editor

## Scope
- Windows, Python/PySide6, one rendered treble staff, in-memory only.
- Select a rendered note/rest/chord with a click; Ctrl+click for multiple.
- Add notes with mouse: select `Add note`, duration and alteration; click staff.
- Add notes with keyboard while Add Note mode is active: A–G append to the active measure.
- 1–5 select whole / half / quarter / eighth / sixteenth duration.
- Delete selected events; select note + change pitch, octave, accidental, duration.
- `Up`/`Down` adjust selected note by diatonic step; `Left`/`Right` navigate.
- `+ Measure` creates a new measure; use the vertical scrollbar to reach it.

## Edit safety
- ScoreEditor performs collision/overflow checks before applying edits.
- Zoom and scroll position survive repaints; score preview and model share one Score.
- All edits are **unsaved**; leaving the document prompts before discarding.
- Undo/Redo and persistent file save/load remain disabled intentionally.

## Technical design
`editor/operations.py` contains Qt-independent editing logic. `ui/widgets/score_workspace.py`
manages the toolbar, inspector and Qt input. `ui/notation/scene_renderer.py` continues
using the v0.0.3 graphics code and adds event hit areas, highlights, measure geometry.

## Limitations
- Only a single treble-clef staff is interactively supported.
- Simplified engraving; note heads and rests are vector Qt shapes.
- The editor inserts single notes, not chord tones. Existing chords can be selected,
  duration-edited and deleted; editing individual pitches within chords comes later.
- Drag-and-drop notes, Undo/Redo, file save/load, MIDI/PDF and audio remain future goals.
- No key-signature engraving beyond early C-major display; click snapping uses
  chosen duration and assumes the active 4/4 measure is visually displayed.
- All edits to a voice must remain non-overlapping, and may leave gaps pending
  later automatic rest-filling features.

## Tests
Run `python -m unittest discover -s tests -v` after installing the package.
Pure-Python edit/model tests can also run with `PYTHONPATH=src` without Qt.
Qt-based GUI tests run offscreen when PySide6 is installed.
