import os
import json
import fitz
from langchain_ollama import ChatOllama
from schema import BenefitPlan
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "llama3:8b-instruct-q4_K_M")


def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc[:3]:
        text += page.get_text("text")
    return " ".join(text.split())


def _parse_json_from_response(text: str) -> dict:
    """Robustly extract a JSON object from LLM output, handling prose and code fences."""
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strip markdown code fences if present
    if "```" in text:
        import re
        fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if fence_match:
            return json.loads(fence_match.group(1))

    # Walk the string to find the outermost {} pair
    start = text.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in LLM response:\n{text[:300]}")

    depth = 0
    for i, ch in enumerate(text[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])

    raise ValueError(f"Unmatched braces in LLM response:\n{text[:300]}")


def parse_benefits(pdf_text: str) -> BenefitPlan:
    llm = ChatOllama(model=MODEL, temperature=0, num_ctx=2048)

    prompt = f"""Extract the following fields from this insurance document and return ONLY valid JSON with no extra text.

Required fields (use exactly these keys):
- plan_name: Name of the health insurance plan
- deductible: Individual annual deductible (e.g. "$1,500")
- out_of_pocket_max: Individual out-of-pocket maximum (e.g. "$5,000")
- emergency_room_cost: Cost for an ER visit (e.g. "$250 copay")
- primary_care_visit: Cost for a primary care visit (e.g. "$25 copay")
- specialist_visit: Cost for a specialist visit (e.g. "$50 copay"), or "Not specified"
- prescription_tier1: Tier 1 / generic drug cost (e.g. "$10 copay"), or "Not specified"

Return ONLY a JSON object. No markdown, no explanation.

Insurance document text:
{pdf_text[:5000]}

JSON:"""

    response = llm.invoke(prompt)

    try:
        data = _parse_json_from_response(response.content)
    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to parse LLM extraction output: {e}") from e

    return BenefitPlan(**data)
