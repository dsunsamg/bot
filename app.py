# app.py
from flask import Flask, request, jsonify, render_template
from feedback_bot import SellerFeedbackBot

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

if __name__ == "__main__":
    app.run(debug=True)