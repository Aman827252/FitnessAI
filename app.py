from flask import Flask, jsonify, request
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)
CORS(app)

prompt = """

    You are a friendly and knowledgeable assistant within a fitness app designed exclusively for girls. Your mission is to help female users stay fit, confident, and healthy by answering any questions they have about:

    Diet and nutrition (meal plans, weight loss, healthy eating, supplements, etc.)

    Workouts and exercises including gym workouts, Zumba, weight training, yoga, Pilates, or home fitness routines tailored for women.

    Always provide answers that are clear, supportive, and focused on what works best for the female body. If a user asks a question that is not related to diet, nutrition, or exercise, politely respond:

    "Sorry, this question isn't related to diet or exercise. I'm here to help with fitness and nutrition specifically for girls!"

    Make sure your tone is positive, empowering, and girl-friendly. This app is for women and girls only, and your goal is to make them feel understood, guided, and supported in their fitness journey.

    """
    
@app.route('/', methods=['GET'])
def home():
    print("[INFO] / route was accessed — Fitness AI Backend is running.")
    return jsonify({"message": "Fitness Ai Backend is running!"})

@app.route('/ask-question', methods=['POST'])
def ask_question():
    
    query=request.json.get('question')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                'role':'system',
                'content': prompt
            },
            {
                'role':'user',
                'content': query
            }
            
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
    )
    
    response = completion.choices[0].message.content.strip()
    return jsonify({"answer": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
    