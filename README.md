# ashvinAI-assignment

This project is designed to classify a set of documents using a machine learning approach. It utilizes PDF documents and employs the power of large language models (LLMs) for classification. The implementation is built with Python and utilizes the LangChain framework alongside Ollama to interact with the LLM.

## Project Overview

The primary objectives of this project are to:

1. **Classify all documents** in a specified folder into predefined categories.
2. **Store the classification results** in a structured format for easy verification and integration into other software systems.

## Requirements

- **Python 3.x**
- **Docker** and **Docker Compose**
- Ollama Llama 3.2 model (run on host).

## Getting Started

To get started with the project, follow these steps:

1. ```ollama pull llama:3.2```
2. ```ollama serve```
3. ```docker compose up -d``` (in the project directory)
