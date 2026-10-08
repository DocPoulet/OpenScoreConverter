# Contributing to OpenScore Converter

Thank you for considering a contribution! The project is in early development.

## Working locally

1. Set up the Python project (see `README.md`).
2. Make a focused branch for your change.
3. Add or update tests where possible.
4. Run `python -m unittest discover -s tests -v`.
5. Open a pull request describing what changed and how it was tested.

## Ground rules

- Keep core music logic independent of Qt wherever possible.
- Do not add paid/cloud dependencies for required functionality.
- Document the purpose, inputs and outputs of non-trivial public APIs.
- Do not add a new format, feature or AI model without a usable test example.
- Avoid storing or submitting copyrighted arrangements or personal scores
  without permission.
- Share code under the project's GPL-3.0-only license.

The roadmap describes goals, not a promise that every feature exists today.
