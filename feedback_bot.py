# feedback_bot.py
from anthropic import Anthropic
from config import CLAUDE_API_KEY
import os

class SellerFeedbackBot:
    def __init__(self):
        self.client = Anthropic(api_key=CLAUDE_API_KEY)
        self.model = "claude-3-haiku-20240307"
        self.max_tokens = 300
        self.context = {}

    def ask_for_info(self, field):
        questions = {
            "seller_name": "Could you please tell me the seller's name?",
            "project": "What was the project or service they did for you?",
            "delivery": "How did they deliver the project? (e.g., quickly, clearly, exceeded expectations)",
            "extra": "Any other thing you'd like to mention? (optional)"
        }
        return questions.get(field, "Please provide more info:")

    def collect_answer(self, field, answer):
        self.context[field] = answer.strip()

    def generate_feedback(self):
        prompt = f"""
You are a helpful assistant helping a buyer craft a short, polite, and professional feedback message for a seller.

Here’s what the buyer shared:
- Seller Name: {self.context.get('seller_name', '')}
- Project: {self.context.get('project', '')}
- Delivery: {self.context.get('delivery', '')}
- Extra Notes: {self.context.get('extra', '')}

Your task:
Write a short and friendly feedback message that thanks the seller, highlights their good work, and feels genuine and unique.

Keep it under 150 words. Make sure it sounds natural and not robotic.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0.7,
                system="You are a helpful assistant helping users write short, unique, and polite feedback messages.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"[Error] Couldn't generate feedback: {str(e)}"