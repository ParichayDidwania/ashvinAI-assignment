import zipfile
import os
from pdf2image import convert_from_path
from io import BytesIO
import json
from langchain_community.document_loaders import PyPDFLoader
from db import add_document, update_document_category_by_id
import base64
from ollama import Options

def unzip_file(zip_path, extract_to):
    os.makedirs(extract_to, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def load_pdfs(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            text, byteImages = extract_text_from_pdf(os.path.join(folder_path, file))
            text = text.strip()
            add_document(text, file, byteImages)
            print(f'Added document {file} to database')

def pdf_to_images_bytes(images):
    image_bytes_list = []
    for image in images:
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        image_bytes_list.append(base64.b64encode(img_byte_arr.getvalue()).decode('utf-8'))

    return image_bytes_list

def extract_text_from_pdf(file_path):
    loader = PyPDFLoader(file_path)
    text_documents = loader.load()
    texts = ""
    for text in text_documents:
        texts+=text.page_content    

    images = convert_from_path(file_path)
    byteImages = pdf_to_images_bytes(images)
    
    return texts, byteImages

def store_documents():
    zip_path = './Deidentified Claims.zip'
    extract_to = '.'
    folder_path='./Deidentified Claims'

    unzip_file(zip_path, extract_to)
    load_pdfs(folder_path)

def classify_documents(cursor, client):
    classified_documents = {}
    categories = ['Order', 'Sleep Study Report', 'Physician Notes', 'Delivery Ticket', 'Prescription', 'Compliance Report']
    total = 0
    correct = 0
    for row in cursor:
        id = row.id
        content = row.content
        file_name = row.file_name
        images = row.images

        input_prompt = f"""You are an AI model trained to classify **content** into specific categories. Your task is to determine the most appropriate **category** for the given content based solely on its **content** and the provided images.
        Please follow these **instructions carefully**:
        1. Read the **content** carefully and focus on the provided details.
        2. Analyze the provided image(s) carefully, if any.
        3. Select **only one** category that best matches the **content**.

        **Categories:**
        - **Order**: The content will mention items, their quantity, and item names (e.g., equipment, services).
        - **Sleep Study Report**: The content will be related to sleep study reports and sleep-related information.
        - **Physician Notes**: The content will include notes by a physician, such as medical history, medications, etc.
        - **Delivery Ticket**: The content will include details of delivery items, including quantities and items, and may mention "Delivery Receipt."
        - **Prescription**: The content will contain prescription details, including medication names, dosage, frequency, and duration.
        - **Compliance Report**: The content will contain patient compliance information, such as hours of equipment use.

        **Important Notes:**
        - Only provide one of the following **categories** as your response: 
        - Order
        - Sleep Study Report
        - Physician Notes
        - Delivery Ticket
        - Prescription
        - Compliance Report

        You are required to return **only the category name** (e.g., "Order", "Sleep Study Report") and nothing else.

        ----------------------Start of the **content**----------------------
        {content}
        ----------------------End of the **content**----------------------

        Make sure to return only the **category name** based on the **content** and **images**, nothing else.
        """

        response = client.generate(model=os.getenv('LLM_MODEL_FOR_CLASSIFICATION'), prompt=input_prompt, images=images, options=Options(temperature=0.2))
        print(f"File Name: {file_name} | Classification: {response['response']}")

        total += 1
        parsedFileName = file_name.split(" ")
        parsedFileName = parsedFileName[:-1]
        parsedFileName = " ".join(parsedFileName)

        if response['response'] == parsedFileName:
            correct += 1

        if (response['response'] not in categories):
            print(f"Invalid category: {response['response']}")
            continue

        classified_documents[file_name] = response['response']
        update_document_category_by_id(id, response['response'])

    print(f"Accuracy: {correct * 100/total}%")
    with open('classified_documents.json', 'w') as f:
        json.dump(classified_documents, f, indent=4)



