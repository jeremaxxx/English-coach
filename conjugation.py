"""Contenu et correction des leçons de conjugaison bilingues."""

import re
from typing import Dict, List, TypedDict


class Lesson(TypedDict):
    title: str
    family: str
    when: str
    rule: str
    examples: List[str]
    tip: str


class ConjugationExercise(TypedDict):
    language: str
    tense: str
    sentence: str
    infinitive: str
    answers: List[str]
    explanation: str


LESSONS: Dict[str, Dict[str, Lesson]] = {
    "English": {
        "Past simple": {
            "title": "Past simple", "family": "Past",
            "when": "A finished action at a specific or understood moment in the past.",
            "rule": "Affirmative: subject + verb-ed (or irregular form). Negative/question: did + base verb.",
            "examples": ["I called the client yesterday.", "She went to Madrid last week.", "Did they finish on time?"],
            "tip": "Look for markers such as yesterday, last…, …ago and in 2024.",
        },
        "Past continuous": {
            "title": "Past continuous", "family": "Past",
            "when": "An action in progress at a past moment, often interrupted by a shorter action.",
            "rule": "Subject + was/were + verb-ing.",
            "examples": ["I was presenting when she called.", "They were working at 8 p.m."],
            "tip": "The long background action often uses the past continuous; the interruption uses the past simple.",
        },
        "Present perfect": {
            "title": "Present perfect", "family": "Past and present",
            "when": "Past experience or action connected to now; an unfinished period or result visible now.",
            "rule": "Subject + have/has + past participle.",
            "examples": ["I have worked here for three years.", "She has already sent the report."],
            "tip": "Use since for a starting point and for for a duration. Do not use it with a finished date such as yesterday.",
        },
        "Past perfect": {
            "title": "Past perfect", "family": "Past",
            "when": "An action completed before another action or reference point in the past.",
            "rule": "Subject + had + past participle.",
            "examples": ["The meeting had started before I arrived.", "They had not seen the email."],
            "tip": "It clarifies which of two past actions happened first.",
        },
        "Present simple": {
            "title": "Present simple", "family": "Present",
            "when": "Habits, routines, permanent situations and general facts.",
            "rule": "Base verb; add -s/-es with he, she or it. Use do/does for negatives and questions.",
            "examples": ["I manage projects.", "She works in finance.", "Does he travel often?"],
            "tip": "Frequency words such as usually, often and every week are useful clues.",
        },
        "Future with will": {
            "title": "Future with will", "family": "Future",
            "when": "Predictions, spontaneous decisions, offers and promises.",
            "rule": "Subject + will + base verb.",
            "examples": ["I will call you tomorrow.", "I think sales will increase."],
            "tip": "For an existing plan, be going to or the present continuous is often more natural.",
        },
    },
    "Español": {
        "Pretérito indefinido": {
            "title": "Pretérito indefinido", "family": "Pasado",
            "when": "Una acción terminada en un período pasado ya cerrado.",
            "rule": "-AR: é, aste, ó, amos, asteis, aron. -ER/-IR: í, iste, ió, imos, isteis, ieron.",
            "examples": ["Ayer hablé con el cliente.", "El equipo terminó el proyecto."],
            "tip": "Busca marcadores como ayer, anoche, el año pasado o en 2024.",
        },
        "Pretérito imperfecto": {
            "title": "Pretérito imperfecto", "family": "Pasado",
            "when": "Hábitos, descripciones y acciones en desarrollo en el pasado.",
            "rule": "-AR: aba, abas, aba, ábamos, abais, aban. -ER/-IR: ía, ías, ía, íamos, íais, ían.",
            "examples": ["Antes trabajaba en Madrid.", "Mientras hablábamos, sonó el teléfono."],
            "tip": "El imperfecto crea el contexto; el indefinido suele expresar el evento que ocurre dentro de él.",
        },
        "Pretérito perfecto": {
            "title": "Pretérito perfecto", "family": "Pasado y presente",
            "when": "Una acción pasada vinculada al presente o dentro de un período todavía abierto.",
            "rule": "Presente de haber + participio: he, has, ha, hemos, habéis, han + -ado/-ido.",
            "examples": ["Hoy he enviado tres correos.", "¿Has visitado Sevilla alguna vez?"],
            "tip": "En España aparece a menudo con hoy, esta semana, ya, todavía no y alguna vez.",
        },
        "Pluscuamperfecto": {
            "title": "Pluscuamperfecto", "family": "Pasado",
            "when": "Una acción que ocurrió antes de otra acción pasada.",
            "rule": "Imperfecto de haber + participio: había, habías, había, habíamos, habíais, habían.",
            "examples": ["La reunión ya había empezado cuando llegué.", "Nunca habían visto ese informe."],
            "tip": "Es el equivalente de «had + participle» en inglés.",
        },
        "Presente": {
            "title": "Presente", "family": "Presente",
            "when": "Hábitos, hechos, estados actuales y acciones que suceden ahora según el contexto.",
            "rule": "Se elimina -ar/-er/-ir y se añade la terminación correspondiente a la persona.",
            "examples": ["Trabajo en un banco.", "Ella aprende rápido.", "Vivimos en París."],
            "tip": "Presta atención a los cambios irregulares: tengo, puedo, hago, voy…",
        },
        "Futuro simple": {
            "title": "Futuro simple", "family": "Futuro",
            "when": "Predicciones, promesas y acciones futuras; también suposiciones sobre el presente.",
            "rule": "Infinitivo completo + é, ás, á, emos, éis, án.",
            "examples": ["Mañana llamaré al cliente.", "El proyecto terminará en junio."],
            "tip": "Algunos radicales son irregulares: tendr-, podr-, har-, dir-, vendr-.",
        },
    },
}


EXERCISES: List[ConjugationExercise] = [
    {"language":"English","tense":"Past simple","sentence":"Yesterday, I ___ the quarterly report. (finish)","infinitive":"finish","answers":["finished"],"explanation":"Yesterday refers to a completed past period, so use the past simple."},
    {"language":"English","tense":"Past simple","sentence":"She ___ the new supplier last Monday. (meet)","infinitive":"meet","answers":["met"],"explanation":"Meet is irregular: its past simple form is met."},
    {"language":"English","tense":"Past continuous","sentence":"We ___ the results when the director arrived. (discuss)","infinitive":"discuss","answers":["were discussing"],"explanation":"The discussion was already in progress when a shorter action occurred."},
    {"language":"English","tense":"Past continuous","sentence":"At 9 a.m., he ___ to a customer. (speak)","infinitive":"speak","answers":["was speaking"],"explanation":"Use was + -ing for an action in progress at a specific past time."},
    {"language":"English","tense":"Present perfect","sentence":"I ___ in this department since 2022. (work)","infinitive":"work","answers":["have worked"],"explanation":"Since introduces a starting point for a situation continuing until now."},
    {"language":"English","tense":"Present perfect","sentence":"She ___ already ___ the invoice. (send)","infinitive":"send","answers":["has already sent"],"explanation":"Use has + past participle; sent is the irregular participle of send."},
    {"language":"English","tense":"Past perfect","sentence":"By the time I called, they ___ the issue. (resolve)","infinitive":"resolve","answers":["had resolved"],"explanation":"The resolution happened before the later past action, called."},
    {"language":"English","tense":"Past perfect","sentence":"He was nervous because he ___ a presentation before. (never give)","infinitive":"give","answers":["had never given"],"explanation":"Use had + given for an experience before that past moment."},
    {"language":"English","tense":"Present simple","sentence":"My manager ___ every proposal carefully. (review)","infinitive":"review","answers":["reviews"],"explanation":"A routine with a third-person singular subject takes -s."},
    {"language":"English","tense":"Present simple","sentence":"They usually ___ from home on Fridays. (work)","infinitive":"work","answers":["work"],"explanation":"Use the base form with they for a habitual action."},
    {"language":"English","tense":"Future with will","sentence":"I think the market ___ next year. (recover)","infinitive":"recover","answers":["will recover"],"explanation":"Will is commonly used for a prediction."},
    {"language":"English","tense":"Future with will","sentence":"Don't worry, I ___ you with the report. (help)","infinitive":"help","answers":["will help"],"explanation":"Use will for a spontaneous offer or promise."},
    {"language":"Español","tense":"Pretérito indefinido","sentence":"Ayer yo ___ con el director. (hablar)","infinitive":"hablar","answers":["hablé"],"explanation":"Ayer es un período terminado; hablar en primera persona es hablé."},
    {"language":"Español","tense":"Pretérito indefinido","sentence":"El equipo ___ el informe la semana pasada. (hacer)","infinitive":"hacer","answers":["hizo"],"explanation":"Hacer es irregular en indefinido: él/ella hizo."},
    {"language":"Español","tense":"Pretérito imperfecto","sentence":"Antes, nosotros ___ juntos cada día. (trabajar)","infinitive":"trabajar","answers":["trabajábamos"],"explanation":"Antes y cada día describen un hábito pasado; usamos trabajábamos."},
    {"language":"Español","tense":"Pretérito imperfecto","sentence":"Mientras ella ___, llegó un mensaje. (presentar)","infinitive":"presentar","answers":["presentaba"],"explanation":"La presentación era la acción en desarrollo cuando llegó el mensaje."},
    {"language":"Español","tense":"Pretérito perfecto","sentence":"Esta semana nosotros ___ tres contratos. (firmar)","infinitive":"firmar","answers":["hemos firmado"],"explanation":"Esta semana es un período aún abierto: hemos + firmado."},
    {"language":"Español","tense":"Pretérito perfecto","sentence":"¿___ alguna vez a México? (viajar, tú)","infinitive":"viajar","answers":["has viajado"],"explanation":"Alguna vez pregunta por una experiencia hasta el presente: has viajado."},
    {"language":"Español","tense":"Pluscuamperfecto","sentence":"Cuando llegué, la reunión ya ___. (empezar)","infinitive":"empezar","answers":["había empezado"],"explanation":"La reunión empezó antes de que yo llegara: había + participio."},
    {"language":"Español","tense":"Pluscuamperfecto","sentence":"Ellos nunca ___ ese problema antes. (tener)","infinitive":"tener","answers":["habían tenido"],"explanation":"Usamos habían tenido para una experiencia anterior a otro momento pasado."},
    {"language":"Español","tense":"Presente","sentence":"Mi compañera ___ muy bien inglés. (hablar)","infinitive":"hablar","answers":["habla"],"explanation":"En presente, la tercera persona singular de hablar es habla."},
    {"language":"Español","tense":"Presente","sentence":"Nosotros ___ una reunión cada lunes. (tener)","infinitive":"tener","answers":["tenemos"],"explanation":"La primera persona plural del presente de tener es tenemos."},
    {"language":"Español","tense":"Futuro simple","sentence":"Mañana yo ___ al cliente. (llamar)","infinitive":"llamar","answers":["llamaré"],"explanation":"Añadimos -é al infinitivo para la primera persona del futuro."},
    {"language":"Español","tense":"Futuro simple","sentence":"El próximo año ellos ___ más tiempo. (tener)","infinitive":"tener","answers":["tendrán"],"explanation":"Tener usa el radical irregular tendr- en futuro: tendrán."},
]


def normalize_conjugation_answer(text: str) -> str:
    """Normalise la saisie tout en conservant les accents significatifs."""

    text = text.casefold().replace("’", "'")
    text = re.sub(r"[^\wáéíóúüñ']+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def is_conjugation_correct(user_answer: str, accepted_answers: List[str]) -> bool:
    """Vérifie une forme conjuguée contre toutes les réponses acceptées."""

    normalized = normalize_conjugation_answer(user_answer)
    return bool(normalized) and normalized in {
        normalize_conjugation_answer(answer) for answer in accepted_answers
    }


def exercises_for(language: str, tense: str) -> List[ConjugationExercise]:
    """Retourne les exercices correspondant à la langue et au temps choisis."""

    return [
        exercise for exercise in EXERCISES
        if exercise["language"] == language and exercise["tense"] == tense
    ]
