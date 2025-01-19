"""
This code sample shows Prebuilt Read operations with the Azure Form Recognizer client library. 
"""
import os
from pathlib import Path
from azure.core.credentials import AzureKeyCredential  # type: ignore
from azure.ai.formrecognizer import DocumentAnalysisClient  # type: ignore
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(".env"))
endpoint = "https://syedsadiquh-doc-intelligence.cognitiveservices.azure.com/"
key: str = str(os.getenv("AZURE_API_KEY"))


def analyze_read_print(file):
    # Read the document
    document = file.read()

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Analyze the document using the "prebuilt-read" model
    poller = document_analysis_client.begin_analyze_document(
        model_id="prebuilt-read", document=document
    )
    result = poller.result()

    # Display the extracted text content
    extracted_text = []
    for page in result.pages:
        page_content = f"Page {page.page_number}:\n"
        for line in page.lines:
            page_content += line.content + "\n"
        extracted_text.append(page_content)

    # Print the extracted text
    print("\nExtracted Text:")
    print("\n----------------------------------------")
    for text in extracted_text:
        print(text)
    print("----------------------------------------")

def analyze_read_return(file):
    document = file.read()
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    poller = document_analysis_client.begin_analyze_document(
        model_id="prebuilt-read", document=document
    )
    result = poller.result()

    # Collect all text from the document
    extracted_text = []
    for page in result.pages:
        for line in page.lines:
            extracted_text.append(line.content)

    return "\n".join(extracted_text)  # Return as a single string


if __name__ == "__main__":
    path_to_doc = "Hitesh_Resume.pdf"  # Supported formats: PNG, JPG, JPEG, PDF, DOCX, etc.
    with open(path_to_doc, "rb") as f:
        analyze_read_print(f)