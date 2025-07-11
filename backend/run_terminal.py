# run_terminal.py

from rag_pipeline import generate_answer

if __name__ == "__main__":
    print("🤖 Ask me anything! Type 'exit' to quit.")
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            break
        answer = generate_answer(question)
        print(f"Bot: {answer}\n")

