import zipfile
import os
from pdf2image import convert_from_path
import json
import pytesseract
from langchain_community.document_loaders import PyPDFLoader
from db import add_document
import ollama

def unzip_file(zip_path, extract_to):
    os.makedirs(extract_to, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def load_pdfs(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            text = extract_text_from_pdf(os.path.join(folder_path, file))
            text = text.strip()
            add_document(text, file)
            print(f'Added document {file} to database')
            

def extract_text_from_pdf(file_path):
    loader = PyPDFLoader(file_path)
    text_documents = loader.load()
    texts = ""
    for text in text_documents:
        texts+=text.page_content


    images = convert_from_path(file_path)

    for _, image in enumerate(images, start=1):
        page_text = pytesseract.image_to_string(image)
        texts+="\n" + page_text
    
    return texts

def store_documents():
    zip_path = './Deidentified Claims.zip'
    extract_to = '.'
    folder_path='./Deidentified Claims'

    unzip_file(zip_path, extract_to)
    load_pdfs(folder_path)

def classify_documents(cursor):
    classified_documents = {}
    for row in cursor:
        content = row.content
        file_name = row.file_name

        input_prompt = f"""You are an AI model trained to classify **content** into specific categories. Your task is to determine the most appropriate **category** for the given content based solely on its **content**. 

        **Instructions:**
        1. Read the **content** carefully.
        2. Select the **category** that best matches the **content**.

        ----------------------Start of the **content**----------------------
        {content}
        ----------------------End of the **content**----------------------

        Select a single best matching category from the following
        - Order
        - Sleep Study Report
        - Physician Notes
        - Delivery Ticket
        - Prescription
        - Compliance Report

        Respond with **only** the **category name** and nothing else. 
        I will be using the provided name to map the **content** to the **category** thus, make sure the **category name** is exactly from one of the provided categories.
        """

        response = ollama.generate(model=os.getenv('LLM_MODEL'), prompt=input_prompt)
        print(f"File Name {file_name}, Classification: {response['response']}")
        classified_documents[file_name] = response['response']

    with open('classified_documents.json', 'w') as f:
        json.dump(classified_documents, f, indent=4)



