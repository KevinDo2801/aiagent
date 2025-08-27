# MindTek AI Chatbot

A web-based chatbot that connects your HTML frontend with OpenAI's GPT model through a Flask backend.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Environment Variables
Create a `.env` file in the w2 directory with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Server
```bash
python server.py
```

### 4. Open the Chatbot
Open your web browser and go to:
```
http://127.0.0.1:5000
```

## Features

- **MindTek AI Assistant**: Specialized chatbot for AI consulting services
- **Session Management**: Each conversation maintains context
- **Conversation Logging**: All conversations are saved as JSON and TXT files
- **Modern UI**: Responsive chat interface with typing indicators
- **Industry-Specific Responses**: Tailored recommendations based on user's industry

## File Structure

- `server.py` - Flask backend server
- `index.html` - Frontend chatbot interface
- `b4.py` - Original console-based chatbot (for reference)
- `requirements.txt` - Python dependencies
- `conversations/` - Saved conversation logs (created automatically)

## How It Works

1. Frontend (HTML/CSS/JavaScript) sends messages to Flask backend
2. Backend processes messages using OpenAI's GPT model
3. Responses are sent back to frontend and displayed
4. All conversations are automatically saved for future reference
