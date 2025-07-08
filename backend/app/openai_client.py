# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()  # loads .env file
# api_key = os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=api_key)

# def answer_with_gpt(query, context_chunks):
#     context = "\n".join(context_chunks)
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "Use the context to answer the user question."},
#             {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"}
#         ]
#     )
#     return response.choices[0].message.content

from transformers import pipeline

# Load pipelines only once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

def summarize_text(text: str) -> str:
    # Optional: truncate for models that don't handle long input
    text = text[:2000]  # Adjust based on model limits
    result = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return result[0]['summary_text']

def answer_with_qa(question: str, context_chunks: list[str]) -> str:
    context = "\n".join(context_chunks)
    context = context[:2500]  # Limit input size for QA model
    result = qa_model(question=question, context=context)
    return result['answer']
