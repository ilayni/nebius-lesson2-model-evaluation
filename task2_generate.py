"""Task 2: Generate product descriptions using Meta-Llama-3.1-8B-Instruct.

Usage:
    python task2_generate.py                                      # uses defaults below
    python task2_generate.py --model <model_name>                 # override model
    python task2_generate.py --output <filename.xlsx>             # override output file
    python task2_generate.py --model <model_name> --output <file> # both

Valid model names:
    meta-llama/Meta-Llama-3.1-8B-Instruct
    google/gemma-2-9b-it-fast
    Qwen/Qwen3-30B-A3B-Instruct-2507
"""

import argparse
import time

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")
if not NEBIUS_API_KEY:
    raise RuntimeError("NEBIUS_API_KEY environment variable is required. See .env")

BASE_URL = "https://api.studio.nebius.com/v1/"
# Default model — override with --model flag
# Valid options:
#   meta-llama/Meta-Llama-3.1-8B-Instruct
#   google/gemma-2-9b-it-fast
#   Qwen/Qwen3-30B-A3B-Instruct-2507
DEFAULT_MODEL = "google/gemma-2-9b-it-fast"
DEFAULT_OUTPUT = "assignment/assignment_01.xlsx"

SYSTEM_PROMPT = """You are a copywriter for an e-commerce retailer. Your job is to write persuasive product descriptions.

Rules:
- Write exactly 50–90 words. Count carefully.
- Use a friendly, credible sales tone — enthusiastic but not exaggerated.
- Base the description ONLY on the product name, attributes, material, and warranty provided. Do not invent features.
- Write in flowing prose (no bullet points or headers).
- Output only the description text, nothing else."""

SYSTEM_PROMPT_V2 = """You are a work for an e-commerce retailer. Your job is to write persuasive product descriptions.

Rules:
- Your description MUST be 50–90 words. Count every word before you finish.
  If your draft exceeds 90 words, shorten it before outputting.
  If it is under 50 words, expand it.
- Be persuasive — use a friendly, credible tone, enthusiastic but not exaggerated.
- Base the description ONLY on the product name, attributes, material, and warranty provided. Do not invent features.
- Some attributes use labels like battery:, weight:, capacity:, rating:, dimensions:, or color options: — these are
  metadata descriptors, not product features. Only mention features that make sense for the product category
  (e.g., a compact dimension does not need to be mentioned as a feature).
- Write in flowing prose (no bullet points or headers).
- Output only the description text, nothing else.

Example input:
  Product name: OnePlus 12
  Attributes: features: Snapdragon 8 Gen 3, 50 MP Hasselblad camera, 100 W SUPERVOOC charging; dimensions: sleek
  Material: silky glass back, aluminum frame
  Warranty: 1-year limited warranty

Example output:
  Meet the OnePlus 12 — a flagship that refuses to compromise. Powered by the Snapdragon 8 Gen 3,
  it blazes through every task while the 50 MP Hasselblad camera captures stunning detail in any light.
  The 100 W SUPERVOOC charging tops up the battery in minutes, not hours. Wrapped in silky glass with
  an aluminum frame, it's built to impress. Backed by a 1-year limited warranty."""


def build_user_message(row: pd.Series) -> str:
    return (
        f"Product name: {row['product_name']}\n"
        f"Attributes: {row['Product_attribute_list']}\n"
        f"Material: {row['material']}\n"
        f"Warranty: {row['warranty']}"
    )


def generate_description(client: OpenAI, user_message: str, model: str) -> dict:
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_V2},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
        #temperature=0.3,
        #top_p=0.85,     
        max_tokens=200,
    )
    latency_ms = (time.time() - start) * 1000

    return {
        "generated_description": response.choices[0].message.content.strip(),
        "latency_ms": round(latency_ms, 1),
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate product descriptions via Nebius API.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name to use for generation.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output Excel filename.")
    args = parser.parse_args()

    model = args.model
    output_file = args.output

    print(f"Model:  {model}")
    print(f"Output: {output_file}\n")

    client = OpenAI(api_key=NEBIUS_API_KEY, base_url=BASE_URL)
    products = pd.read_csv("product_dataset.csv")

    results = []
    for i, row in products.iterrows():
        print(f"[{i + 1}/{len(products)}] Generating: {row['product_name']}")
        user_msg = build_user_message(row)
        result = generate_description(client, user_msg, model)
        result["product_name"] = row["product_name"]
        result["Product_attribute_list"] = row["Product_attribute_list"]
        result["material"] = row["material"]
        result["warranty"] = row["warranty"]
        results.append(result)

    df = pd.DataFrame(results)

    # Reorder columns: product info first, then generated fields
    cols = [
        "product_name", "Product_attribute_list", "material", "warranty",
        "generated_description", "latency_ms", "input_tokens", "output_tokens",
        # Rubric criteria (blank, to be filled manually in Task 3)
        "fluency", "grammar", "tone", "length", "grounding",
        "latency_rating", "cost_rating",
        "final_score",
    ]
    for col in cols:
        if col not in df.columns:
            df[col] = ""

    df = df[cols]
    df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"\nSaved {len(df)} rows to {output_file}")


if __name__ == "__main__":
    main()
