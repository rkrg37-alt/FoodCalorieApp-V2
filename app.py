import os
from flask import Flask, request
import google.generativeai as genai

app = Flask(__name__)

# --- SETUP THE CHEF ---
# We get the key from the "Safe" (Environment Variable)
# If we are testing on laptop, we use the fallback key
api_key = os.environ.get("GEMINI_API_KEY", "PASTE_YOUR_KEY_HERE_FOR_LOCAL_TESTING")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

@app.route('/')
def home():
    return "Hello! The Food Server is Online."

@app.route('/ask')
def ask_chef():
    food = request.args.get('food')
    if not food:
        return "Error: You didn't tell me what food to check!"
    
    # Prompt
    prompt = f"Analyze this food: {food}. Return only the total Calories as a number. Do not say 'kcal', just the number."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    # This part only runs on your laptop
    app.run(debug=True, host='0.0.0.0')