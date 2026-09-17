"""Contenus statiques du parcours d'écriture et de grammaire C1."""

from typing import Dict, List, TypedDict


class WritingPrompt(TypedDict):
    id: str
    language: str
    kind: str
    title: str
    scenario: str
    instructions: List[str]
    min_words: int
    max_words: int
    model_answer: str
    focus: List[str]


class AdvancedExercise(TypedDict):
    topic: str
    prompt: str
    answers: List[str]
    explanation: str


WRITING_PROMPTS: List[WritingPrompt] = [
    {
        "id": "en-email-delay", "language": "English", "kind": "Professional email",
        "title": "Handle a supplier delay",
        "scenario": "A critical delivery is ten days late. The supplier has provided no clear explanation.",
        "instructions": ["Explain the operational impact", "Request a revised date and recovery plan", "Remain firm but diplomatic"],
        "min_words": 140, "max_words": 190,
        "model_answer": "Dear Ms Patel,\n\nI am writing regarding the equipment originally due on 12 May, which has yet to arrive. As these items are required for the next phase of implementation, the delay is now affecting both our schedule and the availability of the field team.\n\nCould you please confirm the revised delivery date and provide a brief recovery plan by close of business tomorrow? In particular, it would be helpful to know whether partial delivery or expedited transport could mitigate the current disruption.\n\nWe value our working relationship and appreciate that unforeseen constraints can arise. Nevertheless, given the operational consequences, we need a firm and realistic commitment on which we can plan.\n\nKind regards,\nAlex",
        "focus": ["diplomatic firmness", "hedging", "clear call to action"],
    },
    {
        "id": "en-report-project", "language": "English", "kind": "Report",
        "title": "Evaluate a delayed project",
        "scenario": "A six-month digital project is four weeks behind schedule but remains within budget.",
        "instructions": ["Summarise the situation", "Identify two causes", "Recommend three corrective actions"],
        "min_words": 220, "max_words": 300,
        "model_answer": "Executive summary\n\nThe digitalisation project is currently four weeks behind its original schedule, although expenditure remains within the approved budget. The delay is primarily attributable to late validation of the functional requirements and limited availability among key subject-matter experts.\n\nFindings\n\nWhile technical delivery has broadly met quality expectations, repeated changes to the scope have created avoidable rework. In addition, decisions requiring business approval have taken an average of nine days, compared with the three days assumed in the plan. Unless addressed, these constraints are likely to affect user testing and training.\n\nRecommendations\n\nFirst, the steering committee should freeze all non-essential requirements until the initial release. Second, a named deputy should be authorised to approve routine decisions whenever the principal owner is unavailable. Finally, the team should adopt a two-week recovery schedule with weekly milestone reviews.\n\nThese measures should enable the project to recover approximately three weeks without additional expenditure, while preserving the quality of the final release.",
        "focus": ["report structure", "cause and consequence", "actionable recommendations"],
    },
    {
        "id": "en-proposal-hybrid", "language": "English", "kind": "Proposal",
        "title": "Improve hybrid working",
        "scenario": "Staff report meeting overload, uneven access to information and declining collaboration in a hybrid team.",
        "instructions": ["Define the problem", "Propose practical measures", "Anticipate one objection"],
        "min_words": 220, "max_words": 300,
        "model_answer": "Purpose\n\nThis proposal outlines a more sustainable approach to hybrid working, with the aim of reducing meeting overload while ensuring that remote and office-based colleagues have equal access to information.\n\nProposed measures\n\nThe team should introduce two meeting-free half-days each week and require every recurring meeting to have a stated purpose, agenda and decision owner. Key decisions should be recorded in a shared log within 24 hours. In addition, project teams should hold one optional in-person collaboration day per month rather than imposing a fixed weekly presence.\n\nPotential concern\n\nManagers may worry that fewer meetings will reduce visibility. However, concise written updates and clearly assigned outcomes would provide a more reliable picture of progress than attendance alone.\n\nRecommendation\n\nA six-week pilot should be launched and evaluated using meeting hours, response times and an anonymous staff survey. If the data confirms improved focus without slower delivery, the approach could then be adopted permanently.",
        "focus": ["persuasive structure", "anticipating objections", "formal register"],
    },
    {
        "id": "en-essay-ai", "language": "English", "kind": "Argumentative essay",
        "title": "AI and professional judgement",
        "scenario": "Some organisations increasingly rely on artificial intelligence to support recruitment and performance decisions.",
        "instructions": ["Discuss benefits and risks", "Take a clear position", "Support it with examples"],
        "min_words": 250, "max_words": 330,
        "model_answer": "Artificial intelligence can help organisations process large volumes of information consistently, yet its growing role in employment decisions raises a fundamental question: efficiency at what cost?\n\nSupporters rightly point out that automated screening can reduce administrative work and identify patterns that human reviewers might overlook. Used carefully, such tools may also make criteria more explicit. Nevertheless, consistency should not be confused with fairness. A model trained on historical decisions may reproduce existing inequalities while presenting its conclusions as objective. Moreover, qualities such as judgement, resilience and potential are difficult to infer from standardised data alone.\n\nThe strongest approach is therefore not to reject AI, but to limit it to decision support. Systems should be independently audited, candidates should know when automation is involved, and a qualified person should remain accountable for every consequential decision. For example, an algorithm might flag applications for closer review, but it should not determine rejection without meaningful human assessment.\n\nUltimately, professional judgement can be informed by technology but should not be delegated to it. The more significant the decision, the greater the need for transparency, context and human responsibility.",
        "focus": ["argument development", "concession", "nuanced conclusion"],
    },
    {
        "id": "en-synthesis-humanitarian", "language": "English", "kind": "Synthesis",
        "title": "Prioritise a humanitarian response",
        "scenario": "A rapid assessment finds water shortages, overcrowded shelters and disrupted access to primary healthcare after flooding.",
        "instructions": ["Synthesise the three needs without listing them mechanically", "Set priorities", "Explain dependencies and trade-offs"],
        "min_words": 180, "max_words": 240,
        "model_answer": "The assessment indicates that the affected population faces three interrelated risks rather than separate sectoral problems. Limited access to safe water creates an immediate public-health threat, which is compounded by overcrowded shelters and reduced access to basic healthcare.\n\nWater supply and sanitation should therefore be stabilised first, alongside urgent measures to reduce congestion in collective shelters. These actions would lower the likelihood of communicable disease while creating safer conditions for vulnerable households. Mobile health services should be deployed in parallel, initially prioritising acute cases, maternal health and continuity of essential treatment.\n\nResources should not, however, be divided equally across all locations. Areas reporting both unsafe water and limited clinical access warrant priority because delays there are likely to produce the most severe consequences. Coordination with local authorities and community representatives will be essential to verify needs, avoid duplication and ensure that assistance reaches people facing the greatest barriers.",
        "focus": ["synthesis", "prioritisation", "cohesion"],
    },
    {
        "id": "en-rewrite-direct", "language": "English", "kind": "B2 to C1 reformulation",
        "title": "Make a message diplomatic",
        "scenario": "Rewrite the following message: “Your team did not send the figures, so we cannot finish the report. Send them today.”",
        "instructions": ["Preserve the urgency", "Remove blame", "Make the next action unambiguous"],
        "min_words": 55, "max_words": 90,
        "model_answer": "We have not yet received the figures required to finalise the report. As this is now affecting the agreed timetable, could you please send the outstanding data by close of business today? If there is any difficulty meeting this deadline, please let us know as soon as possible so that we can review the available options.",
        "focus": ["register", "depersonalising problems", "precise deadline"],
    },
    {
        "id": "en-translation-risk", "language": "English", "kind": "Translation",
        "title": "Translate a risk update",
        "scenario": "Translate into natural professional English: “Même si le risque paraît limité à court terme, nous ne pouvons pas exclure une dégradation rapide de la situation.”",
        "instructions": ["Avoid word-for-word translation", "Use appropriate hedging", "Maintain a formal register"],
        "min_words": 18, "max_words": 35,
        "model_answer": "Although the risk appears limited in the short term, the possibility of a rapid deterioration in the situation cannot be ruled out.",
        "focus": ["concession", "passive structure", "risk language"],
    },
    {
        "id": "en-complaint-service", "language": "English", "kind": "Professional email",
        "title": "Respond to a dissatisfied client",
        "scenario": "A client complains that your analysis arrived late and did not answer one of their key questions.",
        "instructions": ["Acknowledge the problem", "Take proportionate responsibility", "Offer a concrete remedy"],
        "min_words": 150, "max_words": 210,
        "model_answer": "Dear Mr Lewis,\n\nThank you for raising your concerns. I appreciate that the delayed delivery, together with the omission of the regional comparison, meant that the analysis did not fully meet the purpose for which it was requested.\n\nWe have reviewed what happened and identified a gap in our final quality-control process. I apologise for the inconvenience this caused. We are now completing the missing comparison and will send a revised version by 3 p.m. tomorrow. I would also be happy to arrange a short call to take you through the updated findings and confirm that no further questions remain outstanding.\n\nTo prevent a recurrence, all future deliverables for this project will undergo a documented scope check before submission.\n\nKind regards,\nAlex",
        "focus": ["accountability", "service recovery", "professional tone"],
    },
    {
        "id": "es-correo-retraso", "language": "Español", "kind": "Correo profesional",
        "title": "Gestionar un retraso",
        "scenario": "Una entrega esencial lleva diez días de retraso y el proveedor no ha dado una explicación clara.",
        "instructions": ["Explicar el impacto", "Solicitar una fecha y un plan", "Mantener un tono firme y diplomático"],
        "min_words": 140, "max_words": 190,
        "model_answer": "Estimada Sra. López:\n\nMe pongo en contacto con usted en relación con el material cuya entrega estaba prevista para el 12 de mayo y que todavía no hemos recibido. Dado que estos artículos son necesarios para la siguiente fase, el retraso ya está afectando tanto al calendario como a la disponibilidad del equipo.\n\nLe agradeceríamos que nos confirmara mañana, antes del cierre, una nueva fecha de entrega y un breve plan de recuperación. En particular, sería útil saber si un envío parcial o un transporte urgente permitirían reducir el impacto actual.\n\nValoramos nuestra colaboración y entendemos que pueden surgir imprevistos. No obstante, necesitamos un compromiso firme y realista que nos permita reorganizar las actividades.\n\nAtentamente,\nAlex",
        "focus": ["cortesía", "subjuntivo", "petición precisa"],
    },
    {
        "id": "es-informe-mision", "language": "Español", "kind": "Informe",
        "title": "Resumir una misión de evaluación",
        "scenario": "Una evaluación identifica falta de agua, acceso sanitario limitado y problemas de protección.",
        "instructions": ["Sintetizar los hallazgos", "Priorizar necesidades", "Proponer acciones"],
        "min_words": 220, "max_words": 300,
        "model_answer": "Resumen ejecutivo\n\nLa misión constató que las comunidades afectadas se enfrentan a necesidades simultáneas de agua, salud y protección. La escasez de agua potable representa el riesgo más inmediato, especialmente en los asentamientos con mayor densidad de población. Al mismo tiempo, la interrupción de los servicios de salud limita la atención de casos agudos y el seguimiento de enfermedades crónicas.\n\nPrioridades\n\nSe recomienda restablecer de forma urgente los puntos de abastecimiento y reforzar las medidas de saneamiento. Esta intervención debería coordinarse con equipos móviles de salud, priorizando a menores, mujeres embarazadas y personas con movilidad reducida. Asimismo, los mecanismos de distribución deberán incorporar medidas de protección que reduzcan los riesgos durante los desplazamientos y las esperas.\n\nPróximos pasos\n\nConviene validar estos hallazgos con representantes comunitarios, definir indicadores semanales y revisar la respuesta al cabo de catorce días. Este enfoque permitiría adaptar los recursos a la evolución de las necesidades y detectar posibles brechas de cobertura.",
        "focus": ["síntesis", "priorización", "registro humanitario"],
    },
    {
        "id": "es-propuesta-equipo", "language": "Español", "kind": "Propuesta",
        "title": "Mejorar la coordinación del equipo",
        "scenario": "Un equipo internacional pierde información entre reuniones y duplica tareas.",
        "instructions": ["Definir el problema", "Proponer medidas", "Incluir criterios de evaluación"],
        "min_words": 210, "max_words": 280,
        "model_answer": "Objetivo\n\nLa presente propuesta tiene por objeto reducir la duplicación de tareas y garantizar que las decisiones sean accesibles para todos los miembros del equipo, independientemente de su ubicación.\n\nMedidas propuestas\n\nEn primer lugar, cada reunión debería concluir con un registro breve de decisiones, responsables y plazos. En segundo lugar, convendría centralizar los documentos operativos en un único espacio compartido, con una estructura y unas normas de archivo comunes. Por último, se propone sustituir parte de las reuniones informativas por actualizaciones escritas semanales.\n\nEvaluación\n\nLa medida podría aplicarse durante seis semanas. Su eficacia se evaluaría comparando el número de tareas duplicadas, el tiempo dedicado a reuniones y una encuesta breve sobre el acceso a la información. Aunque la adopción inicial requerirá cierta disciplina, el ahorro de tiempo y la mayor claridad deberían compensar ampliamente ese esfuerzo.",
        "focus": ["estructura", "recomendaciones", "condicional"],
    },
    {
        "id": "es-ensayo-teletrabajo", "language": "Español", "kind": "Ensayo argumentativo",
        "title": "Teletrabajo y cohesión",
        "scenario": "Algunas empresas sostienen que el trabajo presencial es indispensable para mantener la cultura de equipo.",
        "instructions": ["Examinar dos perspectivas", "Defender una postura", "Matizar la conclusión"],
        "min_words": 250, "max_words": 330,
        "model_answer": "El debate sobre el teletrabajo suele presentarse como una elección entre productividad y cohesión. Sin embargo, esta oposición simplifica una cuestión que depende, en gran medida, de cómo se organice el trabajo.\n\nLa presencia física puede facilitar conversaciones espontáneas, el aprendizaje informal y la integración de nuevos empleados. Sería un error negar estas ventajas. No obstante, obligar a todos los trabajadores a acudir diariamente no garantiza por sí solo una cultura sólida. Un equipo puede compartir oficina y, aun así, carecer de objetivos comunes, confianza o información accesible.\n\nUn modelo híbrido bien diseñado parece ofrecer un equilibrio más razonable. Las actividades que se benefician claramente de la interacción presencial pueden concentrarse en determinados momentos, mientras que el trabajo que exige concentración puede realizarse a distancia. Para que este sistema funcione, los responsables deben evaluar resultados en lugar de visibilidad y documentar las decisiones importantes.\n\nPor tanto, la cohesión no depende tanto del lugar como de la calidad de la coordinación. La presencialidad sigue siendo valiosa, pero debería responder a una finalidad concreta y no convertirse en un objetivo en sí misma.",
        "focus": ["argumentación", "concesión", "matización"],
    },
]


ADVANCED_GRAMMAR: List[AdvancedExercise] = [
    {"topic":"Inversion","prompt":"Rewrite with inversion: We had rarely encountered such resistance.","answers":["Rarely had we encountered such resistance."],"explanation":"A negative or restrictive adverb at the beginning triggers auxiliary–subject inversion."},
    {"topic":"Inversion","prompt":"Complete: Not only ___ the deadline, but they also reduced costs. (meet)","answers":["did they meet"],"explanation":"Not only at the beginning requires inversion with did + base form."},
    {"topic":"Inversion","prompt":"Rewrite: I understood the scale of the problem only then.","answers":["Only then did I understand the scale of the problem."],"explanation":"Only + adverbial at the beginning triggers inversion."},
    {"topic":"Cleft sentences","prompt":"Emphasise “clear leadership”: We need clear leadership most.","answers":["What we need most is clear leadership."],"explanation":"A what-cleft highlights the element after be."},
    {"topic":"Cleft sentences","prompt":"Emphasise the timing: The decision was announced yesterday.","answers":["It was yesterday that the decision was announced."],"explanation":"An it-cleft can foreground a time expression."},
    {"topic":"Mixed conditionals","prompt":"If we ___ the warning earlier, we would be better prepared now. (take)","answers":["had taken"],"explanation":"Past condition + present result: if + past perfect, would + base form."},
    {"topic":"Mixed conditionals","prompt":"If she were more decisive, she ___ the offer yesterday. (accept)","answers":["would have accepted"],"explanation":"Present characteristic + past result uses would have + participle."},
    {"topic":"Past modals","prompt":"The figures are wrong. You ___ the wrong file. (use, deduction)","answers":["must have used"],"explanation":"Must have + participle expresses a strong deduction about the past."},
    {"topic":"Past modals","prompt":"We ___ the client earlier; now it is too late. (inform, criticism)","answers":["should have informed"],"explanation":"Should have expresses criticism or regret about a past action."},
    {"topic":"Past modals","prompt":"The delay ___ by the storm, but we are not certain. (cause)","answers":["might have been caused","may have been caused"],"explanation":"Might/may have been + participle expresses uncertain passive deduction."},
    {"topic":"Advanced passive","prompt":"Rewrite: People believe that the policy has failed.","answers":["The policy is believed to have failed."],"explanation":"Reporting passive: subject + is believed + perfect infinitive."},
    {"topic":"Advanced passive","prompt":"Rewrite: They expect the team to finish tomorrow.","answers":["The team is expected to finish tomorrow."],"explanation":"The object becomes the subject of the reporting passive."},
    {"topic":"Participle clauses","prompt":"Reduce the clause: Because she was concerned about the delay, she called the supplier.","answers":["Concerned about the delay, she called the supplier."],"explanation":"A past-participle clause can express reason when the subject is shared."},
    {"topic":"Participle clauses","prompt":"Reduce: After he had reviewed the evidence, he changed his recommendation.","answers":["Having reviewed the evidence, he changed his recommendation."],"explanation":"Having + participle marks an earlier completed action."},
    {"topic":"Hedging","prompt":"Make less absolute: This policy will fail.","answers":["This policy is likely to fail.","This policy may well fail.","There is a risk that this policy will fail."],"explanation":"C1 writing calibrates certainty instead of making unsupported absolute claims."},
    {"topic":"Nominalisation","prompt":"Rewrite formally: We analysed the data and found several inconsistencies.","answers":["Our analysis of the data revealed several inconsistencies."],"explanation":"Nominalisation can create a concise formal style when used selectively."},
    {"topic":"Concession","prompt":"Combine with “despite”: The budget was limited. The team delivered all outputs.","answers":["Despite the limited budget, the team delivered all outputs."],"explanation":"Despite is followed by a noun phrase or -ing form, not a full finite clause."},
    {"topic":"Register","prompt":"Rewrite professionally: Your plan won't work.","answers":["The proposed approach may be difficult to implement successfully.","There may be significant challenges in implementing the proposed approach."],"explanation":"Depersonalise disagreement and qualify the claim."},
    {"topic":"Subjuntivo","prompt":"Complete: Es fundamental que el equipo ___ los riesgos. (evaluar)","answers":["evalúe"],"explanation":"Es fundamental que exige presente de subjuntivo."},
    {"topic":"Subjuntivo","prompt":"Complete: Buscamos una solución que ___ sostenible. (ser)","answers":["sea"],"explanation":"Una característica buscada pero no confirmada activa el subjuntivo."},
    {"topic":"Condicionales","prompt":"Si lo ___ antes, habríamos actuado de otra manera. (saber, nosotros)","answers":["hubiéramos sabido","hubiésemos sabido"],"explanation":"Condición irreal pasada: pluscuamperfecto de subjuntivo + condicional compuesto."},
    {"topic":"Registro","prompt":"Reformula formalmente: Mándame los datos hoy.","answers":["Le agradecería que me enviara los datos hoy.","Le agradecería que me enviase los datos hoy."],"explanation":"El condicional de cortesía y el imperfecto de subjuntivo suavizan la petición."},
    {"topic":"Concesión","prompt":"Completa: ___ el presupuesto sea limitado, podemos actuar. (aunque)","answers":["Aunque"],"explanation":"Aunque + subjuntivo presenta una circunstancia aceptada como posible o no confirmada."},
    {"topic":"Estilo formal","prompt":"Nominaliza: El equipo evaluó las necesidades rápidamente.","answers":["El equipo realizó una rápida evaluación de las necesidades."],"explanation":"La nominalización es frecuente en informes, pero debe mantenerse clara."},
]


def writing_prompts_for(language: str, kind: str = "All") -> List[WritingPrompt]:
    """Filtre les sujets de production écrite."""

    return [p for p in WRITING_PROMPTS if p["language"] == language and (kind == "All" or p["kind"] == kind)]


def advanced_exercises_for(language: str) -> List[AdvancedExercise]:
    """Sépare les exercices anglais et espagnols selon leur contenu."""

    spanish_topics = {"Subjuntivo", "Condicionales", "Registro", "Concesión", "Estilo formal"}
    return [x for x in ADVANCED_GRAMMAR if (x["topic"] in spanish_topics) == (language == "Español")]
