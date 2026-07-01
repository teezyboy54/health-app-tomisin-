import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
# Note: You need to set OPENAI_API_KEY in your .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))

import json

GENERAL_KNOWLEDGE_BASE = """
You are a specialized medical AI assistant focusing on General Health and Disease Diagnosis. 
Your goal is to suggest drugs, solutions, and doctors to talk to based on symptoms, as well as the nearest hospital based on the user's location.
Always include a disclaimer that you are an AI and the user should consult real-life doctors.

Respond ONLY with a valid JSON object matching this schema:
{
    "disease_name": "Name of the condition",
    "hospital_name": "Name of a recommended hospital nearby",
    "hospital_address": "Address of the hospital",
    "hospital_contact": "Contact number",
    "recommended_drugs": ["Drug 1", "Drug 2"],
    "solutions": ["Solution 1", "Solution 2"],
    "doctors_to_talk_to": ["Doctor Specialty 1", "Doctor Specialty 2"]
}
"""

def get_ai_response(symptoms: str, location: str):
    try:
        # Basic validation: check if symptoms contains letters and is not just gibberish
        clean_symptoms = "".join([c for c in symptoms if c.isalpha()])
        if len(clean_symptoms) < 3:
            raise ValueError("The symptom description is too short or invalid. Please describe how you feel in detail.")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": GENERAL_KNOWLEDGE_BASE},
                {"role": "user", "content": f"Symptoms: {symptoms}\nLocation: {location}"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return json.loads(response.choices[0].message.content)
    except ValueError as e:
        raise e
    except Exception as e:
        print(f"OpenAI API error (falling back to mock): {e}")
        return get_mock_ai_response(symptoms, location)

def get_mock_ai_response(symptoms: str, location: str):
    # Basic validation: check if symptoms contains letters and is not just gibberish
    clean_symptoms = "".join([c for c in symptoms if c.isalpha()])
    if len(clean_symptoms) < 3:
        raise ValueError("The symptom description is too short or invalid. Please describe how you feel in detail.")

    symptoms_lower = symptoms.lower()
    
    # Common sicknesses
    if "headache" in symptoms_lower or "migraine" in symptoms_lower or "head" in symptoms_lower:
        disease = "Tension Headache / Migraine"
        drugs = ["Ibuprofen (Advil)", "Acetaminophen (Tylenol)", "Aspirin"]
        solutions = ["Rest in a quiet, dark room", "Stay hydrated", "Apply a cold or warm compress", "Manage stress"]
        doctors = ["General Practitioner", "Neurologist"]
    elif "cough" in symptoms_lower or "sore throat" in symptoms_lower or "cold" in symptoms_lower or "runny nose" in symptoms_lower or "congestion" in symptoms_lower or "throat" in symptoms_lower:
        disease = "Common Cold / Viral Infection"
        drugs = ["Cough syrup (Dextromethorphan)", "Lozenges", "Decongestants (Pseudoephedrine)"]
        solutions = ["Drink warm fluids (tea with honey)", "Get plenty of rest", "Gargle with salt water"]
        doctors = ["General Practitioner"]
    elif "fever" in symptoms_lower or "chills" in symptoms_lower or "body ache" in symptoms_lower or "temperature" in symptoms_lower or "temp" in symptoms_lower or "hot" in symptoms_lower or "sweat" in symptoms_lower or "feverish" in symptoms_lower:
        disease = "Influenza (Flu) / Viral Fever"
        drugs = ["Acetaminophen (Tylenol)", "Ibuprofen", "Antiviral drugs (if prescribed)"]
        solutions = ["Get plenty of rest", "Drink fluids", "Use a cool compress to reduce fever"]
        doctors = ["General Practitioner", "Infectious Disease Specialist"]
    elif "sneeze" in symptoms_lower or "allergy" in symptoms_lower or "itch" in symptoms_lower or "watery eyes" in symptoms_lower or "allergies" in symptoms_lower or "hay fever" in symptoms_lower:
        disease = "Allergic Rhinitis (Allergies)"
        drugs = ["Antihistamines (Loratadine, Cetirizine)", "Nasal sprays (Fluticasone)", "Decongestants"]
        solutions = ["Avoid known allergens", "Keep windows closed during high pollen seasons", "Use an air purifier"]
        doctors = ["Allergist", "General Practitioner"]
    # Gastrointestinal disorders
    elif "acid" in symptoms_lower or "burn" in symptoms_lower or "heartburn" in symptoms_lower or "reflux" in symptoms_lower or "indigestion" in symptoms_lower:
        disease = "GERD (Gastroesophageal Reflux Disease)"
        drugs = ["Omeprazole (Prilosec)", "Antacids (Tums, Rolaids)", "Famotidine (Pepcid)"]
        solutions = ["Avoid spicy and acidic foods", "Eat smaller meals", "Don't lie down right after eating"]
        doctors = ["Gastroenterologist"]
    elif "ulcer" in symptoms_lower or ("pain" in symptoms_lower and "stomach" in symptoms_lower) or "tummy" in symptoms_lower or "abdominal" in symptoms_lower:
        disease = "Peptic Ulcer / Stomach Gastritis"
        drugs = ["Proton Pump Inhibitors (PPIs)", "Antibiotics (if H. pylori is present)", "Antacids"]
        solutions = ["Avoid NSAID pain relievers", "Reduce stress", "Avoid alcohol and smoking"]
        doctors = ["Gastroenterologist", "Internal Medicine"]
    elif "constipation" in symptoms_lower or "bloating" in symptoms_lower or "gas" in symptoms_lower or "cramp" in symptoms_lower:
        disease = "Irritable Bowel Syndrome (IBS)"
        drugs = ["Fiber supplements", "Laxatives", "Antispasmodic medications"]
        solutions = ["Increase dietary fiber", "Exercise regularly", "Manage stress levels"]
        doctors = ["Gastroenterologist", "Dietitian"]
    elif "diarrhea" in symptoms_lower or "vomit" in symptoms_lower or "nausea" in symptoms_lower or "food poisoning" in symptoms_lower:
        disease = "Gastroenteritis (Stomach Flu) / Food Poisoning"
        drugs = ["Loperamide (Imodium)", "Bismuth subsalicylate (Pepto-Bismol)", "Oral Rehydration Salts (ORS)"]
        solutions = ["Drink plenty of fluids to avoid dehydration.", "Eat bland, easy-to-digest foods (BRAT diet).", "Get plenty of rest."]
        doctors = ["General Practitioner", "Internal Medicine Specialist"]
    elif "dizzy" in symptoms_lower or "lightheaded" in symptoms_lower or "vertigo" in symptoms_lower or "faint" in symptoms_lower:
        disease = "Mild Vertigo / Dehydration"
        drugs = ["Oral Rehydration Salts (ORS)", "Meclizine (for vertigo if prescribed)"]
        solutions = ["Drink plenty of fluids", "Rest and avoid sudden head movements", "Sit or lie down immediately when feeling dizzy"]
        doctors = ["General Practitioner", "ENT Specialist"]
    elif "rash" in symptoms_lower or "skin" in symptoms_lower or "redness" in symptoms_lower or "spots" in symptoms_lower or "dermatitis" in symptoms_lower:
        disease = "Contact Dermatitis / Skin Rash"
        drugs = ["Hydrocortisone cream", "Antihistamines", "Calamine lotion"]
        solutions = ["Avoid scratching the affected area", "Wash skin with mild soap and cool water", "Identify and avoid potential allergens"]
        doctors = ["Dermatologist", "General Practitioner"]
    elif "back" in symptoms_lower or "muscle" in symptoms_lower or "joint" in symptoms_lower or "strain" in symptoms_lower or "stiff" in symptoms_lower:
        disease = "Musculoskeletal Strain / Muscle Pain"
        drugs = ["Ibuprofen (Advil)", "Acetaminophen", "Topical pain relief gels (e.g. Voltarol)"]
        solutions = ["Apply a warm compress or ice pack", "Rest the affected muscle/joint", "Gentle stretching and avoid heavy lifting"]
        doctors = ["Physiotherapist", "General Practitioner"]
    else:
        disease = "General Symptom Discomfort / General Health Query"
        drugs = ["Acetaminophen (Tylenol)", "Multivitamins"]
        solutions = ["Get plenty of rest and stay hydrated", "Monitor symptoms closely for changes", "Consult a healthcare professional for a precise diagnosis"]
        doctors = ["General Practitioner"]

    return {
        "disease_name": disease,
        "hospital_name": "City General Health Center",
        "hospital_address": f"Central Medical District, near {location}",
        "hospital_contact": "+1 800-555-0199",
        "recommended_drugs": drugs,
        "solutions": solutions,
        "doctors_to_talk_to": doctors
    }


CHAT_SYSTEM_PROMPT = """
You are a specialized medical AI assistant focusing on General Health and Disease Diagnosis. 
Provide helpful, empathetic, and professional advice on common diseases, symptoms, drugs, and health measures.
Always include a clear disclaimer that you are an AI and the user must consult a real-life doctor for proper medical advice.
Keep your responses concise and directly address the user's concerns.
"""

def get_chat_response(message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": CHAT_SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error in chat (falling back to mock): {e}")
        return get_mock_chat_response(message)

def get_mock_chat_response(message: str) -> str:
    mock_data = get_mock_ai_response(message, "your location")
    
    response_text = f"Based on the symptoms you described, there is a potential match for **{mock_data['disease_name']}**.\n\n"
    
    response_text += "Here are some recommended measures/solutions you can take:\n"
    for sol in mock_data['solutions']:
        response_text += f"- {sol}\n"
    
    response_text += "\nSome common over-the-counter options or recommended drugs include:\n"
    for drug in mock_data['recommended_drugs']:
        response_text += f"- {drug}\n"
        
    response_text += f"\nIf you need to seek immediate medical attention, you can visit **{mock_data['hospital_name']}** ({mock_data['hospital_address']}).\n"
    response_text += f"You may want to consult a **{', '.join(mock_data['doctors_to_talk_to'])}**.\n\n"
    response_text += "*Disclaimer: I am an AI assistant, not a doctor. Please consult a real-life medical professional for a proper diagnosis and treatment plan.*"
    
    return response_text

