import fitz 
import json
from langchain_ollama import ChatOllama
from schema import BenefitPlan

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    # Most SBC data is on Page 1 and 2. Let's ONLY grab those to save time.
    text = ""
    for page in doc[:2]:
        text += page.get_text("text") # Simple text mode is faster for tables
    return " ".join(text.split())

def parse_benefits(pdf_text):
    # num_ctx=2048 is plenty for 2 pages and runs 2x faster than 4096
    llm = ChatOllama(
        model="llama3:8b-instruct-q4_K_M", 
        temperature=0,
        num_ctx=2048
    )
    
    # We give the AI a 'Shortcut' by telling it exactly where to look
    prompt = f"""
    Extract these from the insurance text:
    1. Plan Name (e.g. Plan Option 1)
    2. Overall Deductible (e.g. $500)
    3. Out-of-Pocket Max
    4. Emergency Room Cost
    5. Primary Care Visit Copay
    
    Return ONLY JSON.
    Text: {pdf_text[:5000]}
    """
    
    response = llm.invoke(prompt)
    # Clean the response in case Llama adds extra words
    clean_json = response.content.split('{')[-1].split('}')[0]
    data = json.loads("{" + clean_json + "}")
    return BenefitPlan(**data)
