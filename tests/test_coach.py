"""Tests unitaires du moteur de correction."""

import unittest
from unittest.mock import patch

from c1_content import ADVANCED_GRAMMAR, WRITING_PROMPTS, advanced_exercises_for
from coach import get_feedback, normalize_answer
from conjugation import EXERCISES, LESSONS, exercises_for, is_conjugation_correct, normalize_conjugation_answer
from irregular_verbs import irregulars_for
from vocabulary import VOCABULARY, vocabulary_for
from writing_coach import evaluate_with_openai, local_writing_analysis, progress_export, validate_progress_import


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

    def test_c1_content_covers_both_languages(self) -> None:
        self.assertGreaterEqual(len(WRITING_PROMPTS), 12)
        self.assertTrue(any(prompt["language"] == "English" for prompt in WRITING_PROMPTS))
        self.assertTrue(any(prompt["language"] == "Español" for prompt in WRITING_PROMPTS))
        self.assertGreaterEqual(len(ADVANCED_GRAMMAR), 20)
        self.assertTrue(advanced_exercises_for("English"))
        self.assertTrue(advanced_exercises_for("Español"))


class WritingCoachTests(unittest.TestCase):
    def test_local_analysis_reports_objective_features(self) -> None:
        text = (
            "Although the proposal appears reasonable, it may create delays.\n\n"
            "However, a limited pilot would provide stronger evidence.\n\n"
            "Therefore, we recommend testing it before wider implementation."
        )
        analysis = local_writing_analysis(text, 20, 80)
        self.assertTrue(analysis["checks"]["Length within target"])
        self.assertTrue(analysis["checks"]["At least 3 paragraphs"])
        self.assertTrue(analysis["connectors"])
        self.assertTrue(analysis["hedges"])

    def test_progress_round_trip(self) -> None:
        state = {"writing_attempts": [{"title": "Test"}], "error_notebook": [], "review_cards": []}
        restored = validate_progress_import(__import__("json").loads(progress_export(state)))
        self.assertEqual(restored["writing_attempts"][0]["title"], "Test")

    def test_progress_rejects_unknown_version(self) -> None:
        with self.assertRaises(ValueError):
            validate_progress_import({"version": 99})

    @patch("writing_coach.urllib.request.urlopen")
    def test_api_request_disables_storage_and_parses_feedback(self, mock_urlopen) -> None:
        feedback = {
            "summary": "Clear text.",
            "scores": {"task_achievement": 4, "organisation": 4, "grammar": 4,
                       "vocabulary": 3, "register": 4},
            "strengths": ["Clear structure", "Appropriate tone"],
            "priorities": ["Use richer collocations", "Vary sentence openings"],
            "corrections": [], "next_exercise": "Rewrite one paragraph.",
        }

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                payload = {"output": [{"type": "message", "content": [
                    {"type": "output_text", "text": __import__("json").dumps(feedback)}
                ]}]}
                return __import__("json").dumps(payload).encode()

        mock_urlopen.return_value = FakeResponse()
        result = evaluate_with_openai("secret-test-key", "gpt-5.6-luna", "English", "Task", ["Be clear"], "Draft")
        request = mock_urlopen.call_args.args[0]
        sent = __import__("json").loads(request.data.decode())
        self.assertFalse(sent["store"])
        self.assertEqual(result["scores"]["grammar"], 4)


if __name__ == "__main__":
    unittest.main()
