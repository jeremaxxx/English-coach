"""Tests unitaires du moteur de correction."""

import unittest

from coach import get_feedback, normalize_answer
from conjugation import EXERCISES, LESSONS, exercises_for, is_conjugation_correct, normalize_conjugation_answer
from irregular_verbs import irregulars_for
from vocabulary import VOCABULARY, vocabulary_for


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
        for language, lessons in LESSONS.items():
            for tense in lessons:
                self.assertGreaterEqual(len(exercises_for(language, tense)), 4)

    def test_large_bilingual_exercise_bank(self) -> None:
        self.assertGreaterEqual(len(EXERCISES), 80)


class LearningContentTests(unittest.TestCase):
    def test_irregular_directories_are_substantial(self) -> None:
        self.assertGreaterEqual(len(irregulars_for("English")), 70)
        self.assertGreaterEqual(len(irregulars_for("Español")), 30)

    def test_vocabulary_covers_humanitarian_and_daily_life(self) -> None:
        self.assertGreaterEqual(len(VOCABULARY), 80)
        humanitarian = vocabulary_for("Español", ["Humanitarian aid"])
        daily = vocabulary_for("English", ["Travel", "Home"])
        self.assertGreaterEqual(len(humanitarian), 10)
        self.assertGreaterEqual(len(daily), 20)


if __name__ == "__main__":
    unittest.main()
