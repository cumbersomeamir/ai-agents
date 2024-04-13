import os
from openai import OpenAI
import re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


# Attempt to read the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

#Initialising the client
client = OpenAI(api_key=api_key)

#Generate 10 questions for research
def generate_questions(prompt):
 
 
    content = f" Give only 3 relevant questions which will help diving deep into prompt of the user which is: {prompt} in the form of a python list. Don't give any extra text just the list of 10 questions"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
    )

    # Extracting the generated code from the response
    generated_questions = completion.choices[0].message.content
    
    # Converting generated text into a list of questions and removing numbers
    questions_list = [re.sub(r'^\d+\.\s*', '', question.strip()) for question in generated_questions.split('\n')]


    return questions_list
    
def generate_research(questions_list):
    all_text =""
    for question in (questions_list):
        
        content = f"This is the question {question} Please generate most relevant, skimmed,technical, comprehensive knowledge for the user"
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": content}
            ]
        )
        all_text = all_text+ str(completion)
    return all_text
    
    
def export_to_docx(text, prompt, filename="report.docx"):
    # Create a new Document
    doc = Document()
    doc.add_heading(prompt, level=1)

    # Split the text into paragraphs
    paragraphs = text.split('\n\n')
    for para in paragraphs:
        if 'Question:' in para:
            doc.add_heading(para, level=2)
        else:
            p = doc.add_paragraph(para)
            p.style.font.size = Pt(12)  # Setting font size to 12
            p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

    # Save the document
    doc.save(filename)
    print(f"Report saved as {filename}")
    
    
prompt = "What are ci/cd tools"
qs = generate_questions(prompt)
print("THE GENERATED QUESTIONS ARE:", qs)
report = generate_research(qs)
print("THE REPORT IS", report)

# Export the report to a .docx file
export_to_docx(report, prompt)

    
