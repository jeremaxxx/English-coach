from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4-mini",
    input="Write a short haiku about learning English.",
    store=False,
)

print(response.output_text)

