import os
import fitz
from langchain_ollama import ChatOllama

def turbo_genie():
    # 1. SETUP
    pdf_path = os.path.join("data", "sample_plan.pdf")
    user_scenario = "I have a chronic condition, visit my doctor monthly, and want low copays."
    
    print("🚀 Initializing Agentic Document Intelligence Architect...")


    if not os.path.exists(pdf_path):
        print("❌ Error: Put 'sample_plan.pdf' in the 'data' folder.")
        return

    # 2. FAST EXTRACTION (First 2 pages only)
    print("📄 Reading PDF...")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc[:2]:
        text += page.get_text()
    clean_text = " ".join(text.split())[:4000] # Very short for speed

    # 3. DIRECT REASONING (No JSON = Much Faster)
    print("🧠 Analyzing (Privacy Secured)...")
    
    # We use a very low 'num_ctx' to keep your RAM free
    llm = ChatOllama(model="llama3:8b-instruct-q4_K_M", temperature=0, num_ctx=2048)
    
    prompt = f"""
    You are a Senior Benefits Consultant. Read this insurance text and answer the user's need.
    
    USER NEED: {user_scenario}
    INSURANCE TEXT: {clean_text}
    
    TASK:
    1. What is the Plan Name?
    2. What is the Deductible?
    3. Is this plan good for someone with monthly doctor visits? Why?
    """
    
    response = llm.invoke(prompt)
    
    print("\n" + "="*60)
    print("                FINAL ARCHITECT REPORT")
    print("="*60)
    print(response.content)
    print("="*60)

if __name__ == "__main__":
    turbo_genie()
