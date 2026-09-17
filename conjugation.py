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


# Temps complémentaires : ils gardent la même structure que les fiches initiales.
LESSONS["English"].update({
    "Present continuous": {
        "title": "Present continuous", "family": "Present",
        "when": "An action happening now, a temporary situation or a changing trend.",
        "rule": "Subject + am/is/are + verb-ing.",
        "examples": ["I am reviewing the file now.", "Costs are increasing."],
        "tip": "State verbs such as know, believe and need are not normally used in the continuous.",
    },
    "Going to": {
        "title": "Future with be going to", "family": "Future",
        "when": "A prior intention or a prediction based on present evidence.",
        "rule": "Subject + am/is/are going to + base verb.",
        "examples": ["We are going to recruit two people.", "Look at those clouds—it is going to rain."],
        "tip": "Unlike will, going to usually signals that the plan already exists.",
    },
    "Future continuous": {
        "title": "Future continuous", "family": "Future",
        "when": "An action that will be in progress at a particular future time.",
        "rule": "Subject + will be + verb-ing.",
        "examples": ["This time tomorrow, I will be flying.", "We will be working at 10 a.m."],
        "tip": "Use it to place the listener inside a future action in progress.",
    },
    "Future perfect": {
        "title": "Future perfect", "family": "Future",
        "when": "An action that will be completed before a future deadline.",
        "rule": "Subject + will have + past participle.",
        "examples": ["By Friday, we will have finished.", "She will have left by noon."],
        "tip": "By + future time is a strong clue for the future perfect.",
    },
})

LESSONS["Español"].update({
    "Presente progresivo": {
        "title": "Presente progresivo", "family": "Presente",
        "when": "Una acción que está ocurriendo en el momento de hablar.",
        "rule": "Presente de estar + gerundio (-ando, -iendo).",
        "examples": ["Estoy revisando el informe.", "Estamos preparando la distribución."],
        "tip": "Se usa menos que el present continuous inglés; el presente simple también puede expresar una acción actual.",
    },
    "Ir a + infinitivo": {
        "title": "Futuro con ir a", "family": "Futuro",
        "when": "Planes, intenciones y predicciones basadas en indicios presentes.",
        "rule": "Presente de ir + a + infinitivo.",
        "examples": ["Vamos a contratar a dos personas.", "Va a llover."],
        "tip": "Es muy frecuente en la conversación para hablar de planes próximos.",
    },
    "Condicional simple": {
        "title": "Condicional simple", "family": "Condicional",
        "when": "Hipótesis, deseos y peticiones corteses.",
        "rule": "Infinitivo + ía, ías, ía, íamos, íais, ían.",
        "examples": ["Me gustaría ayudarte.", "Con más tiempo, terminaríamos hoy."],
        "tip": "Los radicales irregulares coinciden con los del futuro: tendría, podría, haría…",
    },
    "Presente de subjuntivo": {
        "title": "Presente de subjuntivo", "family": "Subjuntivo",
        "when": "Deseos, dudas, emociones, recomendaciones y finalidad tras ciertas expresiones.",
        "rule": "Se parte de la forma yo del presente, se quita -o y se añaden terminaciones opuestas: -e para -AR, -a para -ER/-IR.",
        "examples": ["Quiero que vengas.", "Es importante que terminemos hoy."],
        "tip": "Dos sujetos unidos por que suelen ser la señal: quiero que tú vengas.",
    },
})


LESSON_DETAILS: Dict[str, Dict[str, Dict[str, str]]] = {
    "English": {
        "Past simple": {"signals":"yesterday, last…, …ago, in + finished year","pitfall":"After did/didn't, use the base form: Did you go?","contrast":"Past simple closes the event; present perfect connects it to now."},
        "Past continuous": {"signals":"while, as, at 8 p.m., when","pitfall":"Use were with you/we/they and was with I/he/she/it.","contrast":"Past continuous is the background; past simple is often the interrupting event."},
        "Present perfect": {"signals":"already, yet, ever, never, just, since, for, so far","pitfall":"Do not combine it with a finished time: say I went yesterday.","contrast":"Present perfect focuses on present relevance; past simple focuses on when it happened."},
        "Past perfect": {"signals":"by the time, already, before, after","pitfall":"Do not use it for every past action—only when the earlier sequence needs clarification.","contrast":"Past perfect marks the earlier action; past simple usually marks the later one."},
        "Present simple": {"signals":"always, usually, often, sometimes, never, every…","pitfall":"Remember third-person -s and do/does + base form.","contrast":"Use present continuous for something temporary or happening now."},
        "Future with will": {"signals":"I think, probably, perhaps, I promise","pitfall":"Never add to after will: will go, not will to go.","contrast":"Use going to for prior intentions or evidence-based predictions."},
        "Present continuous": {"signals":"now, right now, at the moment, currently","pitfall":"Avoid continuous forms with most state verbs: know, want, believe, own.","contrast":"Present simple is regular/permanent; present continuous is current/temporary."},
        "Going to": {"signals":"plan, intend, look!, evidence visible now","pitfall":"Conjugate be: I am, she is, they are going to.","contrast":"Going to signals an existing intention; will can be a decision made now."},
        "Future continuous": {"signals":"this time tomorrow, at + future time","pitfall":"The form is will be working, never will being work.","contrast":"Future simple states an event; future continuous views it in progress."},
        "Future perfect": {"signals":"by Friday, by then, before + future point","pitfall":"Use the past participle after will have.","contrast":"Future perfect looks back from a future deadline at a completed action."},
    },
    "Español": {
        "Pretérito indefinido": {"signals":"ayer, anoche, el año pasado, en 2024, de repente","pitfall":"Muchos verbos frecuentes cambian de raíz: tuve, hice, pude, dije.","contrast":"El indefinido narra eventos terminados; el imperfecto describe el contexto."},
        "Pretérito imperfecto": {"signals":"antes, siempre, normalmente, mientras, todos los días","pitfall":"Solo hay tres irregulares principales: era, iba y veía.","contrast":"Imperfecto = hábito o descripción; indefinido = evento puntual y terminado."},
        "Pretérito perfecto": {"signals":"hoy, esta semana, ya, todavía no, alguna vez","pitfall":"El participio no concuerda con el sujeto: ellas han llegado.","contrast":"En España suele usarse para períodos abiertos; el uso regional varía en América."},
        "Pluscuamperfecto": {"signals":"ya, todavía no, antes, cuando + pasado","pitfall":"Se conjuga haber, no el participio: habíamos escrito.","contrast":"Sitúa una acción antes de otra acción ya pasada."},
        "Presente": {"signals":"siempre, normalmente, cada día, ahora","pitfall":"Los cambios de raíz no suelen aparecer en nosotros/vosotros: puedo, podemos.","contrast":"Puede traducir tanto present simple como present continuous según el contexto."},
        "Futuro simple": {"signals":"mañana, próximamente, el año que viene","pitfall":"Las terminaciones se añaden al infinitivo completo; aprende los radicales irregulares.","contrast":"Ir a + infinitivo es más conversacional para un plan próximo."},
        "Presente progresivo": {"signals":"ahora mismo, en este momento","pitfall":"Algunos gerundios cambian: leyendo, durmiendo, diciendo.","contrast":"No se usa tanto como en inglés; para hábitos se usa el presente simple."},
        "Ir a + infinitivo": {"signals":"esta tarde, mañana, pronto, planear","pitfall":"No olvides la preposición a: voy a trabajar.","contrast":"Expresa intención próxima; el futuro simple suena más neutro o predictivo."},
        "Condicional simple": {"signals":"si pudiera…, me gustaría, en tu lugar","pitfall":"No uses condicional en la condición con si: si tuviera, haría.","contrast":"La condición suele ir en imperfecto de subjuntivo; el resultado, en condicional."},
        "Presente de subjuntivo": {"signals":"quiero que, dudo que, es importante que, para que","pitfall":"Un solo sujeto suele llevar infinitivo: quiero salir; dos sujetos: quiero que salgas.","contrast":"Indicativo afirma información; subjuntivo presenta deseo, duda o valoración."},
    },
}


EXTRA_EXERCISE_ROWS = [
    # English: extra practice for every tense
    ("English","Past simple","We ___ the contract two days ago. (sign)","sign","signed","Two days ago marks a completed past action."),
    ("English","Past simple","The costs ___ unexpectedly last year. (rise)","rise","rose","Rise is irregular: rise, rose, risen."),
    ("English","Past continuous","They ___ dinner when I phoned. (have)","have","were having","Use were having for the background action."),
    ("English","Past continuous","I ___ home at six yesterday. (drive)","drive","was driving","The action was in progress at a stated past time."),
    ("English","Present perfect","We ___ the target yet. (not reach)","reach","have not reached|haven't reached","Yet with an unfinished result calls for the present perfect."),
    ("English","Present perfect","He ___ five countries this year. (visit)","visit","has visited","This year is still open, so the action is connected to now."),
    ("English","Past perfect","She ___ before the meeting began. (leave)","leave","had left","Leaving happened before the meeting began."),
    ("English","Past perfect","We couldn't enter because we ___ the key. (lose)","lose","had lost","The loss occurred before the later inability to enter."),
    ("English","Present simple","Water ___ at 100°C. (boil)","boil","boils","Use the present simple for a general fact."),
    ("English","Present simple","I ___ the weekly figures every Monday. (check)","check","check","Every Monday signals a routine."),
    ("English","Future with will","Perhaps she ___ us later. (join)","join","will join","Will is suitable for an uncertain prediction."),
    ("English","Future with will","I promise I ___ anyone. (not tell)","tell","will not tell|won't tell","Will expresses a promise."),
    ("English","Present continuous","Please wait; I ___ to the donor now. (talk)","talk","am talking","The action is happening at this moment."),
    ("English","Present continuous","The organisation ___ rapidly this year. (grow)","grow","is growing","Use the continuous for a changing trend."),
    ("English","Present continuous","They ___ in Nairobi this month. (work)","work","are working","This month describes a temporary situation."),
    ("English","Present continuous","Why ___ you ___? (laugh)","laugh","are you laughing","Use are + subject + -ing in a question."),
    ("English","Going to","We ___ a new office next month. (open)","open","are going to open","The opening is an existing plan."),
    ("English","Going to","Look out! You ___ that box. (drop)","drop","are going to drop","Present evidence supports the prediction."),
    ("English","Going to","She ___ for the position. (not apply)","apply","is not going to apply|isn't going to apply","Use is not going to for a negative intention."),
    ("English","Going to","___ they ___ the programme? (extend)","extend","are they going to extend","Invert are and the subject in a question."),
    ("English","Future continuous","At noon tomorrow, we ___. (travel)","travel","will be travelling|will be traveling","The journey will be in progress at noon."),
    ("English","Future continuous","This time next week, he ___ the workshop. (lead)","lead","will be leading","Use will be + -ing for a future action in progress."),
    ("English","Future continuous","___ you ___ the office later? (use)","use","will you be using","Future continuous makes a neutral question about plans."),
    ("English","Future continuous","They ___ with us this quarter. (not work)","work","will not be working|won't be working","Use will not be + -ing for the negative form."),
    ("English","Future perfect","By Friday, I ___ the analysis. (complete)","complete","will have completed","The action will be complete before Friday."),
    ("English","Future perfect","By 2030, the city ___ significantly. (change)","change","will have changed","Use will have + participle before a future deadline."),
    ("English","Future perfect","She ___ ten years here by June. (work)","work","will have worked","By June measures completed duration at a future point."),
    ("English","Future perfect","___ they ___ by then? (arrive)","arrive","will they have arrived","Invert will and the subject for the question."),
    # Spanish: extra practice for every tense
    ("Español","Pretérito indefinido","Nosotros ___ el proyecto en mayo. (terminar)","terminar","terminamos","Mayo es un período cerrado; usamos el indefinido."),
    ("Español","Pretérito indefinido","Ellos ___ una decisión ayer. (tomar)","tomar","tomaron","Ayer indica una acción terminada."),
    ("Español","Pretérito imperfecto","De niña, ella ___ cerca del mar. (vivir)","vivir","vivía","Se describe una situación habitual del pasado."),
    ("Español","Pretérito imperfecto","Eran las ocho y ___ frío. (hacer)","hacer","hacía","El imperfecto describe la hora y el tiempo de fondo."),
    ("Español","Pretérito perfecto","Hoy yo ___ con tres proveedores. (hablar)","hablar","he hablado","Hoy es un período todavía abierto."),
    ("Español","Pretérito perfecto","Ellos todavía no ___. (responder)","responder","han respondido","Todavía no conecta una acción pendiente con el presente."),
    ("Español","Pluscuamperfecto","Nunca ___ tanta demanda. (ver, nosotros)","ver","habíamos visto","La experiencia ocurrió antes de otro momento pasado."),
    ("Español","Pluscuamperfecto","Ella ya ___ cuando la llamé. (salir)","salir","había salido","Salir ocurrió antes de la llamada."),
    ("Español","Presente","Yo siempre ___ el correo por la mañana. (leer)","leer","leo","Siempre expresa un hábito presente."),
    ("Español","Presente","Mis colegas ___ en Valencia. (vivir)","vivir","viven","La tercera persona plural de vivir es viven."),
    ("Español","Futuro simple","Nosotros ___ los resultados mañana. (saber)","saber","sabremos","Saber usa el radical irregular sabr-."),
    ("Español","Futuro simple","¿___ venir el lunes? (poder, tú)","poder","podrás","Poder usa el radical podr- en futuro."),
    ("Español","Presente progresivo","Ahora yo ___ el presupuesto. (revisar)","revisar","estoy revisando","Ahora indica una acción en curso."),
    ("Español","Presente progresivo","Los equipos ___ la ayuda. (distribuir)","distribuir","están distribuyendo","Distribuir forma el gerundio irregular distribuyendo."),
    ("Español","Presente progresivo","Nosotros ___ una solución. (buscar)","buscar","estamos buscando","Usamos estar + gerundio para la acción actual."),
    ("Español","Presente progresivo","¿Qué ___ tú? (hacer)","hacer","estás haciendo","Hacer tiene el gerundio irregular haciendo."),
    ("Español","Ir a + infinitivo","Mañana yo ___ al coordinador. (llamar)","llamar","voy a llamar","Voy a + infinitivo expresa un plan próximo."),
    ("Español","Ir a + infinitivo","Nosotros ___ un nuevo centro. (abrir)","abrir","vamos a abrir","El plan se expresa con vamos a + infinitivo."),
    ("Español","Ir a + infinitivo","Ellos no ___ el viaje. (cancelar)","cancelar","van a cancelar","Van a + infinitivo expresa la intención del sujeto plural."),
    ("Español","Ir a + infinitivo","¿___ tú ___ la solicitud? (enviar)","enviar","vas a enviar","La pregunta mantiene a entre ir y el infinitivo."),
    ("Español","Condicional simple","Yo ___ más recursos si pudiera. (pedir)","pedir","pediría","El condicional expresa el resultado de una hipótesis."),
    ("Español","Condicional simple","¿Me ___ ayudar, por favor? (poder, tú)","poder","podrías","Podrías formula una petición cortés."),
    ("Español","Condicional simple","Nosotros ___ el plan con más tiempo. (cambiar)","cambiar","cambiaríamos","Añadimos -íamos al infinitivo."),
    ("Español","Condicional simple","Ella ___ el informe mañana. (hacer)","hacer","haría","Hacer usa el radical irregular har-."),
    ("Español","Presente de subjuntivo","Quiero que tú ___ conmigo. (venir)","venir","vengas","Querer que + otro sujeto exige subjuntivo."),
    ("Español","Presente de subjuntivo","Es importante que nosotros ___ hoy. (terminar)","terminar","terminemos","Es importante que introduce el subjuntivo."),
    ("Español","Presente de subjuntivo","Dudo que él ___ la respuesta. (saber)","saber","sepa","La duda activa el subjuntivo; saber cambia a sepa."),
    ("Español","Presente de subjuntivo","Te recomiendo que ___ el documento. (leer, tú)","leer","leas","Una recomendación con que exige subjuntivo."),
]

EXERCISES.extend([
    {"language": language, "tense": tense, "sentence": sentence,
     "infinitive": infinitive, "answers": answers.split("|"), "explanation": explanation}
    for language, tense, sentence, infinitive, answers, explanation in EXTRA_EXERCISE_ROWS
])


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
