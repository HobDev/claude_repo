from request import Request, add_user_message, add_assistant_message

def start_conversation():
    # Start with an empty message list
    messages=[]
    system="""
    You are a helpful assistant
    """
    # lower temperature increase determinism (predictable) and higher temperature increase randomness (creative)
    temperature=1.0
    request = Request()

    # use a 'while True' loop to run the chatbot forever
    while True:
        # Get user input
        user_input= input("> ")
        print(">", user_input)

        # Skip empty input
        if not user_input.strip():
            continue

        if user_input=="quit":
            break

    # Add user input to the list of questions
        add_user_message(messages, user_input)

        # Pass the list of messages into 'chat' to get a response
        answer= request.chat(messages, system=system, temperature=temperature)

        # Add assistant message to the conversation history
        add_assistant_message(messages, answer)


    
if __name__=="__main__":
    start_conversation()