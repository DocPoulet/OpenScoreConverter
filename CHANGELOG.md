# Changelog

## [0.0.3] — Read-only score preview

### Added
- Qt vector scene drawing real `Score` note/rest/chord events on a staff.
- Treble clef, 4/4 signature, bar lines, noteheads, stems, flags, accidentals,
  ledger lines and elementary rest/dot/tuplet previews.
- Sample four-bar piano score (`File > Open example score`).
- Zoom controls, scrollable white page, note/rest hover tooltips.
- Qt-free exact-rhythm and staff-position helpers with regression tests.
- Additional conditional offscreen Qt GUI tests.

### Changed
- `New score` now shows a blank staff instead of the v0.0.2 text placeholder.
- Visual workspace and home screen updated for v0.0.3.

### Not yet implemented
- Mouse/keyboard editing, Undo/Redo, score save/load, MIDI, PDF and playback.
- Professional layout (beaming, reliable tuplets, arbitrary keys, multi-staff).

## [0.0.2] — Musical data model
- Pure musical data hierarchy and exact rational timing.

## [0.0.1] — Desktop skeleton
- PySide6 window, menus, native C++ scaffold and automated tests.
