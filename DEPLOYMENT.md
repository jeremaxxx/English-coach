# Déployer English Coach avec Streamlit Community Cloud

Ce déploiement est gratuit pour une petite application pédagogique. GitHub
stocke le code et Streamlit Community Cloud exécute `app.py` sur un serveur. Le
navigateur de l'utilisateur communique avec ce serveur par une URL publique ou
privée.

## 1. Vérifier le projet localement

```bash
source .venv-streamlit/bin/activate
python -m unittest discover -s tests -v
python -m streamlit run app.py
```

## 2. Créer un dépôt GitHub

1. Créer un compte sur <https://github.com> si nécessaire.
2. Cliquer sur **New repository**.
3. Choisir un nom, par exemple `english-coach`.
4. Choisir **Public** pour un accès simple par URL, ou **Private** pour limiter
   l'accès.
5. Ne pas ajouter de README ou de `.gitignore` depuis GitHub : ils existent déjà.

## 3. Envoyer le projet vers GitHub

Dans le terminal, remplacer `VOTRE-NOM` par le nom du compte GitHub :

```bash
git add .
git commit -m "Build local English Coach with Streamlit"
git remote add origin https://github.com/VOTRE-NOM/english-coach.git
git push -u origin main
```

Avant `git add .`, vérifier les fichiers avec `git status`. Les environnements
virtuels, caches, fichiers `.env` et secrets Streamlit sont exclus par
`.gitignore` et ne doivent jamais être publiés.

## 4. Créer l'application Streamlit Cloud

1. Ouvrir <https://share.streamlit.io> et se connecter avec GitHub.
2. Autoriser Streamlit à lire le dépôt choisi.
3. Cliquer sur **Create app**.
4. Sélectionner le dépôt `english-coach` et la branche `main`.
5. Indiquer `app.py` comme **Main file path**.
6. Dans **Advanced settings**, choisir Python 3.12.
7. Cliquer sur **Deploy**.

Streamlit installe automatiquement la version indiquée dans `requirements.txt`,
charge `exercises.json`, puis démarre l'application. Aucun secret n'est requis
pour cette version.

## 5. Partager l'application

- Dépôt/application publics : envoyer simplement l'URL `*.streamlit.app`.
- Application privée : ajouter l'adresse e-mail de la personne dans les réglages
  de partage Streamlit. Elle devra s'identifier.

## 6. Publier une modification ultérieure

Après avoir modifié et testé le projet :

```bash
git add .
git commit -m "Describe the change"
git push
```

Streamlit détecte la nouvelle version sur GitHub et redéploie automatiquement
l'application.

## Comprendre le parcours du code

```text
Ordinateur du développeur
        │ git push
        ▼
      GitHub
        │ mise à jour détectée
        ▼
Streamlit Community Cloud
        │ page web HTTPS
        ▼
Navigateur de l'utilisateur
```

GitHub n'exécute pas l'application : il conserve son code et son historique.
Streamlit Cloud crée l'environnement Python, installe les dépendances et fait
tourner le serveur. La progression étant stockée dans `st.session_state`, chaque
onglet possède sa propre session temporaire et rien n'est sauvegardé durablement.
