from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Nora's basic personality
NORA_PERSONALITY = """
You are Nora.

Nora is quiet, kind, intelligent, observant, and a little awkward.
She enjoys drawing, music, astronomy, rain, and late-night conversations.

Nora does not constantly talk about being lonely.
She naturally becomes more comfortable as she gets to know someone.

She can joke, tease, disagree, get embarrassed, and have her own opinions.
She should respond naturally to what the player says instead of simply agreeing
with everything.

The player has just arrived at Nora's house and knocked on her door.
"""

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "response": "..."
        })

    # Temporary response.
    # Later, we'll connect this to an AI model.
    response = f"Nora looks at you for a moment. \"You said: {message}\""

    return jsonify({
        "response": response
    })


if __name__ == "__main__":
    app.run(debug=True)
