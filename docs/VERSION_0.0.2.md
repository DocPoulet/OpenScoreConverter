# v0.0.2 — Score model: acceptance checklist

## Implemented

- [x] Qt-independent score model: `Score → Part → Staff → Measure → Voice → Events`.
- [x] Events: `Note`, `Rest`, and simultaneous `Chord`.
- [x] Written pitches: spelled letter/alteration/octave, preserved enharmonic identity.
- [x] Pitch-to-MIDI-key conversion (`0..127`) for future export.
- [x] Exact `Fraction` timing in whole-note units; floats intentionally rejected.
- [x] Clef, key and time signature primitives.
- [x] Consecutive note/rest/chord insertion, sorted explicit placement.
- [x] Strict overlap and overrun protection per written voice.
- [x] Multiple independent voices, including simultaneous notes.
- [x] Incomplete bars are permitted during editing but reported by validation.
- [x] Special short bars (pickup/anacrusis) via `actual_duration`.
- [x] Project `New` now creates a genuine piano part, treble staff and 4/4 bar.
- [x] GUI placeholder displays the actual in-memory part/staff/measure counts.
- [x] Demo example and automated unit tests.
- [x] Previous v0.0.1 GUI, license, scripts and C++ scaffold retained.

## Explicitly not in scope

- Actual staff engraving/rasterization/SVG/PDF, editing by mouse or keyboard.
- Project saving/loading, MusicXML, MIDI parsing and transcription.
- Tuplet *notation* / beaming / ties. Rational values such as 1/12 are
  representable; their later graphical notation is not yet implemented.
- Complex time maps, note-level dynamics, articulation, pedals and tempo.
- Audio playback and SoundFont support, AI, optical score recognition.

## Time conventions

- **One whole note = 1**.
- Quarter note = `Fraction(1, 4)`.
- Eighth note = `Fraction(1, 8)`.
- One triplet eighth = `Fraction(1, 12)` (not yet rendered as a tuplet).
- `start` and `duration` are measured from the **start of a measure**.
- A measure's effective capacity is `time_signature.duration`, unless
  `actual_duration` is given for a pickup/partial measure.
- Event intervals are half-open `[start, start + duration)`.
- Chords are one event carrying several simultaneous pitches.
- Each voice separately forbids overlaps; different voices may overlap.
- Empty gaps are not silently filled; the validator reports them.

## Planned for v0.0.3

Render our existing musical model visually, using a notation renderer
(evaluating Verovio/MusicXML-to-SVG integration) without making renderer
structures part of the score model.
