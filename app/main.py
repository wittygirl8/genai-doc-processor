from fastapi import FastAPI, UploadFile, File, Query
from app import pdf_utils, openai_client, vector_db

app = FastAPI()

# in-memory storage
chunks = []
index = None

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    pdf_path = f"static/{file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(content)

    text = pdf_utils.extract_text(pdf_path)
    global chunks
    chunks = pdf_utils.chunk_text(text)
    embeddings = vector_db.embed_chunks(chunks)
    global index
    index = vector_db.build_index(embeddings)

    return {"message": "File uploaded and indexed"}

@app.get("/ask")
async def ask_question(q: str = Query(...)):
    results = vector_db.semantic_search(q, index, chunks)
    answer = openai_client.answer_with_gpt(q, results)
    return {"answer": answer}
