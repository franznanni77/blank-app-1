import openai

# Esempio di chiamata aggiornata per chiedere un completamento
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Ciao, come stai?"}
    ]
)

print(response.choices[0].message["content"])