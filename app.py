"""Interface web locale du coach d'anglais professionnel."""

import json
from pathlib import Path
from typing import Dict, List

import streamlit as st

from coach import Feedback, get_feedback
from conjugation import LESSON_DETAILS, LESSONS, exercises_for, is_conjugation_correct
from irregular_verbs import irregulars_for
from vocabulary import VOCABULARY, vocabulary_for


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
        "Practice area", ["Conjugation", "Irregular verbs", "Vocabulary", "Professional English"],
        default="Conjugation", required=True, width="stretch", key="practice_area",
        wrap=True,
    )
    st.sidebar.divider()
    if mode == "Conjugation":
        show_conjugation()
    elif mode == "Irregular verbs":
        show_irregular_verbs()
    elif mode == "Vocabulary":
        show_vocabulary()
    else:
        show_professional_practice()


if __name__ == "__main__":
    main()
