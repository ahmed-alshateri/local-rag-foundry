# Local RAG with Microsoft Foundry Local

This project is part of the Microsoft Summer School.

**Author:** Ahmed Alshateri

## Project Goal

Build a local AI assistant using Retrieval-Augmented Generation (RAG) with Microsoft Foundry Local.

The application allows users to upload PDF or DOCX documents and ask questions about their content. The system retrieves the most relevant information from the document and uses a local language model to generate the answer.

## Features

* Upload PDF and DOCX documents
* Extract text from documents
* Split documents into smaller chunks
* Generate embeddings locally
* Store document embeddings in ChromaDB
* Retrieve relevant document chunks using similarity search
* Generate answers using a local Phi-3.5-mini model
* Run the entire application locally

## Technologies Used

* Python
* Streamlit
* Microsoft Foundry Local
* Phi-3.5-mini
* Qwen3 Embedding 0.6B
* ChromaDB
* OpenAI Python SDK
* PyPDF
* python-docx

## RAG Architecture

```text
Document (PDF/DOCX)
        ↓
Text Extraction
        ↓
Text Chunking
        ↓
Qwen3 Embedding Model
        ↓
ChromaDB
        ↓
Similarity Search
        ↓
Relevant Context
        ↓
Phi-3.5-mini
        ↓
Answer
```

## Example

The user can upload a CV and ask:

> What are my technical skills?

The system retrieves the relevant information from the CV and generates an answer based on the document.

## Local AI Models

### Language Model

`phi-3.5-mini`

Used to generate answers based on the retrieved document context.

### Embedding Model

`qwen3-embedding-0.6b`

Used to convert document chunks and user questions into vectors for similarity search.

## How to Run

Activate the Python virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Make sure Microsoft Foundry Local is running and the required models are loaded.

Then start the Streamlit application:

```powershell
streamlit run app.py
```

Open the local URL displayed in the terminal.

## Project Workflow

1. User uploads a PDF or DOCX document.
2. The application extracts the document text.
3. The text is divided into chunks.
4. Each chunk is converted into an embedding using Qwen3 Embedding.
5. The embeddings are stored in ChromaDB.
6. The user's question is converted into an embedding.
7. ChromaDB finds the most relevant document chunks.
8. The retrieved context is sent to Phi-3.5-mini.
9. The local model generates the final answer.

## Privacy

The project is designed to run locally using Microsoft Foundry Local. Document content is processed locally instead of being sent to an external cloud AI service.
