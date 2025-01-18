from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from gpt_service import extract_details_with_gpt
from ocr_service import analyze_read_return
from dotenv import load_dotenv
import os

# loading environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Function to process the resume and answer questions
def process_resume(resume_text, questions):
    # Split resume into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(resume_text)

    # Embed chunks using OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    # Retrieve answers for each question
    answers = {}
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0, model_name="text-davinci-003", max_tokens=200)
    chain = load_qa_chain(llm, chain_type="stuff")

    for question in questions:
        docs = knowledge_base.similarity_search(question)
        answer = chain.run(input_documents=docs, question=question)
        answers[question] = answer

    return answers

# Function to calculate the score
def calculate_score(answers, category):
    score = 0
    for question, answer in answers.items():
        if "basic understanding" in answer.lower():
            score += 1  # Exposed
        elif "practical experience" in answer.lower():
            score += 2  # Hands-on
        elif "advanced" in answer.lower():
            score += 3  # Advanced

    max_score = len(category) * 3  # Maximum score for the category
    return score, max_score

# Function to calculate overall score
def overall_score(gen_ai_score, ai_ml_score):
    return (gen_ai_score[0] + ai_ml_score[0]) / (gen_ai_score[1] + ai_ml_score[1]) * 100

# Function to provide suggestions for improvement
def provide_suggestions(answers, category):
    suggestions = []
    for question, answer in answers.items():
        if "basic understanding" in answer.lower():
            suggestions.append(f"Gain practical experience related to: {question}")
        elif "practical experience" in answer.lower():
            suggestions.append(f"Deepen your expertise in advanced topics for: {question}")
        elif "no experience" in answer.lower() or "not mentioned" in answer.lower():
            suggestions.append(f"Start gaining experience in: {question}")
    return suggestions

# Main function
def main():

    path_to_doc = "Hitesh_Resume.pdf"
    with open(path_to_doc, "rb") as f:
        extracted_text = analyze_read_return(f)

    # extracting details using GPT
    resume_text = extract_details_with_gpt(extracted_text)
    print("Extracted Details:")
    print(resume_text) 

    # Define questions
    gen_ai_questions = [
        "Does the candidate have experience with GPT or other Generative AI models?",
        "Has the candidate worked on advanced areas like Agentic RAG or Evals?",
        "What is the candidate's exposure to prompt engineering or embeddings?"
    ]

    ai_ml_questions = [
        "What is the candidate's experience with machine learning models like regression or classification?",
        "Has the candidate implemented deep learning projects using TensorFlow or PyTorch?",
        "Has the candidate published research or worked on advanced AI topics?"
    ]

    # Process resume and calculate scores
    gen_ai_answers = process_resume(resume_text, gen_ai_questions)
    ai_ml_answers = process_resume(resume_text, ai_ml_questions)

    gen_ai_score = calculate_score(gen_ai_answers, gen_ai_questions)
    ai_ml_score = calculate_score(ai_ml_answers, ai_ml_questions)

    overall = overall_score(gen_ai_score, ai_ml_score)

    # Provide suggestions for improvement
    gen_ai_suggestions = provide_suggestions(gen_ai_answers, gen_ai_questions)
    ai_ml_suggestions = provide_suggestions(ai_ml_answers, ai_ml_questions)

    # Print results
    print(f"Generative AI Experience Score: {gen_ai_score[0]} / {gen_ai_score[1]}")
    print(f"AI/ML Experience Score: {ai_ml_score[0]} / {ai_ml_score[1]}")
    print(f"Overall Score: {overall:.2f}%\n")

    print("Suggestions for Improvement:")
    for suggestion in gen_ai_suggestions + ai_ml_suggestions:
        print(f"- {suggestion}")

# Run the main function
if __name__ == "__main__":
    main()
