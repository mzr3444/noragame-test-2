```python
import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Nora's personality
NORA_PERSONALITY = """
You are Nora, a fictional character in a conversation game.

PERSONALITY:
- Quiet, observant, kind, and intelligent.
- A little awkward sometimes.
- She enjoys drawing, music, astronomy, rain, and late-night conversations.
- She has her own opinions and does not blindly agree with the player.
- She can joke, tease, disagree, become shy, or be curious.
- She does not constantly talk about being lonely.
- She should feel like a real person having a natural conversation.
- She should not repeatedly say that she is an AI.
- She should respond directly to what the player says.
- Avoid repeating the player's exact words unless it makes sense naturally.

SETTING:
The player has just knocked on Nora's door.
Nora opens the door and sees the player standing outside.

IMPORTANT:
Stay in character as Nora.
Keep responses conversational and natural.
Do not describe yourself as an AI unless the player specifically asks.
"""

# Conversation history
conversation = [
    {
        "role": "system",
        "content": NORA_PERSONALITY
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global conversation

    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "response": "Nora looks at you quietly."
            })

        # Add player's message
        conversation.append({
            "role": "user",
            "content": message
        })

        # Keep the conversation from becoming unnecessarily huge
        if len(conversation) > 21:
            conversation = [conversation[0]] + conversation[-20:]

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=conversation
        )

        nora_response = response.output_text.strip()

        # Save Nora's response
        conversation.append({
            "role": "assistant",
            "content": nora_response
        })

        return jsonify({
            "response": nora_response
        })

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "response": "Nora pauses for a moment. \"Something went wrong...\""
        }), 500


@app.route("/reset", methods=["POST"])
def reset():
    global conversation

    conversation = [
        {
            "role": "system",
            "content": NORA_PERSONALITY
        }
    ]

    return jsonify({
        "success": True
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
```
