# Project SUMMARY & RAG CHAT

Hey, I'm Dany! In this project, I propose to build an application that allows you to get the summary of a PDF and ask questions about that summary. This app is powered by a foundation model that runs locally within a Docker container, alongside a RAG (Retrieval-Augmented Generation) solution that uses Chroma as the database for storing embeddings and documents.

# Features
PDF Summarization: Upload a PDF, and the app will generate a concise summary of its content.

Ask Questions: After summarizing the document, you can ask the app questions related to the summary, and it will provide relevant answers.

Local Model: The app runs locally, ensuring privacy and fast responses.

Dockerized Environment: The entire system is containerized in Docker for easy deployment and setup.

Chroma Database: Chroma is used to store and retrieve embeddings of the documents for accurate similarity-based question answering.

# Tech Stack
Python: The main programming language used for processing PDFs, generating embeddings, and handling the question-answering logic.

Docker: Used to containerize the app and all its dependencies.

Chroma DB: A vector database to store embeddings and documents for efficient retrieval and question answering.

Transformers: Pre-trained language models (e.g., GPT, BERT, etc.) used for text generation and summarization.

Flask (or any web framework of your choice): To create a simple web interface to interact with the app.

# Setup and Installation
Prerequisites
Docker

Python 3.x
