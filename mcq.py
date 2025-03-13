import google.generativeai as genai
import json

class InteractiveMCQGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_mcq(self, text: str, num_questions: int = 3):
        prompt = f"""
        Create {num_questions} multiple choice questions based on this text: {text}

        Make questions that test understanding of key concepts.
        Each question should have 4 options (A, B, C, D).

        Format each question as JSON with this structure:
        {{
            "question": "The question text",
            "options": {{
                "A": "First option",
                "B": "Second option",
                "C": "Third option",
                "D": "Fourth option"
            }},
            "correct_answer": "The correct letter (A, B, C, or D)",
            "explanation": "Brief explanation of why this is correct"
        }}

        Return the questions as a JSON array.
        """

        try:
            response = self.model.generate_content(prompt)

            response_text = response.text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()

            questions = json.loads(json_str)
            return questions

        except Exception as e:
            print(f"Error generating questions: {str(e)}")
            return []

def take_quiz(questions):
    """Interactive function to take the quiz."""
    score = 0
    total = len(questions)

    print("\n=== Let's start the quiz! ===\n")

    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}:")
        print(q['question'])
        for option, text in q['options'].items():
            print(f"{option}) {text}")

        while True:
            answer = input("\nYour answer (A/B/C/D): ").upper()
            if answer in ['A', 'B', 'C', 'D']:
                break
            print("Please enter A, B, C, or D")

        if answer == q['correct_answer']:
            print("\n Correct!")
            score += 1
        else:
            print("\n Incorrect!")

        print(f"Explanation: {q['explanation']}")
        print("\n" + "-"*50)

    print(f"\nQuiz completed. Your score is: {score}/{total} ({(score/total*100):.1f}%)")
    return score

def main():
    api_key = "Your API-KEY"
    generator = InteractiveMCQGenerator(api_key)

    while True:
        print("\n=== MCQ Generator and Quiz ===")
        print("1. Enter your own text")
        print("2. Use sample text")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            text = input("\nEnter the text you want to generate questions from:\n")
            num_questions = int(input("How many questions do you want to generate? "))
        elif choice == "2":
            text = """
            Newton's first law of motion states that an object at rest stays at rest and an object
            in motion stays in motion unless acted upon by an external force. This principle is also
            known as the law of inertia. The second law of motion states that force equals mass
            times acceleration.
            """
            num_questions = 3
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
            continue

        print("\nGenerating questions...")
        questions = generator.generate_mcq(text, num_questions)

        if questions:
            take_quiz(questions)

        again = input("\nWould you like to try another quiz? (y/n): ").lower()
        if again != 'y':
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
