import os
import openai
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)

conversation_history = [
    {
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
    },
]

def save_conversation(conversation_history, filename):
    # save as text in folder "conversations"
    with open(f"conversations/{filename}.txt", "w", encoding="utf-8") as file:
        file.write(f"Conversation: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        for message in conversation_history:
            if message['role'] != "system":
                file.write(f"{message['role']}: {message['content']}\n")
    
    # save as json in folder "conversations" 
    # do not save the system message
    data = {"messages": [message for message in conversation_history if message['role'] != "system"], "date": datetime.now().isoformat()}
    with open(f"conversations/{filename}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# create folder "conversations" if it doesn't exist
if not os.path.exists("conversations"):
    os.makedirs("conversations")

# create filename with current date and time
filename = datetime.now().isoformat().replace(":", "-")

while True:
    user_input = input("You: ").strip().lower()

    if user_input == "exit":
        save_conversation(conversation_history, filename)
        break
    elif not user_input:
        continue

    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=conversation_history,
        temperature=0.7,
        max_tokens=200
    )

    reply = response.choices[0].message.content
    print(f"Assistant: {reply}")

    if reply:
        conversation_history.append({"role": "assistant", "content": reply})
        save_conversation(conversation_history, filename)