# ashvinAI-assignment

This project is designed to classify a set of documents using a machine learning approach. It utilizes PDF documents and employs the power of large language models (LLMs) for classification. The implementation is built with Python and utilizes the LangChain framework alongside Ollama to interact with the LLM.

## Project Overview

The primary objectives of this project are to:

1. **Classify all documents** in a specified folder into predefined categories.
2. **Store the classification results** in a structured format for easy verification and integration into other software systems.

## Implementation Overview

1. The application requires a running llama model on the host. llava:7b is recommended, since it is small in size to run locally, and provides good performance.
2. The main entry point of the application is "__init__.py" file.
3. Setup the database connection to postgres and bootstrapped the database to create a new table with the provided schema.
4. Within "classification.py" resides the main logic
   1. Unzip the provided ZIP file containing the pdf files
   2. Iterate over each file and read the text of the pdf
   3. Store the fileName, text and base64 encoded images of pdf in the postgres db
   4. Iterate over each record in the db using a cursor
   5. Connect to LLM model using ollama Client
   6. Pass a properly structured "input prompt" to the model along with the text and images of the record and get the classification response from the model
   7. Update the "category" column of the record with the received classification
   8. Create a JSON file, containing the mapping of [FileName]:[Classification]

## Requirements

- **Python 3.x**
- **Docker** and **Docker Compose**
- Ollama llava:7b model (run on host).

## Getting Started

To get started with the project, follow these steps:

1. ```ollama pull llava:7b```
2. ```ollama serve```
3. ```docker compose up -d``` (in the project directory)
