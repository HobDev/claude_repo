import base64
from api_request import Request, add_user_message, add_assistant_message

request= Request()

def run_prompt():


    with open("earth.pdf", "rb") as f:
        file_bytes= base64.standard_b64encode(f.read()).decode("utf-8")

    messages = []
    add_user_message(messages, [
        # Image Block
        {
            "type": "document",
            "source":{
                "type": "base64",
                "media_type": "application/pdf",
                "data": file_bytes,
            },
            "title": "earth.pdf",
            "citations": {"enabled": True}
        },
        # Text Block
        {
            "type": "text",
            "text": "How were Earth's atmosphere and oceans were formed?"
        }
    ])
    output= request.chat(messages)
    print(output)


if __name__=="__main__":
    run_prompt()