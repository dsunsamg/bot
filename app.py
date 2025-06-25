# app.py
from flask import Flask, request, jsonify, render_template
from feedback_bot import SellerFeedbackBot
import os

app = Flask(__name__)
chatbot = SellerFeedbackBot()

STEPS = ["seller_name", "project", "delivery", "extra", "generate"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    current_step = request.json.get("step", 0)

    if current_step < len(STEPS) - 1:
        field = STEPS[current_step]
        chatbot.collect_answer(field, user_message)
        next_question = chatbot.ask_for_info(STEPS[current_step + 1])
        return jsonify({
            "response": next_question,
            "step": current_step + 1
        })
    else:
        feedback = chatbot.generate_feedback()
        return jsonify({
            "response": "Here's your feedback:\n\n" + feedback,
            "step": "done"
        })

# This is the important part 👇
if __name__ == "__main__":
    # Use the PORT env var or default to 5000 (for local dev)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
