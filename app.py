"""Interface web locale du coach d'anglais professionnel."""

import json
from pathlib import Path
from typing import Dict, List

import streamlit as st

from coach import Feedback, get_feedback


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


def main() -> None:
    """Construit et exécute l'application Streamlit."""

    st.set_page_config(page_title="English Coach", page_icon="💬", layout="centered")
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


if __name__ == "__main__":
    main()
