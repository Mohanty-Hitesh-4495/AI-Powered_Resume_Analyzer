from openai import OpenAI
import pandas as pd
from openpyxl import load_workbook
from dotenv import load_dotenv
from ocr_service import analyze_read_return
import os
import json

# loading environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

openai = OpenAI(
    api_key = openai_api_key
)
def extract_details_with_gpt(resume_text):
    # defining the GPT prompt
    prompt = [
        {
            "role": "system",
            "content": "You are a helpful assistant that extracts structured information from resumes."
        },
        {
            "role": "user",
            "content": f"""
            Extract the following details from the given resume text:

            Mandatory Fields:
            - Name
            - Contact details (email, phone number)
            - University
            - Year of Study
            - Course
            - Discipline
            - CGPA/Percentage
            - Key Skills (from skills section and project & experience section)
            - Gen AI Experience Score (Keep it empty)
            - AI/ML Experience Score (Keep it empty)
            - Supporting Information (most highlighting informations e.g., certifications, internships, projects)

            Resume Text:
            {resume_text}

            Output JSON Format:
            {{
            "Name": "",
            "Email": "",
            "PhoneNumber": "",
            "University": "",
            "YearOfStudy": "",
            "Course": "",
            "Discipline": "",
            "CGPA": "",
            "KeySkills": "",
            "GenAIExperienceScore": 0,
            "AIMLExperienceScore": 0,
            "SupportingInformation": ""
            }}
            """
        }
    ]
    # calling GPT model
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  
        messages=prompt,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

# function to append data to an existing Excel file
def append_to_excel(file_path, data, header):
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active

        for row in data:
            sheet.append(row)

        workbook.save(file_path)
        print(f"Data appended to {file_path}")
    except FileNotFoundError:
        # If file does not exist, create a new file
        df = pd.DataFrame(data, columns=header)
        df.to_excel(file_path, index=False)
        print(f"New file created at {file_path}")


if __name__ == "__main__":
    path_to_doc = "Hitesh_Resume.pdf"
    with open(path_to_doc, "rb") as f:
        extracted_text = analyze_read_return(f)

    # extracting details using GPT
    extracted_details = extract_details_with_gpt(extracted_text)
    print("Extracted Details:")
    print(extracted_details)

    """ generating excel for updating data extracted from each resume """
    try:
        cleaned_details = extracted_details.strip("json").strip("").strip()
        details_dict = json.loads(cleaned_details)  # Safely parse JSON
        df = pd.DataFrame([details_dict])
        df.to_excel("parsed_resumes.xlsx", index=False)
        print("Results saved to parsed_resumes.xlsx")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print("Extracted text was:")
        print(extracted_details)

    """ used for batch processing for updating data from multiple resuems at a time """
    # cleaning and parsing the output as JSON and saving the data in Excel file
    # try:
    #     cleaned_details = extracted_details.strip("```json").strip("```").strip()
    #     details_dict = json.loads(cleaned_details)

    #     header = list(details_dict.keys())
    #     data_row = [list(details_dict.values())]

    #     file_path = "parsed_resumes.xlsx"

    #     # Append data to the Excel file
    #     append_to_excel(file_path, data_row, header)

    # except json.JSONDecodeError as e:
    #     print(f"Failed to parse JSON: {e}")
    #     print("Extracted text was:")
    #     print(extracted_details)
