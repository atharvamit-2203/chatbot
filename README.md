import google.generativeai as genai
import json

def configure_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def generate_mcq(model, text, num_questions=3):
    prompt = (f"Create {num_questions} multiple choice questions based on this text: {text} "
              "Make questions that test understanding of key concepts. "
              "Each question should have 4 options (A, B, C, D). "
              "Format each question as JSON with this structure: "
              "{ 'question': '...', 'options': {'A': '...', 'B': '...', 'C': '...', 'D': '...'}, "
              "'correct_answer': 'A/B/C/D', 'explanation': '...'} "
              "Return the questions as a JSON array.")
    try:
        response = model.generate_content(prompt)
        response_text = response.text
        json_str = response_text.split("```json")[-1].split("```")[0].strip()
        return json.loads(json_str)
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []

def take_quiz(questions):
    score = 0
    total = len(questions)
    print("\n=== Welcome to the quiz.Hope u have a great time ===\n")
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for option, text in q['options'].items():
            print(f"{option}) {text}")
        while True:
            answer = input("\nYour answer (A/B/C/D): ").upper()
            if answer in ['A', 'B', 'C', 'D','a','b','c','d']:
                break
            print("Please enter A, B, C, or D")
        if answer == q['correct_answer']:
            print("\nCorrect!")
            score += 1
        else:
            print("\nIncorrect!")
        print(f"Explanation: {q['explanation']}\n" + "-"*50)
    print(f"\nQuiz completed. Your score is: {score}/{total} ({(score/total*100):.1f}%)")
def main():
    api_key = "AIzaSyCuYT5rfJdcAcck3FGTHzzMAMkMC-nASWA"
    model = configure_model(api_key)
    while True:
        print("\n=== Quiz generator ===")
        print("1. Enter your input")
        print("2. Take a sample text")
        print("3. Exit")
        choice = input("\nEnter your choice (1-3): ")
        if choice == "1":
            text = input("\nEnter the topic from which you want to generate the questions:\n")
            num_questions = int(input("How many questions do you want to generate ?? "))
        elif choice == "2":
            text = ("Newton's first law of motion states that an object at rest stays at rest "
                    "and an object in motion stays in motion unless acted upon by an external force. "
                    "This principle is also known as the law of inertia. The second law of motion "
                    "states that force equals mass times acceleration.")
            num_questions = 3
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
            continue
        print("\nGenerating questions...")
        questions = generate_mcq(model, text, num_questions)
        if questions:
            take_quiz(questions)
        again = input("\nWould you like to try another quiz ?? (y/n): ").lower()
        if again != 'y':
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
