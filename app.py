"""Interface web locale du coach d'anglais professionnel."""

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

import streamlit as st

from coach import Feedback, get_feedback
from c1_content import ADVANCED_GRAMMAR, WRITING_PROMPTS, advanced_exercises_for, writing_prompts_for
from conjugation import LESSON_DETAILS, LESSONS, exercises_for, is_conjugation_correct
from irregular_verbs import irregulars_for
from vocabulary import VOCABULARY, vocabulary_for
from writing_coach import (
    evaluate_with_openai,
    local_writing_analysis,
    progress_export,
    validate_progress_import,
)


EXERCISES_FILE = Path(__file__).with_name("exercises.json")


@st.cache_data
def load_exercises(path: Path = EXERCISES_FILE) -> List[Dict[str, str]]:
    """Charge et valide les exercices depuis le fichier JSON."""

    with path.open(encoding="utf-8") as file:
        exercises = json.load(file)
    required = {"topic", "prompt", "expected_answer", "explanation"}
    if not isinstance(exercises, list) or not exercises:
        raise ValueError("The exercise file must contain a non-empty list.")
    for exercise in exercises:
        if not isinstance(exercise, dict) or not required.issubset(exercise):
            raise ValueError("An exercise is missing a required field.")
        if not all(isinstance(exercise[field], str) for field in required):
            raise ValueError("Every exercise field must contain text.")
    return exercises


def reset_session(topic_signature: str) -> None:
    """Réinitialise la progression temporaire de la session."""

    st.session_state.exercise_index = 0
    st.session_state.scores = []
    st.session_state.feedback = None
    st.session_state.last_answer = ""
    st.session_state.topic_signature = topic_signature


def show_feedback(feedback: Feedback, exercise: Dict[str, str]) -> None:
    """Affiche le résultat de la réponse courante."""

    score = int(feedback["score"])
    result = "{0} — {1}/100".format(feedback["message"], score)
    if score >= 80:
        st.success(result)
    elif score >= 60:
        st.warning(result)
    else:
        st.error(result)
    st.markdown("#### Model answer")
    st.info(exercise["expected_answer"])
    st.markdown("#### Why?")
    st.write(exercise["explanation"])


def show_professional_practice() -> None:
    """Affiche les exercices d'anglais professionnel historiques."""

    try:
        all_exercises = load_exercises()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        st.error("Unable to load the exercises: {0}".format(error))
        st.stop()

    topics = sorted({exercise["topic"] for exercise in all_exercises})
    st.sidebar.title("Practice settings")
    selected_topics = st.sidebar.multiselect(
        "Topics", topics, default=topics,
        help="Choose one or more professional English themes."
    )
    filtered = [exercise for exercise in all_exercises
                if exercise["topic"] in selected_topics]
    signature = "|".join(selected_topics)
    if ("topic_signature" not in st.session_state
            or st.session_state.topic_signature != signature):
        reset_session(signature)

    st.title("💬 English Coach")
    st.caption("B2 professional English · Local exercises · No AI or external API")
    if not filtered:
        st.warning("Select at least one topic in the sidebar to begin.")
        st.stop()

    completed = len(st.session_state.scores)
    average = round(sum(st.session_state.scores) / completed) if completed else 0
    metric_one, metric_two, metric_three = st.columns(3)
    metric_one.metric("Exercises", "{0}/{1}".format(completed, len(filtered)))
    metric_two.metric("Average", "{0}/100".format(average))
    metric_three.metric("Topics", len(selected_topics))

    index = st.session_state.exercise_index
    if index >= len(filtered):
        st.balloons()
        st.success("Session complete — excellent work!")
        st.write("Your final average is **{0}/100**.".format(average))
        if st.button("Start a new session", type="primary"):
            reset_session(signature)
            st.rerun()
        return

    exercise = filtered[index]
    st.progress(index / len(filtered), text="Progress")
    st.markdown(
        '<div class="exercise-card"><small>EXERCISE {0} OF {1} · {2}</small>'
        '<h3>{3}</h3></div>'.format(index + 1, len(filtered),
                                    exercise["topic"].upper(), exercise["prompt"]),
        unsafe_allow_html=True,
    )

    if st.session_state.feedback is None:
        with st.form("answer_form"):
            answer = st.text_area("Your answer",
                                  placeholder="Write your answer in English…",
                                  height=120)
            submitted = st.form_submit_button("Check my answer", type="primary",
                                               width="stretch")
        if submitted:
            feedback = get_feedback(answer, exercise["expected_answer"])
            st.session_state.feedback = feedback
            st.session_state.last_answer = answer
            st.session_state.scores.append(int(feedback["score"]))
            st.rerun()
    else:
        st.caption("Your answer: {0}".format(st.session_state.last_answer or "(empty)"))
        show_feedback(st.session_state.feedback, exercise)
        if st.button("Next exercise →", type="primary", width="stretch"):
            st.session_state.exercise_index += 1
            st.session_state.feedback = None
            st.session_state.last_answer = ""
            st.rerun()

    if st.sidebar.button("Restart session", width="stretch"):
        reset_session(signature)
        st.rerun()


def reset_conjugation_session(signature: str) -> None:
    """Réinitialise une série d'exercices de conjugaison."""

    st.session_state.conjugation_signature = signature
    st.session_state.conjugation_index = 0
    st.session_state.conjugation_score = 0
    st.session_state.conjugation_answered = False
    st.session_state.conjugation_last_answer = ""


def show_conjugation_lesson(language: str, tense: str) -> None:
    """Affiche la fiche de cours sélectionnée."""

    lesson = LESSONS[language][tense]
    st.subheader(lesson["title"])
    st.caption(lesson["family"])
    with st.container(border=True):
        st.markdown("#### When to use it" if language == "English" else "#### Cuándo se usa")
        st.write(lesson["when"])
        st.markdown("#### Structure" if language == "English" else "#### Formación")
        st.write(lesson["rule"])
    st.markdown("#### Examples" if language == "English" else "#### Ejemplos")
    for example in lesson["examples"]:
        st.markdown("- {0}".format(example))
    st.info(lesson["tip"], icon=":material/lightbulb:")
    details = LESSON_DETAILS[language][tense]
    with st.expander(
        "Go further" if language == "English" else "Profundizar",
        icon=":material/school:",
    ):
        st.markdown("**Signal words**" if language == "English" else "**Marcadores**")
        st.write(details["signals"])
        st.markdown("**Common mistake**" if language == "English" else "**Error frecuente**")
        st.write(details["pitfall"])
        st.markdown("**Key contrast**" if language == "English" else "**Contraste clave**")
        st.write(details["contrast"])


def show_conjugation_practice(language: str, tense: str) -> None:
    """Affiche une série courte avec correction immédiate."""

    exercises = exercises_for(language, tense)
    signature = "{0}|{1}".format(language, tense)
    if st.session_state.get("conjugation_signature") != signature:
        reset_conjugation_session(signature)

    index = st.session_state.conjugation_index
    total = len(exercises)
    if index >= total:
        score = st.session_state.conjugation_score
        st.success("Series complete: {0}/{1} correct answers.".format(score, total))
        st.progress(score / total if total else 0, text="Final score")
        if st.button("Practise again", type="primary", width="stretch"):
            reset_conjugation_session(signature)
            st.rerun()
        return

    exercise = exercises[index]
    st.progress(index / total, text="Exercise {0} of {1}".format(index + 1, total))
    score_col, tense_col = st.columns(2)
    score_col.metric("Correct answers", st.session_state.conjugation_score)
    tense_col.metric("Tense", tense)

    with st.container(border=True):
        st.caption("VERB · {0}".format(exercise["infinitive"]))
        st.subheader(exercise["sentence"])

    if not st.session_state.conjugation_answered:
        with st.form("conjugation_answer_form"):
            answer = st.text_input(
                "Your answer" if language == "English" else "Tu respuesta",
                placeholder="Type only the missing verb form…" if language == "English"
                else "Escribe solo la forma verbal que falta…",
            )
            submitted = st.form_submit_button(
                "Check answer" if language == "English" else "Comprobar",
                type="primary", width="stretch",
            )
        if submitted:
            correct = is_conjugation_correct(answer, exercise["answers"])
            st.session_state.conjugation_answered = True
            st.session_state.conjugation_last_answer = answer
            st.session_state.conjugation_was_correct = correct
            if correct:
                st.session_state.conjugation_score += 1
            st.rerun()
    else:
        if st.session_state.conjugation_was_correct:
            st.success("Correct!", icon=":material/check_circle:")
        else:
            st.error(
                "Not quite. Correct answer: **{0}**".format(exercise["answers"][0]),
                icon=":material/cancel:",
            )
            st.caption("Your answer: {0}".format(
                st.session_state.conjugation_last_answer or "(empty)"
            ))
        st.write(exercise["explanation"])
        if st.button(
            "Next exercise" if language == "English" else "Siguiente ejercicio",
            type="primary", width="stretch",
        ):
            st.session_state.conjugation_index += 1
            st.session_state.conjugation_answered = False
            st.session_state.conjugation_last_answer = ""
            st.rerun()


def show_conjugation() -> None:
    """Affiche les cours et exercices de conjugaison bilingues."""

    st.title("Conjugation trainer")
    st.caption("Learn the rule, study examples, then practise without external APIs.")
    language = st.sidebar.segmented_control(
        "Language", ["English", "Español"], default="English", required=True,
        width="stretch", key="conjugation_language",
    )
    tenses = list(LESSONS[language])
    tense = st.sidebar.selectbox("Tense / Tiempo", tenses)
    section = st.segmented_control(
        "Learning mode", ["Course", "Exercises"], default="Course", required=True,
        width="stretch", key="conjugation_section",
    )
    if section == "Course":
        show_conjugation_lesson(language, tense)
    else:
        show_conjugation_practice(language, tense)


def split_accepted_answers(value: str) -> List[str]:
    """Transforme une cellule contenant plusieurs variantes en réponses."""

    answers = [item.strip() for item in value.split(" / ")]
    return answers + [value]


def reset_quiz(prefix: str, signature: str) -> None:
    """Initialise l'état partagé par les quiz simples."""

    st.session_state["{0}_signature".format(prefix)] = signature
    st.session_state["{0}_index".format(prefix)] = 0
    st.session_state["{0}_score".format(prefix)] = 0
    st.session_state["{0}_answered".format(prefix)] = False
    st.session_state["{0}_answer".format(prefix)] = ""


def show_irregular_directory(language: str) -> None:
    """Affiche un répertoire filtrable des formes irrégulières."""

    rows = irregulars_for(language)
    search = st.text_input(
        "Search a verb or meaning" if language == "English"
        else "Buscar un verbo o significado",
        placeholder="write, écrire…" if language == "English" else "hacer, faire…",
    ).casefold().strip()
    if search:
        rows = [row for row in rows if any(search in value.casefold() for value in row.values())]
    st.caption("{0} verbs".format(len(rows)))
    st.dataframe(rows, hide_index=True, width="stretch")


def show_irregular_quiz(language: str) -> None:
    """Demande une forme irrégulière et donne une correction immédiate."""

    rows = irregulars_for(language)
    fields = (["Past simple", "Past participle"] if language == "English"
              else ["Presente (yo)", "Indefinido (yo)", "Participio", "Futuro (yo)"])
    signature = language
    if st.session_state.get("irregular_signature") != signature:
        reset_quiz("irregular", signature)
    index = st.session_state.irregular_index
    if index >= len(rows):
        st.success("Complete! Score: {0}/{1}.".format(st.session_state.irregular_score, len(rows)))
        if st.button("Start again", type="primary", width="stretch", key="irregular_restart"):
            reset_quiz("irregular", signature)
            st.rerun()
        return

    row = rows[index]
    field = fields[index % len(fields)]
    infinitive_key = "Infinitive" if language == "English" else "Infinitivo"
    expected = row[field]
    st.progress(index / len(rows), text="Verb {0} of {1}".format(index + 1, len(rows)))
    with st.container(border=True):
        st.caption(row["Français"])
        st.subheader(row[infinitive_key])
        st.write("Form requested: **{0}**".format(field))
    if not st.session_state.irregular_answered:
        with st.form("irregular_form"):
            answer = st.text_input("Your answer" if language == "English" else "Tu respuesta")
            submitted = st.form_submit_button("Check", type="primary", width="stretch")
        if submitted:
            correct = is_conjugation_correct(answer, split_accepted_answers(expected))
            st.session_state.irregular_answered = True
            st.session_state.irregular_answer = answer
            st.session_state.irregular_correct = correct
            if correct:
                st.session_state.irregular_score += 1
            st.rerun()
    else:
        if st.session_state.irregular_correct:
            st.success("Correct!", icon=":material/check_circle:")
        else:
            st.error("Correct form: **{0}**".format(expected), icon=":material/cancel:")
        if st.button("Next verb", type="primary", width="stretch", key="irregular_next"):
            st.session_state.irregular_index += 1
            st.session_state.irregular_answered = False
            st.rerun()


def show_irregular_verbs() -> None:
    """Affiche l'espace de référence et d'entraînement des irréguliers."""

    st.title("Irregular verbs")
    st.caption("Study the essential forms, then retrieve them from memory.")
    language = st.sidebar.segmented_control(
        "Language", ["English", "Español"], default="English", required=True,
        width="stretch", key="irregular_language",
    )
    section = st.segmented_control(
        "Mode", ["Reference", "Quiz"], default="Reference", required=True,
        width="stretch", key="irregular_section",
    )
    if section == "Reference":
        show_irregular_directory(language)
    else:
        show_irregular_quiz(language)


def show_vocabulary_reference(language: str, categories: List[str]) -> None:
    """Affiche le lexique trilingue sélectionné."""

    rows = vocabulary_for(language, categories)
    search = st.text_input("Search the vocabulary", placeholder="beneficiary, presupuesto…").casefold().strip()
    if search:
        rows = [row for row in rows if any(search in str(value).casefold() for value in row.values())]
    display_rows = [
        {"Theme": row["category"], "Français": row["Français"], language: row[language]}
        for row in rows
    ]
    st.caption("{0} expressions".format(len(display_rows)))
    st.dataframe(display_rows, hide_index=True, width="stretch")


def show_vocabulary_quiz(language: str, categories: List[str], direction: str) -> None:
    """Fait traduire le vocabulaire choisi dans les deux directions."""

    rows = vocabulary_for(language, categories)
    signature = "|".join([language, direction] + categories)
    if st.session_state.get("vocabulary_signature") != signature:
        reset_quiz("vocabulary", signature)
    index = st.session_state.vocabulary_index
    if index >= len(rows):
        st.success("Complete! Score: {0}/{1}.".format(st.session_state.vocabulary_score, len(rows)))
        if st.button("Start again", type="primary", width="stretch", key="vocabulary_restart"):
            reset_quiz("vocabulary", signature)
            st.rerun()
        return
    row = rows[index]
    source = "Français" if direction == "French → target language" else language
    target = language if source == "Français" else "Français"
    expected = row[target]
    st.progress(index / len(rows), text="Word {0} of {1}".format(index + 1, len(rows)))
    with st.container(border=True):
        st.caption("{0} · translate into {1}".format(row["category"], target))
        st.subheader(row[source])
    if not st.session_state.vocabulary_answered:
        with st.form("vocabulary_form"):
            answer = st.text_input("Translation")
            submitted = st.form_submit_button("Check", type="primary", width="stretch")
        if submitted:
            correct = is_conjugation_correct(answer, split_accepted_answers(expected))
            st.session_state.vocabulary_answered = True
            st.session_state.vocabulary_answer = answer
            st.session_state.vocabulary_correct = correct
            if correct:
                st.session_state.vocabulary_score += 1
            st.rerun()
    else:
        if st.session_state.vocabulary_correct:
            st.success("Correct!", icon=":material/check_circle:")
        else:
            st.error("Expected answer: **{0}**".format(expected), icon=":material/cancel:")
        if st.button("Next word", type="primary", width="stretch", key="vocabulary_next"):
            st.session_state.vocabulary_index += 1
            st.session_state.vocabulary_answered = False
            st.rerun()


def show_vocabulary() -> None:
    """Affiche le lexique professionnel et quotidien avec quiz."""

    st.title("Vocabulary")
    st.caption("Work, humanitarian aid and everyday life—in English and Spanish.")
    language = st.sidebar.segmented_control(
        "Target language", ["English", "Español"], default="English", required=True,
        width="stretch", key="vocabulary_language",
    )
    all_categories = list(dict.fromkeys(row["category"] for row in VOCABULARY))
    categories = st.sidebar.multiselect(
        "Themes", all_categories, default=all_categories, key="vocabulary_categories",
    )
    if not categories:
        st.warning("Select at least one theme.")
        return
    section = st.segmented_control(
        "Mode", ["Reference", "Quiz"], default="Reference", required=True,
        width="stretch", key="vocabulary_section",
    )
    if section == "Reference":
        show_vocabulary_reference(language, categories)
    else:
        direction = st.selectbox(
            "Direction", ["French → target language", "Target language → French"]
        )
        show_vocabulary_quiz(language, categories, direction)


def initialise_c1_state() -> None:
    """Initialise les données privées à la session du navigateur."""

    st.session_state.setdefault("writing_attempts", [])
    st.session_state.setdefault("error_notebook", [])
    st.session_state.setdefault("review_cards", [])
    st.session_state.setdefault("writing_draft", "")
    st.session_state.setdefault("writing_revision", "")
    st.session_state.setdefault("writing_local_feedback", None)
    st.session_state.setdefault("writing_ai_feedback", None)
    st.session_state.setdefault("writing_prompt_id", "")
    st.session_state.setdefault("api_calls_this_session", 0)


def configured_openai() -> Dict[str, Any]:
    """Lit les secrets serveur sans échouer quand aucun secret n'existe."""

    try:
        key = str(st.secrets.get("OPENAI_API_KEY", ""))
        model = str(st.secrets.get("OPENAI_MODEL", "gpt-5.6-luna"))
        allowed = [str(email).casefold() for email in st.secrets.get("OPENAI_ALLOWED_EMAILS", [])]
        max_calls = max(0, min(50, int(st.secrets.get("OPENAI_MAX_CALLS_PER_SESSION", 10))))
    except Exception:
        key, model, allowed, max_calls = "", "gpt-5.6-luna", [], 10
    return {"key": key, "model": model, "allowed": allowed, "max_calls": max_calls}


def api_user_is_allowed(api: Dict[str, Any]) -> bool:
    """Applique l'allowlist côté serveur lorsqu'elle est configurée."""

    if not api["allowed"]:
        return True
    try:
        email = str(st.user.get("email", "")).casefold()
    except Exception:
        email = ""
    return bool(email) and email in api["allowed"]


def show_local_writing_feedback(feedback: Dict[str, Any], minimum: int, maximum: int) -> None:
    """Présente les indicateurs vérifiables calculés sans IA."""

    cols = st.columns(4)
    cols[0].metric("Words", "{0}/{1}–{2}".format(feedback["word_count"], minimum, maximum))
    cols[1].metric("Paragraphs", feedback["paragraph_count"])
    cols[2].metric("Sentences", feedback["sentence_count"])
    cols[3].metric("Lexical variety", "{0}%".format(feedback["lexical_diversity"]))
    for label, passed in feedback["checks"].items():
        st.write(":material/check_circle: {0}".format(label) if passed else ":material/warning: {0}".format(label))
    if feedback["repeated_words"]:
        st.warning("Repeated content words: {0}".format(", ".join(feedback["repeated_words"])))
    st.caption("This local analysis measures form only; it does not judge meaning or grammatical accuracy.")


def show_ai_writing_feedback(feedback: Dict[str, Any]) -> None:
    """Affiche la grille C1 structurée reçue de l'API."""

    st.subheader("C1 diagnostic")
    labels = {
        "task_achievement": "Task", "organisation": "Organisation", "grammar": "Grammar",
        "vocabulary": "Vocabulary", "register": "Register",
    }
    score_cols = st.columns(5)
    for column, (key, label) in zip(score_cols, labels.items()):
        column.metric(label, "{0}/5".format(feedback["scores"][key]))
    st.write(feedback["summary"])
    left, right = st.columns(2)
    with left.container(border=True, height="stretch"):
        st.markdown("#### Strengths")
        for strength in feedback["strengths"]:
            st.markdown("- {0}".format(strength))
    with right.container(border=True, height="stretch"):
        st.markdown("#### Priorities")
        for priority in feedback["priorities"]:
            st.markdown("- {0}".format(priority))
    if feedback["corrections"]:
        st.markdown("#### Corrections to study")
        for correction in feedback["corrections"]:
            with st.expander(correction["category"] + " · " + correction["original"][:60]):
                st.write("**Original:** {0}".format(correction["original"]))
                st.write("**Improved:** {0}".format(correction["improved"]))
                st.write(correction["explanation"])
    st.info("Next targeted exercise: {0}".format(feedback["next_exercise"]), icon=":material/target:")


def save_writing_attempt(prompt: Dict[str, Any], self_scores: Dict[str, int]) -> None:
    """Enregistre le travail et transforme les corrections en cartes de révision."""

    ai_feedback = st.session_state.get("writing_ai_feedback")
    attempt = {
        "prompt_id": prompt["id"], "title": prompt["title"], "language": prompt["language"],
        "kind": prompt["kind"], "draft": st.session_state.writing_draft,
        "revision": st.session_state.writing_revision, "self_scores": self_scores,
        "ai_scores": ai_feedback.get("scores", {}) if ai_feedback else {},
    }
    st.session_state.writing_attempts.append(attempt)
    if ai_feedback:
        existing = {(item.get("original"), item.get("improved")) for item in st.session_state.error_notebook}
        for correction in ai_feedback["corrections"]:
            pair = (correction["original"], correction["improved"])
            if pair not in existing:
                card = {**correction, "box": 1, "reviews": 0}
                st.session_state.error_notebook.append(card)
                st.session_state.review_cards.append(card.copy())


def show_writing_lab() -> None:
    """Guide une production, son évaluation et sa réécriture."""

    language = st.sidebar.segmented_control(
        "Writing language", ["English", "Español"], default="English", required=True,
        width="stretch", key="writing_language",
    )
    kinds = ["All"] + list(dict.fromkeys(p["kind"] for p in WRITING_PROMPTS if p["language"] == language))
    kind = st.sidebar.selectbox("Task type", kinds, key="writing_kind")
    prompts = writing_prompts_for(language, kind)
    selected_title = st.selectbox("Choose a task", [p["title"] for p in prompts], key="writing_prompt_title")
    prompt = next(p for p in prompts if p["title"] == selected_title)
    if st.session_state.writing_prompt_id != prompt["id"]:
        st.session_state.writing_prompt_id = prompt["id"]
        st.session_state.writing_draft = ""
        st.session_state.writing_revision = ""
        st.session_state.writing_local_feedback = None
        st.session_state.writing_ai_feedback = None
        st.session_state.writing_saved = False

    with st.container(border=True):
        st.caption("{0} · {1}–{2} words".format(prompt["kind"], prompt["min_words"], prompt["max_words"]))
        st.subheader(prompt["title"])
        st.write(prompt["scenario"])
        for instruction in prompt["instructions"]:
            st.markdown("- {0}".format(instruction))
        st.caption("Focus: {0}".format(" · ".join(prompt["focus"])))

    with st.form("writing_draft_form"):
        draft = st.text_area(
            "First draft", value=st.session_state.writing_draft, height=300,
            placeholder="Write independently before requesting feedback…",
            key="writing_draft_" + prompt["id"],
        )
        submitted = st.form_submit_button("Analyse my draft", type="primary", width="stretch")
    if submitted:
        if len(draft.strip()) < 40:
            st.error("Write a more substantial draft before requesting analysis.")
        else:
            st.session_state.writing_draft = draft
            st.session_state.writing_local_feedback = local_writing_analysis(
                draft, prompt["min_words"], prompt["max_words"]
            )
            st.session_state.writing_revision = draft
            st.rerun()

    if not st.session_state.writing_local_feedback:
        return
    st.divider()
    st.subheader("Immediate local feedback")
    show_local_writing_feedback(
        st.session_state.writing_local_feedback, prompt["min_words"], prompt["max_words"]
    )

    api = configured_openai()
    if api["key"] and api_user_is_allowed(api):
        with st.container(border=True):
            st.markdown("#### Optional AI evaluation")
            st.caption(
                "Your draft will be sent from the Streamlit server to the OpenAI API. "
                "It is not shown to other app users. Avoid confidential or personal data."
            )
            consent = st.checkbox(
                "I agree to send this draft for evaluation",
                key="writing_api_consent_" + prompt["id"],
            )
            remaining = max(0, api["max_calls"] - st.session_state.api_calls_this_session)
            st.caption("{0} AI evaluations remaining in this browser session.".format(remaining))
            if st.button("Request C1 evaluation", disabled=not consent or remaining == 0):
                with st.spinner("Evaluating the text…"):
                    try:
                        st.session_state.writing_ai_feedback = evaluate_with_openai(
                            api["key"], api["model"], prompt["language"], prompt["scenario"],
                            prompt["instructions"], st.session_state.writing_draft,
                        )
                        st.session_state.api_calls_this_session += 1
                        st.rerun()
                    except RuntimeError as error:
                        st.error(str(error))
    elif api["key"]:
        st.warning("AI evaluation is not enabled for your signed-in email address.", icon=":material/lock:")
    else:
        st.info(
            "AI evaluation is disabled. Add OPENAI_API_KEY to Streamlit secrets to enable it; "
            "the local writing workflow remains fully usable.",
            icon=":material/lock:",
        )
    if st.session_state.writing_ai_feedback:
        show_ai_writing_feedback(st.session_state.writing_ai_feedback)

    st.divider()
    st.subheader("Rewrite")
    st.write("Revise the text using the feedback above. Do not copy the model answer yet.")
    revision = st.text_area(
        "Second version", value=st.session_state.writing_revision,
        height=300, key="writing_revision_widget_" + prompt["id"],
    )
    rubric_labels = ["Task achievement", "Organisation", "Grammar", "Vocabulary", "Register"]
    self_scores = {
        label: st.slider(
            label, 1, 5, 3,
            key="self_{0}_{1}".format(prompt["id"], label.lower().replace(" ", "_")),
        )
        for label in rubric_labels
    }
    if st.button("Save revision and reveal model", type="primary", width="stretch"):
        if revision.strip() == st.session_state.writing_draft.strip():
            st.warning("Make at least one change before saving the revision.")
        else:
            st.session_state.writing_revision = revision
            save_writing_attempt(prompt, self_scores)
            st.session_state.writing_saved = True
            st.rerun()
    if st.session_state.get("writing_saved"):
        st.success("Revision saved. Compare structure and choices—not exact wording.")
        with st.expander("Model C1 answer", expanded=True, icon=":material/menu_book:"):
            st.write(prompt["model_answer"])


def reset_advanced_grammar(language: str) -> None:
    st.session_state.advanced_language = language
    st.session_state.advanced_index = 0
    st.session_state.advanced_score = 0
    st.session_state.advanced_answered = False


def show_advanced_grammar() -> None:
    """Entraîne les structures qui distinguent souvent B2 et C1."""

    language = st.sidebar.segmented_control(
        "Language", ["English", "Español"], default="English", required=True,
        width="stretch", key="advanced_grammar_language",
    )
    exercises = advanced_exercises_for(language)
    if st.session_state.get("advanced_language") != language:
        reset_advanced_grammar(language)
    index = st.session_state.advanced_index
    if index >= len(exercises):
        st.success("Series complete: {0}/{1}.".format(st.session_state.advanced_score, len(exercises)))
        if st.button("Practise again", type="primary"):
            reset_advanced_grammar(language)
            st.rerun()
        return
    exercise = exercises[index]
    st.progress(index / len(exercises), text="{0} of {1}".format(index + 1, len(exercises)))
    with st.container(border=True):
        st.caption(exercise["topic"])
        st.subheader(exercise["prompt"])
    if not st.session_state.advanced_answered:
        with st.form("advanced_grammar_form"):
            answer = st.text_input("Your answer")
            submit = st.form_submit_button("Check", type="primary", width="stretch")
        if submit:
            correct = is_conjugation_correct(answer, exercise["answers"])
            st.session_state.advanced_answered = True
            st.session_state.advanced_correct = correct
            if correct:
                st.session_state.advanced_score += 1
            st.rerun()
    else:
        if st.session_state.advanced_correct:
            st.success("Correct!")
        else:
            st.error("Suggested answer: **{0}**".format(exercise["answers"][0]))
        st.write(exercise["explanation"])
        if st.button("Next", type="primary", width="stretch", key="advanced_next"):
            st.session_state.advanced_index += 1
            st.session_state.advanced_answered = False
            st.rerun()


def show_error_notebook() -> None:
    """Affiche, enrichit et révise le carnet d'erreurs personnel."""

    with st.form("manual_error_form"):
        st.markdown("#### Add an error manually")
        category = st.selectbox("Category", ["Grammar", "Vocabulary", "Register", "Cohesion", "Spelling"])
        original = st.text_input("Original wording")
        improved = st.text_input("Corrected wording")
        explanation = st.text_input("Rule or explanation")
        add = st.form_submit_button("Add to notebook")
    if add and original.strip() and improved.strip():
        item = {"category": category, "original": original, "improved": improved,
                "explanation": explanation, "box": 1, "reviews": 0}
        st.session_state.error_notebook.append(item)
        st.session_state.review_cards.append(item.copy())
        st.rerun()

    if not st.session_state.error_notebook:
        st.info("Your errors will appear here after an AI evaluation or manual entry.")
        return
    st.dataframe(st.session_state.error_notebook, hide_index=True, width="stretch")
    cards = st.session_state.review_cards
    if not cards:
        return
    card_index = st.session_state.get("review_index", 0) % len(cards)
    card = cards[card_index]
    st.subheader("Spaced review")
    with st.container(border=True):
        st.caption(card.get("category", "Review"))
        st.write("Improve this: **{0}**".format(card["original"]))
        reveal = st.toggle("Reveal correction", key="review_reveal")
        if reveal:
            st.success(card["improved"])
            st.write(card.get("explanation", ""))
    if reveal:
        with st.container(horizontal=True):
            if st.button("Again", key="review_again"):
                card["box"] = 1
                card["reviews"] = card.get("reviews", 0) + 1
                st.session_state.review_index = card_index + 1
                st.rerun()
            if st.button("Hard", key="review_hard"):
                card["box"] = max(1, int(card.get("box", 1)))
                card["reviews"] = card.get("reviews", 0) + 1
                st.session_state.review_index = card_index + 1
                st.rerun()
            if st.button("Good", type="primary", key="review_good"):
                card["box"] = min(5, int(card.get("box", 1)) + 1)
                card["reviews"] = card.get("reviews", 0) + 1
                st.session_state.review_index = card_index + 1
                st.rerun()


def show_c1_progress() -> None:
    """Présente la progression et permet un export/import local."""

    attempts = st.session_state.writing_attempts
    errors = st.session_state.error_notebook
    reviewed = sum(int(card.get("reviews", 0)) for card in st.session_state.review_cards)
    cols = st.columns(3)
    cols[0].metric("Writing tasks", len(attempts))
    cols[1].metric("Errors collected", len(errors))
    cols[2].metric("Card reviews", reviewed)
    if attempts:
        score_totals: Dict[str, List[int]] = {}
        for attempt in attempts:
            source = attempt.get("ai_scores") or {
                key.lower().replace(" ", "_"): value
                for key, value in attempt.get("self_scores", {}).items()
            }
            for key, value in source.items():
                score_totals.setdefault(key, []).append(int(value))
        averages = {
            key: sum(values) / len(values) for key, values in score_totals.items() if values
        }
        if averages:
            weakest = min(averages, key=averages.get)
            recommendations = {
                "task_achievement": "Choose a synthesis or report and check every instruction before writing.",
                "organisation": "Practise paragraph plans and advanced linking language.",
                "grammar": "Complete the Advanced grammar series, then rewrite one previous text.",
                "vocabulary": "Review collocations and replace repeated general verbs with precise alternatives.",
                "register": "Choose a professional email or B2-to-C1 reformulation task.",
            }
            st.info(
                "Adaptive recommendation · weakest area: **{0}** ({1:.1f}/5). {2}".format(
                    weakest.replace("_", " "), averages[weakest], recommendations.get(weakest, "Review this area in your next task.")
                ),
                icon=":material/route:",
            )
        st.dataframe([
            {"Task": item["title"], "Language": item["language"], "Type": item["kind"],
             "Self score": sum(item["self_scores"].values()),
             "AI score": sum(item.get("ai_scores", {}).values()) or None}
            for item in attempts
        ], hide_index=True, width="stretch")
    st.download_button(
        "Download my private progress", progress_export(dict(st.session_state)),
        file_name="language-coach-progress.json", mime="application/json",
        icon=":material/download:",
    )
    uploaded = st.file_uploader("Restore a progress file", type=["json"], key="progress_upload")
    if uploaded and st.button("Restore progress"):
        try:
            imported = validate_progress_import(json.loads(uploaded.getvalue().decode("utf-8")))
            for key, value in imported.items():
                st.session_state[key] = value
            st.success("Progress restored.")
            st.rerun()
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as error:
            st.error("Invalid progress file: {0}".format(error))


DOCUMENT_STOPWORDS = {
    "about", "after", "again", "avec", "avoir", "comme", "dans", "para", "pero", "porque",
    "esta", "este", "that", "their", "there", "these", "they", "this", "those", "would",
    "from", "have", "with", "your", "pour", "plus", "nous", "vous", "elle", "elles", "sont",
}


def show_document_lab() -> None:
    """Extrait localement des candidats lexicaux de documents non sensibles."""

    st.subheader("Document vocabulary lab")
    st.write("Upload a `.txt` or `.csv` document. It is processed in memory and is not sent to an AI service.")
    upload = st.file_uploader("Professional document", type=["txt", "csv"], key="document_upload")
    if not upload:
        return
    try:
        text = upload.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        st.error("The document must use UTF-8 encoding.")
        return
    tokens = [
        token.casefold() for token in re.findall(r"[^\W\d_]{5,}", text, re.UNICODE)
        if token.casefold() not in DOCUMENT_STOPWORDS
    ]
    rows = [{"Candidate term": word, "Occurrences": count}
            for word, count in Counter(tokens).most_common(60)]
    st.dataframe(rows, hide_index=True, width="stretch")
    st.caption("Review these candidates manually before adding them to the learning corpus.")


def show_c1_workshop() -> None:
    """Point d'entrée du parcours d'écrit C1."""

    initialise_c1_state()
    st.title("C1 writing workshop")
    st.caption("Write, receive evidence-based feedback, rewrite, and review your recurring errors.")
    section = st.segmented_control(
        "C1 workspace",
        ["Writing lab", "Advanced grammar", "Error notebook", "Progress", "Documents"],
        default="Writing lab", required=True, width="stretch", wrap=True, key="c1_section",
    )
    if section == "Writing lab":
        show_writing_lab()
    elif section == "Advanced grammar":
        show_advanced_grammar()
    elif section == "Error notebook":
        show_error_notebook()
    elif section == "Progress":
        show_c1_progress()
    else:
        show_document_lab()


def main() -> None:
    """Construit et exécute l'application Streamlit."""

    st.set_page_config(page_title="Language Coach", page_icon="💬", layout="centered")
    st.markdown(
        """
        <style>
        .block-container {max-width: 850px; padding-top: 2rem;}
        [data-testid="stMetric"] {background: rgba(49,51,63,.06); border: 1px solid
        rgba(49,51,63,.14); border-radius: 14px; padding: .8rem 1rem;}
        .exercise-card {border: 1px solid rgba(49,51,63,.16); border-radius: 18px;
        padding: 1.3rem 1.5rem; margin: 1rem 0; background: rgba(255,255,255,.025);}
        </style>
        """,
        unsafe_allow_html=True,
    )
    mode = st.sidebar.segmented_control(
        "Practice area", ["C1 Writing", "Conjugation", "Irregular verbs", "Vocabulary", "Professional English"],
        default="C1 Writing", required=True, width="stretch", key="practice_area",
        wrap=True,
    )
    st.sidebar.divider()
    if mode == "C1 Writing":
        show_c1_workshop()
    elif mode == "Conjugation":
        show_conjugation()
    elif mode == "Irregular verbs":
        show_irregular_verbs()
    elif mode == "Vocabulary":
        show_vocabulary()
    else:
        show_professional_practice()


if __name__ == "__main__":
    main()
