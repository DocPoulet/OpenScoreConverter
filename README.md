# OpenScore Converter

> **An open-source tool for converting, editing, transcribing and progressively simplifying music scores.**

OpenScore Converter is an ambitious open-source project aiming to create a powerful, completely free and local music transcription ecosystem.

The long-term goal is to provide high-quality conversion between **MIDI files, sheet music, MusicXML, PDF, images and other music formats**, while offering an integrated score editor and intelligent tools to improve readability, transcription quality and accessibility.

No subscriptions.  
No paid API.  
No cloud dependency.  
No artificial limitations.

Everything should be usable locally and improved by the community.

---

## Why this project?

There are already many MIDI-to-sheet-music and sheet-music-to-MIDI converters.

Unfortunately, automatic transcription often produces technically correct but practically unreadable results:

- unnecessarily complex rhythms;
- excessive ties;
- incorrect voice separation;
- poor left/right hand separation;
- awkward enharmonic spelling;
- tiny rests everywhere;
- inconsistent notation;
- bad quantization of human performances.

The objective of OpenScore Converter is not simply to convert musical data.

The objective is to produce a result that a **human musician would actually want to read and play**.

---

# Main goals

## MIDI → Sheet Music

Convert MIDI files into clean and readable scores.

The transcription engine will progressively support:

- perfectly quantized MIDI;
- human-recorded MIDI;
- timing imperfections;
- chords;
- tuplets;
- multiple voices;
- left/right hand separation;
- multiple tracks;
- multiple instruments;
- dynamics;
- pedal information;
- tempo changes;
- time signature changes;
- expressive performances.

Instead of blindly translating MIDI events into notation, the software will attempt to find the **most musically sensible representation**.

---

## Sheet Music → MIDI

The reverse conversion will also be supported.

Planned input sources include:

- PDF scores;
- MusicXML;
- scanned sheet music;
- PNG / JPEG images;
- smartphone photos;
- eventually handwritten music.

Optical Music Recognition will reconstruct the musical structure before allowing the user to review and correct the result.

The reconstructed score can then be exported to MIDI or other formats.

---

# Integrated Score Editor

Before building advanced conversion systems, OpenScore Converter will first provide its own integrated score editor.

The editor will eventually support:

- notes and rests;
- chords;
- multiple voices;
- multiple staves;
- clefs;
- key signatures;
- time signatures;
- accidentals;
- ties and slurs;
- tuplets;
- articulations;
- dynamics;
- tempo markings;
- instrument tracks;
- MIDI information;
- score metadata;
- undo / redo;
- interactive correction of transcription results.

The editor will act as the central workspace for all conversions.

---

# Intelligent Transcription

A MIDI file usually contains enough information to determine **what was played**.

It does not necessarily contain enough information to determine **how it should be written**.

Several valid notations may represent nearly the same performance.

OpenScore Converter will therefore use a hybrid approach combining:

**Deterministic algorithms**

for operations where the correct result can be calculated reliably.

Examples:

- MIDI parsing;
- note positions;
- measures;
- timing;
- file conversion;
- music structure.

**Artificial intelligence**

for ambiguous musical decisions where context and readability matter.

Examples:

- quantization;
- rhythmic interpretation;
- voice separation;
- left/right hand separation;
- enharmonic spelling;
- notation simplification;
- musical readability;
- ranking several possible transcriptions.

The goal is not to use AI everywhere.

The goal is to use it **where it actually improves the music**.

---

# Transcription Modes

The software is planned to offer several transcription modes.

### Faithful

Preserve the original performance as accurately as possible.

Best for studying exactly what was played.

### Readable

Clean timing imperfections and prioritize conventional, readable notation.

Best for normal sheet music.

### Simplified

Reduce unnecessary complexity while preserving the musical identity of the piece.

Best for learners or easier arrangements.

### Engraving

Prioritize professional-looking notation and musical conventions.

Best for publication-quality results.

---

# Progressive Difficulty System

One of the long-term goals of OpenScore Converter is to go beyond simple transcription.

The software should eventually be able to generate **progressively simplified versions of a piece**.

Instead of having only:

```text
Easy version
      ↓
Original version
```

the system could generate something closer to:

```text
Level 1
  ↓
Level 2
  ↓
Level 3
  ↓
Level 4
  ↓
Level 5
  ↓
Original piece
```

Each level would introduce additional musical complexity while remaining recognizably the same song.

The system could progressively restore:

- additional notes;
- faster rhythms;
- larger chords;
- left-hand complexity;
- syncopation;
- ornaments;
- octave jumps;
- accompaniment patterns;
- original voicings;
- expressive details.

For example:

```text
Original chord

C4 E4 G4 C5

        ↓

C4 G4 C5

        ↓

C4 G4

        ↓

C4
```

But difficulty cannot be determined only by counting notes.

A future AI system could also evaluate:

- hand span;
- finger movement;
- tempo;
- rhythmic complexity;
- independence between hands;
- repeated notes;
- jumps;
- chord shapes;
- polyphony;
- coordination;
- technical patterns.

The objective would be to help beginners learn music they actually enjoy by gradually approaching the original arrangement.

This system could eventually provide an experience inspired by progressive-learning systems found in modern music-learning software, while remaining completely open source.

---

# Assisted Validation

Automatic transcription will never be perfect.

Instead of hiding uncertainty, OpenScore Converter should expose it.

Elements generated by the transcription system may receive confidence scores.

Example:

```text
Measure 12     98%
Measure 13     94%
Measure 14     57% ⚠
Measure 15     89%
```

The editor could highlight uncertain sections and allow users to quickly review only problematic measures.

This becomes especially useful for batch conversion.

---

# Learning From Human Corrections

A future optional system could allow users to contribute corrections to improve transcription models.

The basic idea:

```text
Original MIDI
      ↓
Automatic transcription
      ↓
Human correction
      ↓
Corrected score
```

These pairs could form high-quality training data.

Participation should remain voluntary.

The software itself should remain fully usable offline without sending personal files anywhere.

---

# Supported Formats

## Initial development

### Input

```text
MIDI
```

### Output

```text
PDF
MusicXML
Project file
```

The first major goal is therefore:

```text
MIDI
 ↓
OpenScore Converter
 ↓
Editable score
 ↓
PDF / MusicXML
```

---

## Future formats

The architecture will be designed to eventually support as many useful music formats as possible.

Potential formats include:

```text
MIDI
MusicXML
MXL
PDF
MSCZ
MEI
SVG
PNG
JPEG
other score formats
```

---

# MusicXML

MusicXML will be used as one of the main interchange formats.

This will allow scores created by OpenScore Converter to be opened in compatible notation software and allow external scores to be imported into the application.

OpenScore Converter will nevertheless use its **own internal score representation**.

This allows the project to store information that does not naturally belong inside normal sheet-music formats, such as:

```text
transcription confidence
source MIDI event
AI predictions
alternative interpretations
user corrections
simplification information
difficulty information
```

---

# Playback

Audio playback is not part of the first development phase.

It is planned for later versions.

Future playback features may include:

- score playback;
- MIDI playback;
- synchronized playback cursor;
- solo / mute;
- metronome;
- instrument selection;
- MIDI velocity;
- dynamics;
- tempo control;
- section looping;
- SoundFont support;
- `.sf2` sound libraries.

This would eventually allow the editor to function both as a notation environment and as a lightweight MIDI playback environment.

---

# Planned Architecture

The project will use a hybrid **Python + C++** architecture.

```text
                ┌───────────────────────┐
                │       GUI / Editor    │
                │     Python / Qt       │
                └───────────┬───────────┘
                            │
                  ┌─────────▼─────────┐
                  │ Internal Score    │
                  │      Model        │
                  └─────────┬─────────┘
                            │
        ┌───────────────────┼────────────────────┐
        │                   │                    │
        ▼                   ▼                    ▼
   MIDI Engine         MusicXML Engine       Rendering
        │
        ▼
Transcription Engine
        │
   ┌────┴────┐
   │         │
Algorithms   AI
```

### Python

Python will primarily be used for:

- graphical interface;
- application logic;
- experimentation;
- AI / machine learning;
- transcription research;
- tooling.

### C++

C++ will progressively be used for:

- performance-critical components;
- large MIDI processing;
- optimized algorithms;
- low-level musical processing;
- components where native performance becomes useful.

Python and C++ modules can communicate through bindings.

---

# 🪟 Platform

Initial development targets:

```text
Windows
```

Cross-platform support may later include:

```text
Linux
macOS
```

The architecture should avoid unnecessary Windows-specific dependencies whenever possible.

---

# 🗺️ Development Roadmap

## Phase 0 — Score Editor

Build the foundation of the application.

```text
Score data model
        ↓
Basic rendering
        ↓
Note editing
        ↓
Undo / Redo
        ↓
Basic musical notation
        ↓
Project save/load
        ↓
MusicXML
```

Target:

> A functional editor capable of manually creating and editing a simple right-hand piano score.

---

## Phase 1 — Basic MIDI Transcription

```text
MIDI parser
      ↓
MIDI event representation
      ↓
Piano roll / debugging tools
      ↓
Perfectly quantized MIDI
      ↓
Basic score generation
```

Initial scope:

```text
Piano
Right hand
Single track
```

---

## Phase 2 — Human MIDI

Introduce intelligent quantization and rhythmic interpretation.

```text
Human performance
       ↓
Timing analysis
       ↓
Candidate rhythms
       ↓
Musical scoring
       ↓
Readable notation
```

---

## Phase 3 — Complete Piano

Add:

```text
Left hand
Two staves
Hand separation
Multiple voices
Advanced piano notation
```

---

## Phase 4 — Multi-track Music

Add:

```text
Multiple MIDI tracks
Multiple instruments
Percussion
Large scores
Instrument-aware notation
```

---

## Phase 5 — Intelligent Transcription

Improve transcription using machine learning and user corrections.

Focus areas:

```text
Quantization
Voice separation
Hand separation
Rhythmic readability
Enharmonic spelling
Score cleanup
```

---

## Phase 6 — Playback

Add MIDI and score playback.

Eventually support SoundFonts and `.sf2` libraries.

---

## Phase 7 — Sheet Music Recognition

Introduce:

```text
PDF → Score
Scan → Score
Image → Score
Photo → Score
```

Then progressively improve Optical Music Recognition.

---

## Phase 8 — Progressive Difficulty

Create intelligent arrangement and simplification tools.

The objective:

> Generate several playable difficulty levels between a beginner arrangement and the original score.

This will require advanced musical analysis and will likely become one of the largest AI components of the project.

---

# Current Status

> **Very early development / planning stage**

Current priority:

```text
Build the score editor and internal musical representation.
```

MIDI conversion, AI transcription and Optical Music Recognition will be implemented progressively after the editor foundation is stable.

---

# Open Source Philosophy

OpenScore Converter is intended to remain:

```text
Free
Open source
Offline-capable
Community-driven
No subscription
No mandatory account
No paid API dependency
```

Music tools should not require recurring payments simply to convert or edit files.

The project aims to provide an open platform that musicians, developers, researchers and learners can improve together.

---

# Contributions

Contributions will be welcome once the initial architecture is stable.

Future contribution areas may include:

- C++;
- Python;
- Qt / UI development;
- music theory;
- MIDI processing;
- MusicXML;
- engraving;
- machine learning;
- Optical Music Recognition;
- accessibility;
- testing;
- documentation;
- datasets;
- translations.

Musicians without programming experience will also be valuable contributors by testing transcription quality and correcting generated scores.

---

# License

This project is intended to be released under the **GNU General Public License v3.0 (GPLv3)**.

The objective is to keep the project and its derivatives open and accessible to the community.

---

# Long-Term Vision

OpenScore Converter should eventually become more than a converter.

The goal is to create an open music-processing platform capable of:

```text
Reading music
Writing music
Converting music
Correcting music
Playing music
Understanding music
Simplifying music
Teaching music
```

A musician should eventually be able to take a song they love, import it, obtain a clean score, correct it if necessary, generate an easier version adapted to their level, and progressively work their way toward the original arrangement.

All locally.

All for free.

All open source.

(Thanks Chat GPT for the good explanation for this project cause I suck for that😅, no more use of AI now!)
