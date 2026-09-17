"""Analyse locale et évaluation API optionnelle des productions écrites."""

import json
import re
import urllib.error
import urllib.request
from collections import Counter
from typing import Any, Dict, List


CONNECTORS = {
    "however", "nevertheless", "moreover", "furthermore", "therefore",
    "consequently", "although", "whereas", "while", "nonetheless",
    "however", "therefore", "aunque", "sin embargo", "además", "por tanto",
    "no obstante", "mientras que", "por consiguiente", "aun así",
}
HEDGES = {
    "may", "might", "appears", "seems", "likely", "unlikely", "arguably",
    "potentially", "perhaps", "puede", "podría", "parece", "probablemente",
    "posiblemente", "hasta cierto punto",
}
INFORMAL_MARKERS = {
    "gonna", "wanna", "a lot of", "kids", "stuff", "thing", "things",
    "un montón", "cosas", "tío", "super",
}


def words(text: str) -> List[str]:
    """Retourne les mots Unicode en minuscules."""

    return re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)?", text.casefold(), re.UNICODE)


def local_writing_analysis(text: str, min_words: int, max_words: int) -> Dict[str, Any]:
    """Produit des indicateurs objectifs sans prétendre corriger le sens."""

    tokens = words(text)
    count = len(tokens)
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    sentences = [part.strip() for part in re.split(r"[.!?]+", text) if part.strip()]
    unique_ratio = len(set(tokens)) / count if count else 0
    frequencies = Counter(token for token in tokens if len(token) > 4)
    repetitions = [word for word, amount in frequencies.most_common(5) if amount >= 3]
    lowered = text.casefold()
    connectors = sorted(marker for marker in CONNECTORS if marker in lowered)
    hedges = sorted(marker for marker in HEDGES if marker in lowered)
    informal = sorted(marker for marker in INFORMAL_MARKERS if marker in lowered)
    checks = {
        "Length within target": min_words <= count <= max_words,
        "At least 3 paragraphs": len(paragraphs) >= 3,
        "Uses linking language": bool(connectors),
        "Uses calibrated language": bool(hedges),
        "No obvious informal markers": not informal,
    }
    return {
        "word_count": count,
        "paragraph_count": len(paragraphs),
        "sentence_count": len(sentences),
        "lexical_diversity": round(unique_ratio * 100),
        "connectors": connectors,
        "hedges": hedges,
        "informal_markers": informal,
        "repeated_words": repetitions,
        "checks": checks,
    }


FEEDBACK_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "scores": {
            "type": "object",
            "properties": {
                "task_achievement": {"type": "integer", "minimum": 1, "maximum": 5},
                "organisation": {"type": "integer", "minimum": 1, "maximum": 5},
                "grammar": {"type": "integer", "minimum": 1, "maximum": 5},
                "vocabulary": {"type": "integer", "minimum": 1, "maximum": 5},
                "register": {"type": "integer", "minimum": 1, "maximum": 5},
            },
            "required": ["task_achievement", "organisation", "grammar", "vocabulary", "register"],
            "additionalProperties": False,
        },
        "strengths": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 4},
        "priorities": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 4},
        "corrections": {
            "type": "array", "maxItems": 8,
            "items": {
                "type": "object",
                "properties": {
                    "original": {"type": "string"}, "improved": {"type": "string"},
                    "category": {"type": "string"}, "explanation": {"type": "string"},
                },
                "required": ["original", "improved", "category", "explanation"],
                "additionalProperties": False,
            },
        },
        "next_exercise": {"type": "string"},
    },
    "required": ["summary", "scores", "strengths", "priorities", "corrections", "next_exercise"],
    "additionalProperties": False,
}


def evaluate_with_openai(
    api_key: str,
    model: str,
    language: str,
    task: str,
    instructions: List[str],
    draft: str,
) -> Dict[str, Any]:
    """Envoie un brouillon au serveur OpenAI sans conservation applicative."""

    system = (
        "You are a demanding but constructive CEFR C1 writing coach. Evaluate only the submitted text. "
        "Do not invent errors. Distinguish incorrect, unnatural, overly simple, and register-inappropriate wording. "
        "Use the language of the submitted text for feedback. Scores are diagnostic, not an official certification."
    )
    user = "Language: {0}\nTask: {1}\nRequirements:\n- {2}\n\nLearner draft:\n{3}".format(
        language, task, "\n- ".join(instructions), draft
    )
    payload = {
        "model": model,
        "store": False,
        "input": [
            {"role": "developer", "content": system},
            {"role": "user", "content": user},
        ],
        "text": {
            "format": {
                "type": "json_schema", "name": "writing_feedback",
                "strict": True, "schema": FEEDBACK_SCHEMA,
            }
        },
        "max_output_tokens": 2200,
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer {0}".format(api_key), "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError("OpenAI API error ({0}): {1}".format(error.code, detail[:500])) from error
    except (urllib.error.URLError, TimeoutError) as error:
        raise RuntimeError("Unable to reach the OpenAI API: {0}".format(error)) from error

    for item in body.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    return json.loads(content["text"])
    raise RuntimeError("The API returned no structured writing feedback.")


def progress_export(state: Dict[str, Any]) -> str:
    """Sérialise seulement les données pédagogiques explicitement retenues."""

    safe = {
        "version": 1,
        "writing_attempts": state.get("writing_attempts", []),
        "error_notebook": state.get("error_notebook", []),
        "review_cards": state.get("review_cards", []),
    }
    return json.dumps(safe, ensure_ascii=False, indent=2)


def validate_progress_import(data: Any) -> Dict[str, Any]:
    """Valide un export avant de le charger dans la session."""

    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("Unsupported progress file.")
    result: Dict[str, Any] = {}
    for key in ("writing_attempts", "error_notebook", "review_cards"):
        value = data.get(key, [])
        if not isinstance(value, list) or len(value) > 2000:
            raise ValueError("Invalid {0}.".format(key))
        result[key] = value
    return result
