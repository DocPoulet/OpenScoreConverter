# Changelog

## [0.0.4] — Interactive single-staff editing

### Added
- Qt-independent `ScoreEditor` with atomic note insertion, deletion and replacements.
- Interactive select/add-note tools and snapped click-to-insert note positions.
- Pitch/duration properties, letter-key note entry, navigation and note-value shortcuts.
- Ctrl+click multi-selection, multi-delete and `+ Measure` command.
- Selection outlines on Qt notation scene items and preserved zoom when redrawing.
- Unsaved edit indicator, safe discard confirmations and editing regression tests.

### Not yet implemented
- Undo/Redo, dragging, professional engraving, persistent save/load, MIDI, PDF and playback.

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
