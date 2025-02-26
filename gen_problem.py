import openai
import json
from dotenv import load_dotenv

# Load JSON data
def load_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Function to generate JSON-structured problems
def generate_problem(data, problem_id=0):
    page = data["page"]
    key_point = data["key_point"]
    problem_type = data["problem_type"]
    content = " ".join(data["content"])  # Merge content list into a single string

    if problem_type == "multiple_choice":
        prompt = (
            f"Generate a multiple-choice question with 5 choices based on the following content and key points:\n\n"
            f"Content: {content}\n"
            f"Key points: {key_point}\n\n"
            f"Return the problem in this JSON format:\n"
            f'{{"id": {problem_id}, "title": "{key_point}", "problem": "<question_text>", '
            f'"choices": {{"A": "<choice 1>", "B": "<choice 2>", "C": "<choice 3>", "D": "<choice 4>", "E": "<choice 5>"}}, '
            f'"answer": "<correct choice (A/B/C/D/E)>"}}, without explanation.'
        )
    else:  # O/X problem
        prompt = (
            f"Generate a True/False (O/X) question based on the following content and key points:\n\n"
            f"Content: {content}\n"
            f"Key points: {key_point}\n\n"
            f"Return the problem in this JSON format:\n"
            f'{{"id": {problem_id}, "title": "{key_point}", "problem": "<statement_text> (O/X)", "answer": "<O/X>"}}, '
            f'without explanation.'
        )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        problem_json = json.loads(response["choices"][0]["message"]["content"])
        return problem_json
    except json.JSONDecodeError:
        print(f"Error decoding JSON for problem ID {problem_id}")
        return None

# -------------------------------------------------

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Example usage
data = load_json("sample.json")
generated_problem = generate_problem(data, problem_id=1)

# Save the generated problem to a JSON file
if generated_problem:
    with open("generated_problem.json", "w", encoding="utf-8") as f:
        json.dump(generated_problem, f, ensure_ascii=False, indent=4)

    print("Problem generated and saved to generated_problem.json")
