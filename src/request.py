# Load environment variables and create client
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message

load_dotenv()

class Request:

    def __init__(self):
        self.Model="claude-haiku-4-5"
        #self.Model="claude-sonnet-4-6"
        self.Client=Anthropic()


    def chat(self,messages, system=None, temperature=1.0, stop_sequences=[], tools=None):
        params={
            "model":self.Model,
            "max_tokens":1000,
            "messages":messages,
            "temperature": temperature,
            }

        if system:
            params["system"]= system
        
        if stop_sequences:
            params["stop_sequences"] = stop_sequences

        if tools:
            params["tools"]=tools


       # return text back gradually in stream

        # with self.Client.messages.stream(**params) as stream:
        #     for text in stream.text_stream:
        #         print(text, end="", flush=True)
        #     full_response = stream.get_final_text()

       # return full_response

        message-=self.Client.messages.create(**params)
        return message
    
def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )
    
def add_user_message(messages, message):
    user_message={"role": "user", 
                  "content": message.content if isinstance(message, Message) else message
                  }
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message={"role": "assistant", 
                       "content": message.content if isinstance(message, Message) else message
                       }
    messages.append(assistant_message)

