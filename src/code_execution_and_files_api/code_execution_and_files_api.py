
# Load env variables and create client
from dotenv import load_dotenv
from anthropic import Anthropic
from pathlib import Path
from api_request import Request, add_user_message

load_dotenv()

request= Request()

client = Anthropic(
     # optional headers with api
            default_headers={
        # beta features which are not generally available
        "anthropic-beta": "code-execution-2026-01-20, files-api-2025-04-14"
            }
)
model = "claude-sonnet-4-5-20250929"


def upload(file_path):
    path = Path(file_path)
    extension = path.suffix.lower()

    mime_type_map = {
        ".pdf": "application/pdf",
        ".txt": "text/plain",
        ".md": "text/plain",
        ".py": "text/plain",
        ".js": "text/plain",
        ".html": "text/plain",
        ".css": "text/plain",
        ".csv": "text/csv",
        ".json": "application/json",
        ".xml": "application/xml",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.ms-excel",
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }

    mime_type = mime_type_map.get(extension)

    if not mime_type:
        raise ValueError(f"Unknown mimetype for extension: {extension}")
    filename = path.name

    with open(file_path, "rb") as file:
        return client.beta.files.upload(file=(filename, file, mime_type))


def list_files():
    return client.beta.files.list()


def delete_file(id):
    return client.beta.files.delete(id)


def download_file(id, filename=None):
    file_content = client.beta.files.download(id)

    if not filename:
        file_metadata = get_metadata(id)
        file_content.write_to_file(file_metadata.filename)
    else:
        file_content.write_to_file(filename)


def get_metadata(id):
    return client.beta.files.retrieve_metadata(id)









if __name__=="__main__":
    file_metadata = upload("streaming.csv")
    print(file_metadata)
    messages = []

    add_user_message(
        messages,
        [
            {
                "type": "text",
                "text": """
    Run a detailed analysis to determine major drivers of churn.
    Your final output should include at least one detailed plot summarizing your findings.

    Critical note: Every time you execute code, you're starting with a completely clean slate. 
    No variables or library imports from previous executions exist. You need to redeclare/reimport all variables/libraries.
                """,
            },
            {"type": "container_upload", "file_id": file_metadata.id},
        ],
    )

    request.chat(messages, tools=[{"type": "code_execution_20260120", "name": "code_execution"}])