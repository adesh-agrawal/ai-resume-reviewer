from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import os
import json

# Load environment variables
load_dotenv()
#Ask user which resume to review?
resume_name = input("Enter resume filename (example: AdeshAgrawal_SPM.pdf): ")

# File Paths
RESUME_FILE = "Resumes/AdeshAgrawal_SPM.pdf"
PROMPT_FILE = "prompt.txt"

# Read the resume pdf
reader = PdfReader(RESUME_FILE)

resume_text = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        resume_text += text + "\n"

# Read the prompt template
with open("prompt.txt", "r") as file:
    prompt_template = file.read()

# Replace {resume} with the actual resume
    final_prompt = prompt_template.format(
    resume=resume_text
)

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Call GPT
response = client.responses.create(
    model="gpt-5",
    input=final_prompt,
)

# Print AI response as JSON
review = response.output_text
review_json = json.loads(review)

# Create Outputs folder if needed
os.makedirs("Outputs", exist_ok=True)

# Save JSON
with open("Outputs/review.json", "w") as file:
    json.dump(review_json, file, indent=4)

# Pretty Print
print("\n")
print("=" * 60)
print("          AI RESUME REVIEW")
print("=" * 60)

print(f"\nATS Score : {review_json['ats_score']}")
print(f"AI Readiness : {review_json['ai_readiness']}")

print("\nExecutive Summary")
print(review_json["executive_summary"])

print("\nTop Strengths")
for item in review_json["strengths"]:
    print(f"• {item}")

print("\nTop Weaknesses")
for item in review_json["weaknesses"]:
    print(f"• {item}")

print("\nMissing Keywords")
for item in review_json["missing_keywords"]:
    print(f"• {item}")

print("\nResume Improvements")
for item in review_json["resume_improvements"]:
    print(f"• {item}")

print("\nInterview Questions")

for i, question in enumerate(review_json["interview_questions"], start=1):
    print(f"\n{i}. {question['question']}")
    print(f"   Why: {question['why_it_is_asked']}")

print("\nRecommendation")
print(review_json["recommendation"])

print("\n")
print("=" * 60)
print("Review saved successfully!")
print("Location: Outputs/review.json")
print("=" * 60)