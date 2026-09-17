# English Coach

Application web pour pratiquer l'anglais professionnel, l'anglais général et
l'espagnol. Elle réunit plusieurs espaces pédagogiques :

- 20 fiches de conjugaison anglaise et espagnole, avec plus de 80 exercices ;
- un répertoire de plus de 100 verbes irréguliers et un quiz de mémorisation ;
- 80 expressions de vocabulaire trilingue sur le travail, l'humanitaire et la
  vie quotidienne, consultables ou utilisables en quiz ;
- 30 exercices historiques d'anglais professionnel de niveau B2.

Elle comprend également un atelier d'écriture C1 : e-mails, rapports,
propositions, essais, synthèses, traductions et reformulations. Chaque travail
suit une boucle brouillon → analyse → réécriture → comparaison avec un modèle.
Un carnet d'erreurs, des cartes de révision, des exercices de grammaire avancée
et un export JSON privé permettent de suivre la progression.

Aucune API d'intelligence artificielle n'est appelée : le contenu et la
correction fermée fonctionnent localement. L'évaluation IA des productions
libres est facultative et reste désactivée tant qu'aucune clé API n'est ajoutée
aux secrets Streamlit.

## Évaluation IA facultative

L'abonnement ChatGPT et l'API OpenAI sont deux produits facturés séparément.
Après avoir activé la facturation API, ajouter dans les secrets du déploiement :

```toml
OPENAI_API_KEY = "votre-clé-de-projet"
OPENAI_MODEL = "gpt-5.6-luna"
OPENAI_ALLOWED_EMAILS = ["vous@example.com", "partenaire@example.com"]
OPENAI_MAX_CALLS_PER_SESSION = 10
```

Ne jamais placer une vraie clé dans le dépôt. L'application lit la clé côté
serveur, impose un consentement avant chaque envoi et utilise `store=false`.
Les textes ne sont pas écrits dans les journaux de l'application. Une liste
d'adresses autorisées et un maximum d'évaluations par session peuvent être
configurés ; il faut également définir un budget et des limites dans le projet
API OpenAI, seule protection globale contre la multiplication des sessions.

Sans clé, l'analyse locale, la réécriture, les modèles C1, la grammaire, le
vocabulaire et tous les quiz restent disponibles.

## Prérequis

- Python 3.10 à 3.14 (Python 3.12 est recommandé)

## Installation

Depuis le dossier du projet :

```bash
/opt/anaconda3/bin/python3.12 -m venv .venv-streamlit
source .venv-streamlit/bin/activate
python -m pip install -r requirements.txt
```

La première commande ne doit être exécutée qu'une fois. Lors des utilisations
suivantes, il suffit de réactiver l'environnement.

## Lancer l'application

```bash
source .venv-streamlit/bin/activate
python -m streamlit run app.py
```

Streamlit ouvre normalement `http://localhost:8501` dans le navigateur. Les
thèmes se sélectionnent dans la barre latérale. La progression et la moyenne
existent uniquement pendant la session et sont perdues lorsqu'elle est fermée.

## Exécuter les tests

```bash
python -m unittest discover -s tests -v
```

## Organisation

- `app.py` : interface Streamlit, navigation et état de la session ;
- `coach.py` : normalisation, comparaison et score via `get_feedback()` ;
- `conjugation.py` : cours, exercices et correction de conjugaison bilingues ;
- `irregular_verbs.py` : formes essentielles des verbes irréguliers ;
- `vocabulary.py` : lexique trilingue professionnel, humanitaire et quotidien ;
- `c1_content.py` : sujets d'écriture, modèles et grammaire avancée C1 ;
- `writing_coach.py` : analyse locale, appel API facultatif et export de progression ;
- `exercises.json` : 30 exercices d'anglais professionnel ;
- `tests/test_coach.py` : tests unitaires du moteur de correction ;
- `.streamlit/config.toml` : couleurs et configuration locale de l'interface ;
- `requirements.txt` : dépendance Streamlit ;
- `.python-version` : version Python recommandée ;
- `api_demo.py` : ancienne démonstration OpenAI, isolée de l'application.

## Limite du prototype

Le score mesure la ressemblance textuelle avec la réponse modèle. La casse, la
ponctuation et les espaces superflus sont ignorés. Sans modèle linguistique, une
formulation différente mais correcte peut donc recevoir un score inférieur.

`api_demo.py` n'est jamais importé par l'application. Son exécution manuelle
nécessiterait le paquet `openai`, une clé et une connexion réseau ; il est
conservé seulement comme exemple séparé.

## Déployer pour une autre personne

Le déploiement le plus simple utilise GitHub et Streamlit Community Cloud. La
personne qui utilise l'application n'a alors rien à installer : elle ouvre une
adresse `https://...streamlit.app` dans son navigateur.

Le guide détaillé se trouve dans [`DEPLOYMENT.md`](DEPLOYMENT.md).
