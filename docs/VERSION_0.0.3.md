# v0.0.3 — Read-only staff preview

## New features

- Qt `QGraphicsScene` vector-based score preview inside the existing Windows application.
- `File > New score` creates a genuine blank treble-clef 4/4 bar and draws it.
- `File > Open example score` creates a four-bar score that demonstrates notes,
  rests, a chord, a sharp, a dotted rhythm, flags and ledger lines.
- Automatic redraw from the **real v0.0.2 Score model**. The renderer does
  not store its own duplicate music data and does not change the model.
- Zoom in / out / reset, plus scroll/drag for navigation.
- Basic per-note/rest tooltips and attached model paths for later selection.
- Exact rhythm lookup and diatonic staff positions are testable without Qt.

## Important limitations

The notation engine is a **lightweight preview**, not a finished professional
engraver. Only the first staff is drawn. The supported display is currently
piano right hand, treble clef, C major, single-voice 4/4 notation.
Notes with standard, dotted (up to two dots) and basic triplet durations have
approximate glyphs. Triplets lack full group brackets, beaming is not yet
implemented, and complex chords / multiple voices may overlap visually.
A duration that cannot be represented is shown **explicitly as a red text
fallback** rather than being silently misrepresented. Non-C major key signatures
are also explicitly flagged rather than drawn incorrectly. A changed time
signature within a system is not yet fully engraved.

`New score` is empty by design. Use **Open example score** for visible musical
content. Since the v0.0.3 editor is read-only, the example is a convenient
way to inspect progress before note entry in v0.0.4.

No opening/saving/export of score files yet. No MIDI/PDF conversion, playback,
AI, or SF2 support. Opening another score discards the in-memory one.

## Components

- `openscore.engraving.layout`: pure operations, exact fractions.
- `openscore.ui.notation.scene_renderer`: translates Score into Qt primitives.
- `openscore.ui.widgets.score_workspace`: visual workspace and zoom controls.
- `openscore.score.demo`: self-contained demonstration Score.

## Manual GUI check (Windows)

1. Run `setup_windows.bat` and `run_windows.bat`.
2. Choose `New score`: see a blank treble staff and 4/4 meter.
3. Choose `File > Open example score`: see 4 measures in 2 rows.
4. Hover noteheads and rests for pitch/duration tooltips.
5. Use +/- and 100% to change and reset zoom; scroll horizontally/vertically.
6. Verify `Open`/`Save`/`Undo`/`Redo` are still disabled.

## Automated tests

`python -m unittest discover -s tests -v` includes pure layout/model tests and
optional offscreen GUI tests. Tests need an environment with PySide6 to execute
the Qt-specific cases. C++ scaffolding remains unchanged.
