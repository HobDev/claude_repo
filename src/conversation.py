from request import Request, add_user_message, add_assistant_message
import tools_and_schemas
import json

def start_conversation():
    # Start with an empty message list
    messages=[]
    system="""
    You are a helpful assistant
    """
    # lower temperature increase determinism (predictable) and higher temperature increase randomness (creative)
    temperature=1.0
    tools= [tools_and_schemas.get_current_datetime_schema]
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
        answer= request.chat(messages, system=system, temperature=temperature, tools= tools)

        # Add assistant message to the conversation history
        add_assistant_message(messages, answer)

        if answer.stop_reason == "tool_use":

            tool_results = run_tools(answer)
            add_user_message(messages, tool_results)


def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return tools_and_schemas.get_current_datetime(**tool_input)



def run_tools(message):
    tool_requests =[
        block for block in message.content if block.type == "tool_use"
    ]
    tool_result_blocks =[]

    for tool_request in tool_requests:
        try:
            tool_output=run_tool(tool_request.name,tool_request.input)
            tool_result_block={
                "type":"tool_result",
                "tool_use_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False
            }
        except Exception as e:
            tool_result_block={
                "type":"tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True
            }

            tool_result_blocks.append(tool_result_block)
    return tool_result_blocks
    
if __name__=="__main__":
    start_conversation()