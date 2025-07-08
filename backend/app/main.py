from fastapi import FastAPI, UploadFile, File, Query
from app import pdf_utils, openai_client, vector_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# in-memory storage
chunks = []
index = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the GenAI Doc Processor API"}

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
# @app.get("/ask")
# async def ask_question(q: str = Query(...)):
#     if index is None or not chunks:
#         return {"error": "No document uploaded or indexed yet. Please upload a PDF first."}
#     results = vector_db.semantic_search(q, index, chunks)
#     answer = openai_client.answer_with_gpt(q, results)
#     return {"answer": answer}

@app.get("/ask")
async def ask_question(q: str = Query(...)):
    if index is None or not chunks:
        return {"error": "Please upload a document first."}
    
    if "summary" in q.lower():
        context_text = "\n".join(chunks)
        return {"summary": openai_client.summarize_text(context_text)}
    
    # Otherwise: perform semantic search + QnA
    top_chunks = vector_db.semantic_search(q, index, chunks)
    answer = openai_client.answer_with_qa(q, top_chunks)
    return {"answer": answer}