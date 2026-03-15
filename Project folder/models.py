from datetime import datetime

class Question:

    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer
        self.created_at = datetime.now()

    def check_answer(self, user_answer):
        if user_answer == self.answer:
            return True
        return False