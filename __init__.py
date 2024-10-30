from dotenv import load_dotenv
load_dotenv()

from db import bootstrap_database, useCursorForExecution
bootstrap_database()
print('Database Connected\n')

from classification import store_documents, classify_documents
store_documents()
print('Documents Stored\n')

from ollama import Client
import os

client = Client(host=f"http://{os.getenv('OLLAMA_HOST')}:{os.getenv('OLLAMA_PORT')}")

useCursorForExecution(classify_documents, client)
print('Documents Classified')
