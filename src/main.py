from src import ClaudeAgent

from src import InventoryController, ShipmentController


def main():
    """
    Run THE PharmaOps AI command line interface
    """


    try:
        agent = ClaudeAgent(controllers=[InventoryController(), ShipmentController()])

    except ValueError as error:
        print(f"Configuration error: {error}")
        return

    print("PharmaOps AI")
    print("Type 'exit' or 'quit' to stop. ")


    while True:
        question = input("\nYou: ").strip()

        if not question:
            continue

        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break


        try:
            response = agent.ask(question)

            print(f"\nPharmaOps AI :")
            print(response)

        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()