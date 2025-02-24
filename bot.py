import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

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


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


# load variables from .env file into the environment
load_dotenv(dotenv_path="./.gitignore/key.env",override=True)

# retieve the API_KEY
openai_api_key = os.getenv('API_KEY')

if openai_api_key:
    logging.info("API key loaded successfully")
else:
    logging.error("API key not found, check your .env file")

client = OpenAI(api_key=openai_api_key)

user_message_with_instructions = [
    {
        "role": "system",
        "content": instruction("patient_interaction")
    },
    {
        "role": "user",
        "content" : "I've been experiencing frequent headaches and blurred vision. What might be causing these symptoms?"
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=user_message_with_instructions
)

print(response.choices[0].message.content)

