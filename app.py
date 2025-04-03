from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gemin_model import AITutor
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize AI tutor
tutor = AITutor()

@app.route('/')
def serve_chat():
    return send_from_directory(app.static_folder, 'chat.html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message or not user_message.strip():
            return jsonify({"error": "Message cannot be empty"}), 400

        # Get response from Gemini
        response = tutor.ask_gemini(user_message)
        return jsonify({"reply": response})

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "AI service unavailable. Please try again later."}), 500

if __name__ == "__main__":
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(host="0.0.0.0", port=5000, debug=True)