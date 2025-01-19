# Generative AI-Powered Resume Analyzer 
This project is a tool for extracting structured information from resumes using AI models. The application supports batch processing of resumes and saves the analysis in an Excel file. It uses OpenAI's GPT for extracting insights from resume text.

### Features
- Upload and process multiple resumes (PDF format).
- Extract essential details like name, contact information, education, skills, and more.
- Calculate scores for General AI Experience and AI/ML Experience.
- Save analyzed results in an Excel file for easy sharing and review.

### Prerequisites
Before running the project, ensure you have the following:
- Python: Version 3.10 or higher.
- Python IDE of your choice
- Virtual Environment: Recommended to keep dependencies iinsolated.
- API Key: OpenAI API key for GPT services and Azure API key fro document intelligence. (Available in zip folder or you may create your own)<br>
(If you are using your own API key, then update Azure doc-intelligence endpoint)

## Setup Instructions
### 1. Clone the Repository
Clone the repository to your local system:
```bash
git clone https://github.com/Mohanty-Hitesh-4495/Generative_AI-Powered_Resume_Analyzer.git
```
### 2. Create a Virtual Python Environment
However, a virtual Python environment (venv) is not necessary to run this project. 
It is recommended to use a virtual environment as ngrok and other packages are 
specific to this project and may clash with other versions.
<br>To create a new python venv. First, open the cloned repo in your favourite IDE
and open the terminal. Run this command while being in the project's directory.
```shell
python -m venv venv
```
Now, that the venv is created with the name 'venv'. Activate it using a specific command for your OS:
<br>MacOS `source activate venv/bin/activate`
<br>Windows (in CMD) `env/Scripts/activate.bat`
<br>Windows (in powershell) `env/Scripts/Activate.ps1`

### 3. Install dependencies
Install the required packages for this project. Run:
```bash
pip install -r requirements.txt
```
### 4. Set Up API Keys
- Create a `.env` file in the root directory of the project if it doesn't already exist.
- Add your API keys to the `.env` file in the following format:
```bash
OPENAI_API_KEY=your_openai_api_key
AZURE_API_KEY=your_other_api_key
```
- The code will automatically load the keys from the `.env` file when running the application.

## Running the Project
### 1. Run the Streamlit Application
To start the application, run the `app.py` script using the following command:
```bash
streamlit run app.py
```
### 2. Upload Resumes and View Output
- Upload resumes in PDF format only.
- The processed results are saved/updated in the analyzed_resumes.xlsx file.
- You can also download the results directly from the application interface.

### Folder Structure
The final Project Structure should look like this:
```
|
|-- sample_resumes/        # Directory for storing resume files
|-- output_files/          # Directory for saving analyzed Excel files
|-- app.y                  # Streamlit application 
|-- batch_processing.py    # Main script for batch processing resumes
|-- gpt_service.py         # Script for GPT-based resume text processing
|-- ocr_service.py         # Script for AZURE Document Intelligence
|-- requirements.txt       # Python dependencies
|-- README.md              # Project documentation
|-- .gitignore
|-- langchain_scoring.py   # langchain code for scoring resumes (in progress)
```

#### Thank you for checking out my project. 😃
