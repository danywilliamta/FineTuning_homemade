import os
import asyncio

from flask import Flask, render_template, request, jsonify
from pydantic import BaseModel
from litellm import completion
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

app.config['DB_FOLDER'] = db_path = "db/"

embedding = FastEmbedEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Définit une taille max raisonnable
    chunk_overlap=50,  # Ajoute du chevauchement pour garder du contexte
    separators=["\n\n", "\n", " "],  # Coupe en priorité aux bons endroits
)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(db_path, exist_ok=True)


class ResponseModel(BaseModel):
    title: str
    summary: str


@app.route('/home', methods=['GET', 'POST'])
async def index():

    if request.method == 'POST':
        file = request.files.get('pdf')

        if file and file.filename.endswith(".pdf"):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            pdf = await get_pdf_text(file_path)

            loop = asyncio.get_event_loop()
            res = await loop.run_in_executor(None,
                process_completion,
                "ollama/llama3.2",
                [{"content": f"Summarize this text: {pdf}", "role": "user"}],
                "http://ollama:11434",
                ResponseModel
            )
            return jsonify({"summary": res['choices'][0]['message']["content"]})
    return render_template('app.html')


def process_completion(model, messages, api_base, response_format):
    response = completion(model=model, messages=messages, api_base=api_base, response_format=response_format)
    return response.json()


async def get_pdf_text(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text = ""
    store_chunks(docs)
    for doc in docs:
        text += doc.page_content + "\n"

    return text


@app.route('/chat', methods=['POST'])
async def chat():
    data = request.json
    message = data["message"]
    chatTemplate = [{"content": message, "role": "user"}]
    res = await query_chroma(message)

    if res:
        all_info = (" ".join([r.page_content for r in res]))
        prompt =  "Answer to the user's question with the following information: " + all_info
        chatTemplate.append({"content": prompt, "role": "system"})

    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None,
        process_completion,
        "ollama/llama3.2",
        chatTemplate,
        "http://ollama:11434",
        ResponseModel
    )
    return jsonify({"response": res['choices'][0]['message']["content"]})


async def query_chroma(query):

    vector_store = Chroma(persist_directory=db_path, embedding_function=embedding)
    results = vector_store.similarity_search(
        query,
        k=2,
    )
    return results


def store_chunks(docs):
    chunks = text_splitter.split_documents(docs)
    vector_store = Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=db_path)
    vector_store.persist()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
