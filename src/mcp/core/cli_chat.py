from typing import List, Tuple
from mcp.types import Prompt, PromptMessage
from anthropic.types import MessageParam

from core.chat import Chat
from core.claude import Claude
from mcp_client import MCPClient

class CliChat(Chat):
    def __init__(
            self,
            doc_client: MCPClient,
            clients: dict[str, MCPClient],
            claude_service: Claude,
    ):
        super().__init__(clients=clients, claude_service= claude_service)

        self.doc_client: MCPClient = doc_client

    async def list_prompts(self) -> list[Prompt]:
        return await self.doc_client.list_prompts()
    
    async def list_docs_ids(self) -> list[str]:
        return await self.doc_client.read_resource("docs://documents")
    
    async def get_doc_content(self, doc_id: str)-> str:
        return await self.doc_client.read_resource(f"docs://documents/{doc_id}")
    

    async def get_prompt(
            self, command: str, doc_id: str
    )-> list[PromptMessage]:
        return await self.doc_client.get_prompt(command, {"doc_id": doc_id})
    
    async def _extract_resources(self, query: str) -> str:
        mentions= [word[1:] for word in query.split() if word.startswith("@")]

        doc_ids= await self.list_docs_ids()
        mentioned_docs: list[Tuple[str, str]] = []

        for doc_id in doc_ids:
            if doc_id in mentions:
                content = await self.get_doc_content(doc_id)
                mentioned_docs.append((doc_id, content))

        return "".join(
            f'\n<document id="{doc_id}">\n{content}\n</document>\n'
            for doc_id, content in mentioned_docs
        )
    
    async def _process_command(self, query: str)-> bool:
        if not query.startswith("/"):
            return False
        
        words= query.split()
        command= words[0].replace("/","")

        messages= await self.doc_client.get_prompt(
            command, {"doc_id": words[1]}
        )

        