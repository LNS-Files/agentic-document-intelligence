from langchain_ollama import ChatOllama

def compare_plans(extracted_data: list, user_scenario: str):
    """
    Expert system to analyze extracted plan data against user needs.
    """
    llm = ChatOllama(model="llama3:8b-instruct-q4_K_M", temperature=0.3)
    
    prompt = f"""
    You are a Senior Benefits Consultant. Analyze the following health plans 
    for an employee with this life situation: "{user_scenario}"
    
    PLAN DATA:
    {extracted_data}
    
    TASK:
    1. Identify which plan minimizes the employee's out-of-pocket costs.
    2. Explain 'Why' based on the deductible and copayments.
    3. Highlight any 'Risks' (e.g., high ER costs).
    """
    
    response = llm.invoke(prompt)
    return response.content
