from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# --- Load API key ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    code = data.get("code", "")
    messages = data.get("messages", [])
    model = data.get("model", "gpt-4o-mini")  # Default to 4o-mini

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert software assistant. "
                    "When modifying the code, first provide a short, clear **Markdown bullet list** of the specific edits made "
                    "(3–7 concise points max). Each item should describe a unique change. "
                    "IMPORTANT: After your list, include a fenced code block (```python ... ```) containing the COMPLETE, FULL file "
                    "with all modifications applied. You MUST include the entire file from start to finish, not just the modified sections. "
                    "Preserve all existing code that wasn't changed, and include all imports, functions, and code exactly as they appear in the original, "
                    "except for the specific modifications requested.\n"
                    "When asked for explanation or reasoning, respond with Markdown-formatted plain text and no fenced code."
                ),
            },
            *messages,
            {"role": "user", "content": f"Current code:\n```python\n{code}\n```"},
        ],
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    content = file.read().decode("utf-8")
    return jsonify({"content": content, "filename": file.filename})

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    filename = data.get("filename", "main.py")
    code = data.get("code", "")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    return jsonify({"message": f"Saved as {filename}"})

if __name__ == "__main__":
    app.run(debug=True)
