# English Coach

Application web locale pour pratiquer l'anglais professionnel de niveau B2.
Elle propose 30 exercices sur les entretiens, le conseil, la banque, la data et
les situations de Business Manager. Les réponses restent sur votre ordinateur :
aucune API d'intelligence artificielle n'est appelée.

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

- `app.py` : interface Streamlit, filtres et état de la session ;
- `coach.py` : normalisation, comparaison et score via `get_feedback()` ;
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
