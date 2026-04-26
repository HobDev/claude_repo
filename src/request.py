# Load environment variables and create client
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

class Request:

    def __init__(self):
        self.Model="claude-haiku-4-5"
        #self.Model="claude-sonnet-4-6"
        self.Client=Anthropic()


    def chat(self,messages, system=None, temperature=1.0, stop_sequences=[]):
        params={
            "model":self.Model,
            "max_tokens":1000,
            "messages":messages,
            "temperature": temperature
            }

        if system:
            params["system"]= system
        
        if stop_sequences:
            params["stop_sequences"] = stop_sequences

        with self.Client.messages.stream(**params) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
            full_response = stream.get_final_text()

        return full_response
    

    
def add_user_message(messages, text):
    user_message={"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message={"role": "assistant", "content": text}
    messages.append(assistant_message)

