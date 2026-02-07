from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import json

app = Flask(__name__)

# --- SETUP ---
api_key = os.environ.get("GEMINI_API_KEY", "PASTE_KEY_HERE_IF_LOCAL")
genai.configure(api_key=api_key)

# USING YOUR WORKING MODEL
#model = genai.GenerativeModel('gemini-flash-latest')
model = genai.GenerativeModel('gemini-2.5-flash-lite')

@app.route('/')
def home():
    return "Hello! The Clinical Nutritionist AI is Online."

@app.route('/ask', methods=['GET'])
def ask_calories():
    food_item = request.args.get('food')
    
    if not food_item:
        return jsonify({"error": "No food specified"})

    # --- THE CLINICAL PROMPT ---
    # Asking for the full list: Carbs, Fats, and Micronutrients
    prompt = (
        f"Analyze this food intake: '{food_item}'. "
        f"Return a strictly valid JSON object with these exact keys (values should be numbers or strings like '5mg'): "
        f"'calories' (kcal), "
        f"'protein' (g), "
        f"'carbs' (g), "
        f"'fats' (g), "
        f"'fiber' (g), "
        f"'water_content' (ml, approx fluid intake from this food), "
        f"'vitamin_a' (ug), "
        f"'thiamin' (mg), "
        f"'riboflavin' (mg), "
        f"'niacin' (mg), "
        f"'vitamin_b6' (mg), "
        f"'vitamin_b12' (ug), "
        f"'folate' (ug), "
        f"'vitamin_c' (mg), "
        f"'calcium' (mg), "
        f"'iodine' (ug), "
        f"'iron' (mg), "
        f"'magnesium' (mg), "
        f"'potassium' (mg), "
        f"'sodium' (mg), "
        f"'zinc' (mg). "
        f"If a value is negligible, put '0'. Do not use Markdown."
    )

    try:
        response = model.generate_content(prompt)
        cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned_text)
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

