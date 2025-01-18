from gpt_service import extract_details_with_gpt
from gpt_service import evaluate_resume
from gpt_service import append_to_excel
from ocr_service import analyze_read_return
import json
import os

# Specify the directory path
directory_path = 'sample_resumes'

# Get a list of files and directories
files_and_directories = os.listdir(directory_path)

# Filter for only files
files = [f for f in files_and_directories if os.path.isfile(os.path.join(directory_path, f))]
files = [(os.path.join(directory_path, f)) for f in files ]

if __name__ == "__main__":
     # List of resume file paths (you can dynamically collect them from a directory)
    resume_files = files
    
    file_path = "parsed_resumes.xlsx"
    
    for file in resume_files:
        with open(file, "rb") as f:
            extracted_text = analyze_read_return(f)
        # Extract details using GPT
        extracted_details = extract_details_with_gpt(extracted_text)
        print(f"Processing on {file}")
        """ used for batch processing for updating data from multiple resuems at a time """
        try:
            cleaned_details = extracted_details.strip("```json").strip("```").strip()
            details_dict = json.loads(cleaned_details)

            # evaluating the resume for scores
            scores_response = evaluate_resume(extracted_text)
            clean_scores = scores_response.strip("```json").strip("```").strip()
            scores = json.loads(clean_scores)  
            
            details_dict["Gen-AI Experience Score"] = scores.get("gen_ai_experience_score", {}).get("score", 0)
            details_dict["AI/ML Experience Score"] = scores.get("ai_ml_experience_score", {}).get("score", 0)
            details_dict["Overall Score"] = scores.get("overall_score", {}).get("score",0)
            details_dict["Suggestions for improvement"] = scores.get("Suggestions", "")
        
            header = list(details_dict.keys())
            data_row = [list(details_dict.values())]
            # Append data to the Excel file
            append_to_excel(file_path, data_row, header)

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print("Extracted text was:")
            print(extracted_details)