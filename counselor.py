import os
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "llama3:8b-instruct-q4_K_M")


def compare_plans(extracted_data: list, user_scenario: str) -> str:
    """Analyze extracted plan data against the user's needs and return a recommendation."""
    llm = ChatOllama(model=MODEL, temperature=0.3, num_ctx=2048)

    plans_text = "\n".join(
        f"Plan {i + 1}: {plan}" for i, plan in enumerate(extracted_data)
    )

    prompt = f"""You are a Senior Benefits Consultant. A client needs help evaluating their health insurance options.

CLIENT PROFILE: {user_scenario}

AVAILABLE PLAN(S):
{plans_text}

Provide a clear, concise recommendation covering:
1. Which plan best fits this client and the primary reason why
2. The specific cost drivers (deductible, copays) that matter most for their situation
3. Any risks or hidden costs to watch out for

Be specific — reference actual dollar amounts from the plan data above."""

    response = llm.invoke(prompt)
    return response.content
