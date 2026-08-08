import streamlit as st
from openai import OpenAI
from pypdf import PdfReader
from docx import Document
import chromadb


def read_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def read_docx(file):
    doc = Document(file)
    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text


def split_text(text, chunk_size=1000):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


client = OpenAI(
    base_url="http://127.0.0.1:52111/v1",
    api_key="foundry"
)


embedding_client = OpenAI(
    base_url="http://127.0.0.1:52111/v1",
    api_key="foundry"
)


chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="documents"
)


st.set_page_config(
    page_title="Local RAG Assistant"
)

st.title("📄 Local RAG Assistant")


uploaded_file = st.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf", "docx"]
)


question = st.text_input(
    "Ask a question about your document"
)



if st.button("Ask"):

    if uploaded_file is None:
        st.warning("Please upload a PDF or DOCX file first.")

    elif question == "":
        st.warning("Please enter a question.")

    else:

        if uploaded_file.name.endswith(".pdf"):
            document_text = read_pdf(uploaded_file)

        else:
            document_text = read_docx(uploaded_file)


        chunks = split_text(document_text)


        try:
            chroma_client.delete_collection("documents")
        except:
            pass


        collection = chroma_client.get_or_create_collection(
            name="documents"
        )


        embeddings = []

        for chunk in chunks:

            result = embedding_client.embeddings.create(
                model="qwen3-embedding-0.6b",
                input=chunk
            )

            embeddings.append(result.data[0].embedding)


        ids = []

        for i in range(len(chunks)):
            ids.append(f"chunk_{i}")


        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )


        question_embedding = embedding_client.embeddings.create(
            model="qwen3-embedding-0.6b",
            input=question
        ).data[0].embedding


        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=3
        )


        context = "\n".join(
            results["documents"][0]
        )


        prompt = f"""
Answer the question using only the context below.

If the answer is not in the context, say:
"I could not find the answer in the document."

Context:
{context}

Question:
{question}
"""


        response = client.chat.completions.create(
            model="phi-3.5-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        st.success("Answer")

        st.write(
            response.choices[0].message.content
        )