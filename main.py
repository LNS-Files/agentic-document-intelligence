import csv
import json
import os
import sys

from dotenv import load_dotenv

from counselor import compare_plans
from extractor import extract_text_from_pdf, parse_benefits

load_dotenv()

DEFAULT_SCENARIO = os.getenv(
    "USER_SCENARIO",
    "I have a chronic condition, visit my doctor monthly, and want low copays.",
)


def run(pdf_paths: list, user_scenario: str) -> None:
    print("Agentic Document Intelligence")
    print("=" * 60)

    plans = []

    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"Warning: '{pdf_path}' not found — skipping.")
            continue

        print(f"\nProcessing: {pdf_path}")
        print("  Reading PDF...")
        pdf_text = extract_text_from_pdf(pdf_path)

        print("  Extracting benefits (local LLM — data stays on device)...")
        try:
            plan = parse_benefits(pdf_text)
            plans.append(plan)
            print(f"  Done: {plan.plan_name}")
        except ValueError as e:
            print(f"  Extraction failed: {e}")

    if not plans:
        print("\nNo plans could be extracted. Exiting.")
        sys.exit(1)

    # Print structured summary
    print("\n--- Extracted Plan Data ---")
    for plan in plans:
        print(f"\n  {plan.plan_name}")
        print(f"    Deductible        : {plan.deductible}")
        print(f"    Out-of-Pocket Max : {plan.out_of_pocket_max}")
        print(f"    ER Cost           : {plan.emergency_room_cost}")
        print(f"    Primary Care      : {plan.primary_care_visit}")
        print(f"    Specialist Visit  : {plan.specialist_visit}")
        print(f"    Rx Tier 1         : {plan.prescription_tier1}")

    # Counselor recommendation
    print("\nGenerating personalized recommendation...")
    recommendation = compare_plans([p.model_dump() for p in plans], user_scenario)

    print("\n" + "=" * 60)
    print("COUNSELOR RECOMMENDATION")
    print("=" * 60)
    print(f"Client Profile: {user_scenario}")
    print("-" * 60)
    print(recommendation)
    print("=" * 60)

    # Export results
    plans_data = [p.model_dump() for p in plans]

    with open("output.json", "w") as f:
        json.dump(plans_data, f, indent=2)
    print("\nExported: output.json")

    with open("output.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=plans_data[0].keys())
        writer.writeheader()
        writer.writerows(plans_data)
    print("Exported: output.csv")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        pdf_paths = sys.argv[1:]
    else:
        # Auto-discover all PDFs in data/ folder
        data_dir = "data"
        if os.path.isdir(data_dir):
            pdf_paths = [
                os.path.join(data_dir, f)
                for f in os.listdir(data_dir)
                if f.lower().endswith(".pdf")
            ]
        else:
            pdf_paths = []

        if not pdf_paths:
            print("Usage:  python main.py plan1.pdf plan2.pdf ...")
            print("Or place PDFs in the 'data/' folder and run: python main.py")
            sys.exit(1)

    run(pdf_paths=pdf_paths, user_scenario=DEFAULT_SCENARIO)
