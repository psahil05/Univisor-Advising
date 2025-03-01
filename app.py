import os
import json
import openai
from openai import OpenAI
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
client = OpenAI()

# Set OpenAI API Key (Replace with your actual API key)
OPENAI_API_KEY = "your-api-key-here"
openai.api_key = OPENAI_API_KEY

# ✅ Function to get ChatGPT response
def chatgpt_response(prompt, model="gpt-4-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI academic advisor."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ✅ Generate class schedule
def generate_schedule(student_profile):
    prompt = f"""
    Given the following student profile: {json.dumps(student_profile)},
    generate an optimized, conflict-free class schedule considering prerequisites, course availability,
    and degree requirements.
    """
    return chatgpt_response(prompt)

# ✅ Recommend courses based on career goals
def recommend_courses(student_interests, career_goals):
    prompt = f"""
    Given student interests: {student_interests} and career goals: {career_goals},
    recommend elective and major courses that align with their academic and professional aspirations.
    """
    return chatgpt_response(prompt)

# ✅ Track progress based on transcript
def track_progress(student_transcript):
    prompt = f"""
    Based on this student transcript: {json.dumps(student_transcript)},
    evaluate graduation progress, missing requirements, and provide GPA improvement suggestions.
    """
    return chatgpt_response(prompt)

# ✅ Train the AI using fine-tuning data
def train_ai(training_data):
    fine_tune_data = []
    for data in training_data:
        fine_tune_data.append({
            "messages": [
                {"role": "system", "content": "You are an AI academic advisor."},
                {"role": "user", "content": data["input"]},
                {"role": "assistant", "content": data["output"]}
            ]
        })
    
    with open("fine_tune_data.jsonl", "w") as f:
        for entry in fine_tune_data:
            f.write(json.dumps(entry) + "\n")
    
    return "Training data prepared. Upload to OpenAI's fine-tuning API."

# ✅ Fix: Serve AIad.html using a **relative path**
@app.route('/')
def index():
    file_path = os.path.join(os.getcwd(), "AIad.html")  # Get the file in the current directory
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return jsonify({"error": "AIad.html not found"}), 404  # Return error if file is missing

# ✅ API endpoint for chat
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    response_text = chatgpt_response(prompt)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
