from gpt_service import extract_details_with_gpt
from gpt_service import evaluate_resume
from gpt_service import append_to_excel
from ocr_service import analyze_read_return
import streamlit as st
import json
import os
import time

def process_resumes(resume_files, output_file):
    process_no = 1
    status_placeholder = st.empty() 
    for file in resume_files:
        status_placeholder.info(f"⏳ Processing {process_no}/{len(resume_files)}")
        process_no += 1
        with open(file, "rb") as f:
            extracted_text = analyze_read_return(f)

        print(f"Processing {file}")
        
        try:
            # Extract details using GPT
            extracted_details = extract_details_with_gpt(extracted_text)
            cleaned_details = extracted_details.strip("```json").strip("```").strip()
            details_dict = json.loads(cleaned_details)
            # Evaluate the resume for scores
            scores_response = evaluate_resume(extracted_details)
            time.sleep(20)  # Respect API rate limits
            clean_scores = scores_response.strip("```json").strip("```").strip()
            scores = json.loads(clean_scores)
            
            # Combine details and scores
            details_dict["Gen-AI Experience Score"] = scores.get("gen_ai_experience_score", {}).get("score", 0)
            details_dict["AI/ML Experience Score"] = scores.get("ai_ml_experience_score", {}).get("score", 0)
            details_dict["Overall Score"] = scores.get("overall_score", {}).get("score", 0)
            
            # Prepare data for Excel
            header = list(details_dict.keys())
            data_row = [list(details_dict.values())]
            
            # Append data to the Excel file
            append_to_excel(output_file, data_row, header)
        
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print("Extracted text was:")
            print(extracted_details)

    print("All Resumes are analyzed successfully! you may download excel sheet.")

if __name__ == "__main__":
    # Specify the directory path
    directory_path = 'sample_resumes'

    # Get a list of files and directories
    files_and_directories = os.listdir(directory_path)

    # Filter for only files
    files = [f for f in files_and_directories if os.path.isfile(os.path.join(directory_path, f))]
    files = [(os.path.join(directory_path, f)) for f in files ]
    
    # Replace with actual file paths
    process_resumes(files[:1], "output_files/analyzed_resumes.xlsx")