from dotenv import load_dotenv
load_dotenv()

from db import bootstrap_database, useCursorForExecution
bootstrap_database()
print('Database Connected\n')

from classification import store_documents, classify_documents
store_documents()
print('Documents Stored\n')

useCursorForExecution(classify_documents)
print('Documents Classified')
