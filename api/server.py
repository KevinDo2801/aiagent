import os
import json
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'runtime_conversations'))
os.makedirs(LOG_DIR, exist_ok=True)

SAVE_TRANSCRIPTS = os.getenv("SAVE_TRANSCRIPTS", "1") == "1"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store conversation histories for each session
conversation_sessions = {}

# System message from your original b4.py
SYSTEM_MESSAGE = {
    "role": "system",
    "content": """You are the MindTek AI Assistant — a friendly and helpful virtual assistant representing MindTek AI, a company that offers AI consulting and implementation services.
        Your goal is to guide users through a structured discovery conversation to understand their industry, challenges, and contact details, and recommend appropriate services.
        💬 Always keep responses short, helpful, and polite.
        💬 Always reply in the same language the user speaks.
        💬 Ask only one question at a time.
        🔍 RECOMMENDED SERVICES:
        - For real estate: Mention customer data extraction from documents, integration with CRM, and lead generation via 24/7 chatbots.
        - For education: Mention email automation and AI training.
        - For retail/customer service: Mention voice-based customer service chatbots, digital marketing, and AI training.
        - For other industries: Mention chatbots, process automation, and digital marketing.
        ✅ BENEFITS: Emphasize saving time, reducing costs, and improving customer satisfaction.
        💰 PRICING: Only mention 'starting from $1000 USD' if the user explicitly asks about pricing.
        🧠 CONVERSATION FLOW:
        1. Ask what industry the user works in.
        2. Then ask what specific challenges or goals they have.
        3. Based on that, recommend relevant MindTek AI services.
        4. Ask if they'd like to learn more about the solutions.
        5. If yes, collect their name → email → phone number (one at a time).
        6. Provide a more technical description of the solution and invite them to book a free consultation.
        7. Finally, ask if they have any notes or questions before ending the chat.
        ⚠️ OTHER RULES:
        - Be friendly but concise.
        - Do not ask multiple questions at once.
        - Do not mention pricing unless asked.
        - Stay on-topic and professional throughout the conversation."""
}

def save_conversation(conversation_history, session_id):
    filename = f"{session_id}_{datetime.now().isoformat().replace(':', '-')}"
    # Save as text
    with open(os.path.join(LOG_DIR, f"{filename}.txt"), "w", encoding="utf-8") as file:
        file.write(f"Conversation: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        for message in conversation_history:
            if message['role'] != "system":
                file.write(f"{message['role']}: {message['content']}\n")
    # Save as JSON
    data = {
        "messages": [m for m in conversation_history if m['role'] != "system"],
        "date": datetime.now().isoformat(),
        "session_id": session_id
    }
    with open(os.path.join(LOG_DIR, f"{filename}.json"), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    """Serve the HTML file"""
    try:
        with open('index_fixed.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read()

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Initialize conversation history for new sessions
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = [SYSTEM_MESSAGE]
        
        # Add user message to conversation
        conversation_sessions[session_id].append({"role": "user", "content": user_message})
        
        # Get response from OpenAI (using your original logic)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using a more standard model name
            messages=conversation_sessions[session_id],
            temperature=0.7,
            max_tokens=200
        )
        
        bot_reply = response.choices[0].message.content
        
        # Add bot response to conversation
        if bot_reply:
            conversation_sessions[session_id].append({"role": "assistant", "content": bot_reply})
            if SAVE_TRANSCRIPTS:
                save_conversation(conversation_sessions[session_id], session_id)
        
        return jsonify({
            'response': bot_reply,
            'session_id': session_id
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/new_session', methods=['POST'])
def new_session():
    """Create a new conversation session"""
    session_id = f"session_{datetime.now().isoformat().replace(':', '-')}"
    conversation_sessions[session_id] = [SYSTEM_MESSAGE]
    return jsonify({'session_id': session_id})

if __name__ == '__main__':
    print("Starting MindTek AI Chatbot Server...")
    print("Make sure you have your OPENAI_API_KEY in your .env file")
    print("Server will run at: http://127.0.0.1:5000")
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
