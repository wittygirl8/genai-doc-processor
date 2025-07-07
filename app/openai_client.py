import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
def answer_with_gpt(query, context_chunks):
    context = "\n".join(context_chunks)
    messages = [
        {"role": "system", "content": "Use the context to answer."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response["choices"][0]["message"]["content"]
