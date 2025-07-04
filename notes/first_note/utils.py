from transformers import pipeline
import fitz  # PyMuPDF

# Load summarization model only once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def summarize_text(text):
    # HuggingFace models have input length limits (1024 tokens for BART)
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = ""

    for chunk in chunks[:3]:  # Limit to first 3 chunks to avoid long response
        result = summarizer(chunk, max_length=120, min_length=30, do_sample=False)
        summary += result[0]['summary_text'] + "\n\n"
    return summary.strip()


def answer_question_from_text(full_text, question):
    detailed_question = f"Answer in detail: {question}"
    result = qa_model({
        "context": full_text[:4000],
        "question": detailed_question
    })
    answer = result['answer'].strip()
    # If answer is empty or too short, show a better message
    if not answer or len(answer.split()) < 5:
        return "Sorry, I couldn't find a detailed answer. Try rephrasing your question or make sure the note contains relevant information."
    return answer
