"""Tests unitaires du moteur de correction."""

import unittest

from coach import get_feedback, normalize_answer
from conjugation import exercises_for, is_conjugation_correct, normalize_conjugation_answer


class NormalizeAnswerTests(unittest.TestCase):
    def test_ignores_case_punctuation_and_extra_spaces(self) -> None:
        self.assertEqual(
            normalize_answer("  Hello,   WORLD!  "),
            "hello world",
        )

    def test_normalizes_typographic_apostrophe(self) -> None:
        self.assertEqual(normalize_answer("Don’t"), "don't")


class GetFeedbackTests(unittest.TestCase):
    def test_exact_answer_receives_full_score(self) -> None:
        feedback = get_feedback("I managed a team.", "I managed a team.")
        self.assertEqual(feedback["score"], 100)
        self.assertTrue(feedback["is_correct"])

    def test_formatting_differences_do_not_reduce_score(self) -> None:
        feedback = get_feedback("  I MANAGED a team! ", "I managed a team.")
        self.assertEqual(feedback["score"], 100)

    def test_empty_answer_receives_zero(self) -> None:
        feedback = get_feedback("   ", "I managed a team.")
        self.assertEqual(feedback["score"], 0)
        self.assertFalse(feedback["is_correct"])

    def test_similar_answer_receives_partial_score(self) -> None:
        feedback = get_feedback("I manage a team.", "I managed a team.")
        self.assertGreater(feedback["score"], 0)
        self.assertLess(feedback["score"], 100)


class ConjugationTests(unittest.TestCase):
    def test_accepts_case_and_spacing_differences(self) -> None:
        self.assertTrue(is_conjugation_correct("  HAD   RESOLVED ", ["had resolved"]))

    def test_preserves_spanish_accents(self) -> None:
        self.assertEqual(normalize_conjugation_answer("HABLÉ!"), "hablé")
        self.assertFalse(is_conjugation_correct("hable", ["hablé"]))

    def test_rejects_empty_answer(self) -> None:
        self.assertFalse(is_conjugation_correct("  ", ["worked"]))

    def test_each_tense_has_exercises(self) -> None:
        self.assertEqual(len(exercises_for("English", "Past simple")), 2)
        self.assertEqual(len(exercises_for("Español", "Pretérito imperfecto")), 2)


if __name__ == "__main__":
    unittest.main()
