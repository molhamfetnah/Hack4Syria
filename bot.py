import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
from flask import Flask, request, jsonify
import uuid
from flask_cors import CORS

load_dotenv(dotenv_path="./.gitignore/key.env", override=True)
openai_api_key = os.getenv('API_KEY')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-domain requests

client = OpenAI(api_key=openai_api_key)

# In-memory storage for conversations (use a database in production)
sessions = {}

def instruction(model):
    instruc = ""
    if (model == "triage_tool"): #Prioritization of Medical Cases
        instruc = (
            "Given the following symptoms provided by the patient, classify the urgency of the case into one of the following categories: critical, urgent, moderate, or low priority."
            "Consider the severity, potential life-threatening nature of the symptoms, and recommend the necessary immediate steps."
            "Symptoms: [user input]"
            )
    elif(model == "ai_specialist_agents"): #Medical Experts in Specific Fields
        instruc = (
            "As a [specialist name, e.g., cardiologist]"
            "Analyze the following case presented by the emergency department."
            "Based on the symptoms and initial diagnosis, provide a detailed opinion on the next steps and any urgent medical actions required."
            "Symptoms: [user input], Initial diagnosis: [diagnostics]"
            )
    elif(model == "nlp"): 
        instruc = (
            "Given the following medical notes, extract and summarize the critical details related to the patient's condition, such as diagnosis, treatment history, allergies, and any red flags that need immediate attention. Notes: [insert medical notes here]"
            )
    elif(model == "patient_interaction"): #Chatbot to Collect Symptoms
        instruc = (
            "Answer the following questions to help us understand the condition."
            "Your responses will guide the emergency team in deciding the appropriate level of care."
            "1. What are user main symptoms? 2. When did the symptoms start? 3. Do the user have any history of chronic illnesses or previous surgeries? 4. Are the user experiencing any pain, and if so, what is the intensity on a scale of 1-10?"
        )
    elif(model == "continuous_learning"): #Improvement Through Deep Learning
        instruc = (
            "Analyze the following case data and compare it to historical patient records to identify patterns and suggest improvements in triage decision-making."
            "Use the case to enhance the accuracy of predicting treatment priorities."
            "Case Data: [user input], Historical Comparison: [user historical data]"
        )
    elif(model == "iehs"): # Integration with Existing Hospital Systems (API Integration)
        instruc = (
            "Integrate the patient data from the hospital's EMR system with the AI-based triage tool."
            "Ensure that all the patient's medical history, allergies, and previous treatments are automatically populated into the triage model, and generate an immediate triage recommendation based on the patient’s current symptoms."
            "Patient Data: [user data from EMR]"
        )
    return instruc

@app.route('/start_session', methods=['POST'])
def start_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = [
        {"role": "system", "content": instruction("patient_interaction")}
    ]
    return jsonify({"session_id": session_id})

@app.route('/chat', methods=['POST'])
def handle_chat():
    data = request.get_json()
    session_id = data.get('session_id')
    user_input = data.get('user_input')

    if not session_id or not user_input:
        return jsonify({"error": "Missing parameters"}), 400

    conversation = sessions.get(session_id)
    if not conversation:
        return jsonify({"error": "Invalid session ID"}), 404

    conversation.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation,
        )
        assistant_reply = response.choices[0].message.content.strip()
        conversation.append({"role": "assistant", "content": assistant_reply})
        sessions[session_id] = conversation
        
        return jsonify({"response": assistant_reply})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)