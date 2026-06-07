from api_request import Request, add_user_message, add_assistant_message
import tool_use.tools_and_schemas as tools_and_schemas
import json
import tool_use.built_in_tool_schemas as built_in_tool_schemas
import tool_use.text_editor_tool_functions as text_editor_tool_functions

text_tool= text_editor_tool_functions.TextEditorTool()

def start_conversation():
    # Start with an empty message list
    messages=[]
    system=[
        {
        "type": "text",
        "text":  "You are a helpful assistant"
        }
    ]
   
    # lower temperature increase determinism (predictable) and higher temperature increase randomness (creative)
    temperature=1.0
    tools= [
        tools_and_schemas.get_current_datetime_schema,
        tools_and_schemas.add_duration_to_datetime_schema,
        tools_and_schemas.set_reminder_schema,
        built_in_tool_schemas.text_edit_schema,
        built_in_tool_schemas.web_search_schema
        ]
    
    thinking= False

    request = Request()

    # use a 'while True' loop to run the chatbot forever
    while True:
        # Get user input
        user_input= input("\n>")

        # Skip empty input
        if not user_input.strip():
            continue

        if user_input=="quit":
            break

    # Add user input to the list of questions
        add_user_message(messages, user_input)

        # Keep going until the model has no more tool calls for this user turn.
        while True:
            # Pass the list of messages into 'chat' to get a response.
            answer= request.chat(messages, system=system, temperature=temperature, tools= tools, thinking)

            if answer is None:
                print("\nError: model did not return a response.")
                break

            # Add assistant message to the conversation history.
            add_assistant_message(messages, answer)

            if answer.stop_reason != "tool_use":
                break

            tool_results = run_tools(answer)
            add_user_message(messages, tool_results)


def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return tools_and_schemas.get_current_datetime(**tool_input)
    elif tool_name== "add_duration_to_datetime":
        return tools_and_schemas.add_duration_to_datetime(**tool_input)
    elif tool_name== "set_reminder":
        return tools_and_schemas.set_reminder(**tool_input)
    elif tool_name == "str_replace_based_edit_tool":
        command = tool_input["command"]
        if command == "view":
            return text_tool.view(
                tool_input["path"], tool_input.get("view_range")
            )
        elif command == "str_replace":
            return text_tool.str_replace(
                tool_input["path"], tool_input["old_str"], tool_input["new_str"]
            )
        elif command == "create":
            return text_editor_tool_functions.create(tool_input["path"], tool_input["file_text"])
        elif command == "insert":
            return text_tool.insert(
                tool_input["path"],
                tool_input["insert_line"],
                tool_input["new_str"],
            )
        elif command == "undo_edit":
            return text_tool.undo_edit(tool_input["path"])
        else:
            raise Exception(f"Unknown text editor command: {command}")
    else:
        raise Exception(f"Unknown tool name: {tool_name}")
    


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