from flask import Flask, send_file, request
import os
from openai import OpenAI
import re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

app = Flask(__name__)

# Ensure the API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def generate_questions(prompt):
    content = f"Generate three relevant questions that help dive deep into the topic: {prompt}."
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
    )
    generated_questions = completion.choices[0].message.content
    questions_list = [re.sub(r'^\d+\.\s*', '', question.strip()) for question in generated_questions.split('\n')]
    return questions_list

def generate_research(questions_list):
    all_text = ""
    for question in questions_list:
        content = f"Generate a detailed explanation for: {question}"
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
        )
        all_text += str(completion.choices[0].message.content)
    return all_text

def export_to_docx(text, prompt, filename):
    doc = Document()
    doc.add_heading(prompt, level=1)
    sections = text.split('Question:')
    for section in sections:
        if section.strip():
            question, content = section.split('\n', 1)
            doc.add_heading(question, level=2)
            paragraphs = content.split('\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    p = doc.add_paragraph(paragraph.strip())
                    p.style.font.size = Pt(12)
                    p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    doc.save(filename)

@app.route('/export', methods=['POST'])
def export_document():
    prompt = request.args.get('prompt')
    if not prompt:
        return "Please provide a prompt parameter.", 400
    
    questions = generate_questions(prompt)
    research = generate_research(questions)
    filename = "generated_report.docx"
    export_to_docx(research, prompt, filename)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
