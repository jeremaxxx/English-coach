"""Fonctions de correction du coach d'anglais local."""

import re
from difflib import SequenceMatcher
from typing import Dict, Union


Feedback = Dict[str, Union[int, bool, str]]


def normalize_answer(text: str) -> str:
    """Normalise une réponse avant comparaison.

    La casse, la ponctuation et les espaces multiples ne pénalisent pas
    l'utilisateur. Les apostrophes typographiques sont aussi uniformisées.
    """

    text = text.lower().replace("’", "'")
    text = re.sub(r"[^a-z0-9']+", " ", text)
    return " ".join(text.split())


def get_feedback(user_answer: str, expected_answer: str) -> Feedback:
    """Compare deux réponses et renvoie un score ainsi qu'un court message.

    Cette fonction constitue la frontière du moteur de correction. Elle pourra
    donc être remplacée plus tard sans modifier l'interface en ligne de commande.
    """

    normalized_user = normalize_answer(user_answer)
    normalized_expected = normalize_answer(expected_answer)

    if not normalized_user:
        score = 0
    else:
        similarity = SequenceMatcher(
            None, normalized_user, normalized_expected
        ).ratio()
        score = round(similarity * 100)

    if score == 100:
        message = "Excellent: your answer matches the expected answer."
    elif score >= 80:
        message = "Very good: your answer is close to the expected answer."
    elif score >= 60:
        message = "Good attempt: review a few words or the sentence structure."
    else:
        message = "Keep practising: compare your answer with the model answer."

    return {
        "score": score,
        "is_correct": score == 100,
        "message": message,
    }
