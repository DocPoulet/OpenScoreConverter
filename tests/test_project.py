"""Pure Python tests: these should pass without a GUI toolkit."""

import unittest

from openscore import __version__
from openscore.core.project import ProjectSession


class ProjectSessionTests(unittest.TestCase):
    """Validate the v0.0.2 project session backed by a score."""

    def test_starts_without_a_project(self):
        session = ProjectSession()
        self.assertFalse(session.has_project)
        self.assertIsNone(session.name)

    def test_new_project_creates_placeholder(self):
        session = ProjectSession()
        session.create_new()
        self.assertTrue(session.has_project)
        self.assertEqual(session.name, "Untitled")
        self.assertIsNotNone(session.score)
        self.assertEqual(session.score.parts[0].name, "Piano")

    def test_project_name_can_be_changed(self):
        session = ProjectSession()
        session.create_new("  My piece  ")
        self.assertEqual(session.name, "My piece")
        self.assertEqual(session.score.title, "My piece")

    def test_empty_project_name_rejected(self):
        session = ProjectSession()
        with self.assertRaises(ValueError):
            session.create_new("  ")
        self.assertFalse(session.has_project)

    def test_clear_returns_to_welcome_state(self):
        session = ProjectSession()
        session.create_new("Piece")
        session.clear()
        self.assertFalse(session.has_project)
        self.assertIsNone(session.score)

    def test_version(self):
        self.assertEqual(__version__, "0.0.3")


if __name__ == "__main__":
    unittest.main()
