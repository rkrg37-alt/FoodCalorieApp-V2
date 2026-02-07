from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import json

app = Flask(__name__)

# --- SETUP THE CHEF ---
# Get the key from the server's safe (Environment Variable)
api_key = os.environ.get("GEMINI_API_KEY", "PASTE_YOUR_KEY_HERE_FOR_LOCAL_TESTING")
genai.configure(api_key=api_key)

# We use the Flash model for speed
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "Hello! The Nutritionist AI is Online."

@app.route('/ask', methods=['GET'])
def ask_calories():
    # 1. Get the food name from the URL
    food_item = request.args.get('food')
    
    if not food_item:
        return jsonify({"error": "No food specified"})

    # 2. The New Prompt (Asking for JSON)
    # We tell Gemini to act like a database and return structured data
    prompt = (
        f"Analyze this food intake: '{food_item}'. "
        f"Return a strictly valid JSON object with these exact keys: "
        f"'calories' (integer number only), "
        f"'protein' (string, e.g., '20g'), "
        f"'fiber' (string, e.g., '5g'), "
        f"'micronutrients' (string, list key vitamins/minerals). "
        f"Do not use Markdown formatting or code blocks. Just the raw JSON."
    )

    try:
        # 3. Ask Gemini
        response = model.generate_content(prompt)
        
        # 4. Clean up the answer (sometimes AI adds ```json at the start)
        cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
        
        # 5. Convert text to real JSON and send it back
        data = json.loads(cleaned_text)
        return jsonify(data)

    except Exception as e:
        # If something breaks, send a safe error message
        return jsonify({
            "calories": 0, 
            "protein": "0g", 
            "fiber": "0g", 
            "micronutrients": "Error: Could not analyze.",
            "details": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)