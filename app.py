from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import os

# Load environment variables
load_dotenv()

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

# Print AI response
review = response.output_text
print(review)
with open("resume_review.md", "w") as file:
    file.write(review)
print("\n✅ Review saved as resume_review.md")