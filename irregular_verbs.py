"""Répertoires locaux de verbes irréguliers anglais et espagnols."""

from typing import Dict, List


ENGLISH_ROWS = [
    ("be", "was / were", "been", "être"), ("become", "became", "become", "devenir"),
    ("begin", "began", "begun", "commencer"), ("break", "broke", "broken", "casser"),
    ("bring", "brought", "brought", "apporter"), ("build", "built", "built", "construire"),
    ("buy", "bought", "bought", "acheter"), ("catch", "caught", "caught", "attraper"),
    ("choose", "chose", "chosen", "choisir"), ("come", "came", "come", "venir"),
    ("cost", "cost", "cost", "coûter"), ("cut", "cut", "cut", "couper"),
    ("deal", "dealt", "dealt", "traiter / gérer"), ("do", "did", "done", "faire"),
    ("draw", "drew", "drawn", "dessiner / tirer"), ("drink", "drank", "drunk", "boire"),
    ("drive", "drove", "driven", "conduire"), ("eat", "ate", "eaten", "manger"),
    ("fall", "fell", "fallen", "tomber"), ("feel", "felt", "felt", "ressentir"),
    ("fight", "fought", "fought", "combattre"), ("find", "found", "found", "trouver"),
    ("fly", "flew", "flown", "voler"), ("forget", "forgot", "forgotten", "oublier"),
    ("forgive", "forgave", "forgiven", "pardonner"), ("get", "got", "got / gotten", "obtenir"),
    ("give", "gave", "given", "donner"), ("go", "went", "gone", "aller"),
    ("grow", "grew", "grown", "grandir / croître"), ("have", "had", "had", "avoir"),
    ("hear", "heard", "heard", "entendre"), ("hide", "hid", "hidden", "cacher"),
    ("hold", "held", "held", "tenir"), ("keep", "kept", "kept", "garder"),
    ("know", "knew", "known", "savoir / connaître"), ("lead", "led", "led", "diriger"),
    ("leave", "left", "left", "partir / laisser"), ("lend", "lent", "lent", "prêter"),
    ("let", "let", "let", "laisser"), ("lose", "lost", "lost", "perdre"),
    ("make", "made", "made", "faire / fabriquer"), ("mean", "meant", "meant", "signifier"),
    ("meet", "met", "met", "rencontrer"), ("pay", "paid", "paid", "payer"),
    ("put", "put", "put", "mettre"), ("read", "read", "read", "lire"),
    ("ride", "rode", "ridden", "monter / faire du vélo"), ("ring", "rang", "rung", "sonner"),
    ("run", "ran", "run", "courir"), ("say", "said", "said", "dire"),
    ("see", "saw", "seen", "voir"), ("sell", "sold", "sold", "vendre"),
    ("send", "sent", "sent", "envoyer"), ("set", "set", "set", "fixer / placer"),
    ("show", "showed", "shown", "montrer"), ("shut", "shut", "shut", "fermer"),
    ("sing", "sang", "sung", "chanter"), ("sit", "sat", "sat", "s'asseoir"),
    ("sleep", "slept", "slept", "dormir"), ("speak", "spoke", "spoken", "parler"),
    ("spend", "spent", "spent", "dépenser / passer"), ("stand", "stood", "stood", "être debout"),
    ("swim", "swam", "swum", "nager"), ("take", "took", "taken", "prendre"),
    ("teach", "taught", "taught", "enseigner"), ("tell", "told", "told", "dire / raconter"),
    ("think", "thought", "thought", "penser"), ("understand", "understood", "understood", "comprendre"),
    ("wear", "wore", "worn", "porter"), ("win", "won", "won", "gagner"),
    ("write", "wrote", "written", "écrire"),
]

ENGLISH_IRREGULARS: List[Dict[str, str]] = [
    {"Infinitive": base, "Past simple": past, "Past participle": participle, "Français": meaning}
    for base, past, participle, meaning in ENGLISH_ROWS
]


SPANISH_ROWS = [
    ("andar", "marcher", "ando", "anduve", "andado", "andaré"),
    ("caber", "tenir / rentrer", "quepo", "cupe", "cabido", "cabré"),
    ("caer", "tomber", "caigo", "caí", "caído", "caeré"),
    ("conducir", "conduire", "conduzco", "conduje", "conducido", "conduciré"),
    ("conocer", "connaître", "conozco", "conocí", "conocido", "conoceré"),
    ("dar", "donner", "doy", "di", "dado", "daré"),
    ("decir", "dire", "digo", "dije", "dicho", "diré"),
    ("dormir", "dormir", "duermo", "dormí", "dormido", "dormiré"),
    ("estar", "être", "estoy", "estuve", "estado", "estaré"),
    ("haber", "avoir (auxiliaire)", "he", "hube", "habido", "habré"),
    ("hacer", "faire", "hago", "hice", "hecho", "haré"),
    ("ir", "aller", "voy", "fui", "ido", "iré"),
    ("leer", "lire", "leo", "leí", "leído", "leeré"),
    ("morir", "mourir", "muero", "morí", "muerto", "moriré"),
    ("oír", "entendre", "oigo", "oí", "oído", "oiré"),
    ("pedir", "demander", "pido", "pedí", "pedido", "pediré"),
    ("poder", "pouvoir", "puedo", "pude", "podido", "podré"),
    ("poner", "mettre", "pongo", "puse", "puesto", "pondré"),
    ("querer", "vouloir / aimer", "quiero", "quise", "querido", "querré"),
    ("reír", "rire", "río", "reí", "reído", "reiré"),
    ("saber", "savoir", "sé", "supe", "sabido", "sabré"),
    ("salir", "sortir", "salgo", "salí", "salido", "saldré"),
    ("seguir", "suivre", "sigo", "seguí", "seguido", "seguiré"),
    ("sentir", "sentir", "siento", "sentí", "sentido", "sentiré"),
    ("ser", "être", "soy", "fui", "sido", "seré"),
    ("tener", "avoir", "tengo", "tuve", "tenido", "tendré"),
    ("traer", "apporter", "traigo", "traje", "traído", "traeré"),
    ("venir", "venir", "vengo", "vine", "venido", "vendré"),
    ("ver", "voir", "veo", "vi", "visto", "veré"),
    ("volver", "revenir", "vuelvo", "volví", "vuelto", "volveré"),
]

SPANISH_IRREGULARS: List[Dict[str, str]] = [
    {"Infinitivo": base, "Français": meaning, "Presente (yo)": present,
     "Indefinido (yo)": past, "Participio": participle, "Futuro (yo)": future}
    for base, meaning, present, past, participle, future in SPANISH_ROWS
]


def irregulars_for(language: str) -> List[Dict[str, str]]:
    """Retourne le répertoire correspondant à la langue."""

    return ENGLISH_IRREGULARS if language == "English" else SPANISH_IRREGULARS
