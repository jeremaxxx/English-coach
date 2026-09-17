"""Vocabulaire trilingue pour les quiz professionnels et quotidiens."""

from typing import Dict, List


VOCABULARY_ROWS = [
    # Humanitaire
    ("Humanitarian aid", "Humanitaire", "bénéficiaire", "beneficiary", "beneficiario / beneficiaria"),
    ("Humanitarian aid", "Humanitaire", "aide d'urgence", "emergency relief", "ayuda de emergencia"),
    ("Humanitarian aid", "Humanitaire", "abri", "shelter", "refugio"),
    ("Humanitarian aid", "Humanitaire", "moyens de subsistance", "livelihoods", "medios de vida"),
    ("Humanitarian aid", "Humanitaire", "personne déplacée", "displaced person", "persona desplazada"),
    ("Humanitarian aid", "Humanitaire", "réfugié", "refugee", "refugiado / refugiada"),
    ("Humanitarian aid", "Humanitaire", "sécurité alimentaire", "food security", "seguridad alimentaria"),
    ("Humanitarian aid", "Humanitaire", "assainissement", "sanitation", "saneamiento"),
    ("Humanitarian aid", "Humanitaire", "protection de l'enfance", "child protection", "protección infantil"),
    ("Humanitarian aid", "Humanitaire", "distribution", "distribution", "distribución"),
    ("Humanitarian operations", "Humanitaire", "évaluation des besoins", "needs assessment", "evaluación de necesidades"),
    ("Humanitarian operations", "Humanitaire", "intervention d'urgence", "emergency response", "respuesta de emergencia"),
    ("Humanitarian operations", "Humanitaire", "chaîne d'approvisionnement", "supply chain", "cadena de suministro"),
    ("Humanitarian operations", "Humanitaire", "partie prenante", "stakeholder", "parte interesada"),
    ("Humanitarian operations", "Humanitaire", "redevabilité", "accountability", "rendición de cuentas"),
    ("Humanitarian operations", "Humanitaire", "renforcement des capacités", "capacity building", "fortalecimiento de capacidades"),
    ("Humanitarian operations", "Humanitaire", "suivi et évaluation", "monitoring and evaluation", "seguimiento y evaluación"),
    ("Humanitarian operations", "Humanitaire", "zone difficile d'accès", "hard-to-reach area", "zona de difícil acceso"),
    ("Humanitarian operations", "Humanitaire", "approvisionnement", "procurement", "adquisiciones"),
    ("Humanitarian operations", "Humanitaire", "principe de ne pas nuire", "do no harm principle", "principio de no hacer daño"),
    # Travail : conseil, gestion, banque et data
    ("Projects & consulting", "Travail", "cahier des charges", "requirements document", "pliego de condiciones"),
    ("Projects & consulting", "Travail", "livrable", "deliverable", "entregable"),
    ("Projects & consulting", "Travail", "échéance", "deadline", "fecha límite"),
    ("Projects & consulting", "Travail", "ordre du jour", "agenda", "orden del día"),
    ("Projects & consulting", "Travail", "compte rendu", "meeting minutes", "acta de reunión"),
    ("Projects & consulting", "Travail", "charge de travail", "workload", "carga de trabajo"),
    ("Projects & consulting", "Travail", "périmètre du projet", "project scope", "alcance del proyecto"),
    ("Projects & consulting", "Travail", "retour d'information", "feedback", "comentarios"),
    ("Projects & consulting", "Travail", "goulot d'étranglement", "bottleneck", "cuello de botella"),
    ("Projects & consulting", "Travail", "mettre en œuvre", "to implement", "implementar"),
    ("Finance & data", "Travail", "chiffre d'affaires", "revenue", "ingresos"),
    ("Finance & data", "Travail", "trésorerie", "cash flow", "flujo de caja"),
    ("Finance & data", "Travail", "prêt", "loan", "préstamo"),
    ("Finance & data", "Travail", "taux d'intérêt", "interest rate", "tipo de interés"),
    ("Finance & data", "Travail", "solvabilité", "creditworthiness", "solvencia"),
    ("Finance & data", "Travail", "jeu de données", "dataset", "conjunto de datos"),
    ("Finance & data", "Travail", "tendance", "trend", "tendencia"),
    ("Finance & data", "Travail", "prévision", "forecast", "previsión"),
    ("Finance & data", "Travail", "écart", "variance", "desviación"),
    ("Finance & data", "Travail", "tableau de bord", "dashboard", "cuadro de mando"),
    # Vie quotidienne
    ("Travel", "Vie quotidienne", "aller simple", "one-way ticket", "billete de ida"),
    ("Travel", "Vie quotidienne", "aller-retour", "return ticket", "billete de ida y vuelta"),
    ("Travel", "Vie quotidienne", "correspondance", "connection", "conexión"),
    ("Travel", "Vie quotidienne", "retard", "delay", "retraso"),
    ("Travel", "Vie quotidienne", "quai", "platform", "andén"),
    ("Travel", "Vie quotidienne", "bagage à main", "hand luggage", "equipaje de mano"),
    ("Travel", "Vie quotidienne", "réserver", "to book", "reservar"),
    ("Travel", "Vie quotidienne", "annuler", "to cancel", "cancelar"),
    ("Travel", "Vie quotidienne", "plan de la ville", "city map", "mapa de la ciudad"),
    ("Travel", "Vie quotidienne", "être en retard", "to be late", "llegar tarde"),
    ("Home", "Vie quotidienne", "loyer", "rent", "alquiler"),
    ("Home", "Vie quotidienne", "propriétaire", "landlord / landlady", "casero / casera"),
    ("Home", "Vie quotidienne", "locataire", "tenant", "inquilino / inquilina"),
    ("Home", "Vie quotidienne", "facture", "bill", "factura"),
    ("Home", "Vie quotidienne", "ménage", "housework", "tareas domésticas"),
    ("Home", "Vie quotidienne", "étagère", "shelf", "estantería"),
    ("Home", "Vie quotidienne", "robinet", "tap / faucet", "grifo"),
    ("Home", "Vie quotidienne", "déménager", "to move house", "mudarse"),
    ("Home", "Vie quotidienne", "en panne", "out of order", "averiado / averiada"),
    ("Home", "Vie quotidienne", "quartier", "neighbourhood", "barrio"),
    ("Health", "Vie quotidienne", "rendez-vous médical", "medical appointment", "cita médica"),
    ("Health", "Vie quotidienne", "ordonnance", "prescription", "receta"),
    ("Health", "Vie quotidienne", "pharmacie", "pharmacy", "farmacia"),
    ("Health", "Vie quotidienne", "blessure", "injury", "lesión"),
    ("Health", "Vie quotidienne", "se rétablir", "to recover", "recuperarse"),
    ("Health", "Vie quotidienne", "mal de tête", "headache", "dolor de cabeza"),
    ("Health", "Vie quotidienne", "fièvre", "fever", "fiebre"),
    ("Health", "Vie quotidienne", "être enrhumé", "to have a cold", "estar resfriado"),
    ("Health", "Vie quotidienne", "douleur", "pain", "dolor"),
    ("Health", "Vie quotidienne", "assurance maladie", "health insurance", "seguro médico"),
    ("Food & social life", "Vie quotidienne", "addition", "bill / check", "cuenta"),
    ("Food & social life", "Vie quotidienne", "pourboire", "tip", "propina"),
    ("Food & social life", "Vie quotidienne", "entrée", "starter / appetizer", "entrante"),
    ("Food & social life", "Vie quotidienne", "plat principal", "main course", "plato principal"),
    ("Food & social life", "Vie quotidienne", "sans gluten", "gluten-free", "sin gluten"),
    ("Food & social life", "Vie quotidienne", "faire connaissance", "to get to know", "conocerse"),
    ("Food & social life", "Vie quotidienne", "se retrouver", "to meet up", "quedar"),
    ("Food & social life", "Vie quotidienne", "avoir hâte", "to look forward to", "tener ganas de"),
    ("Food & social life", "Vie quotidienne", "s'entendre avec", "to get along with", "llevarse bien con"),
    ("Food & social life", "Vie quotidienne", "rendre visite", "to visit", "visitar"),
]


VOCABULARY: List[Dict[str, str]] = [
    {"category": category, "audience": audience, "Français": french,
     "English": english, "Español": spanish}
    for category, audience, french, english, spanish in VOCABULARY_ROWS
]


def vocabulary_for(language: str, categories: List[str]) -> List[Dict[str, str]]:
    """Filtre les cartes de vocabulaire par catégories."""

    return [entry for entry in VOCABULARY if entry["category"] in categories and entry[language]]
