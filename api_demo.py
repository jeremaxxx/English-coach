"""Démonstration historique de l'API OpenAI.

Ce fichier ne fait pas partie de l'application locale. Il nécessite le paquet
tiers ``openai``, une clé API et une connexion réseau pour être exécuté.
"""

from openai import OpenAI


client = OpenAI()

response = client.responses.create(
    model="gpt-5.4-mini",
    input="Write a short haiku about learning English.",
    store=False,
)

print(response.output_text)
