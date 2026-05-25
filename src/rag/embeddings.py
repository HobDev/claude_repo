from dotenv import load_dotenv
import voyageai
from typing import Any, Union

load_dotenv()

client: Any = getattr(voyageai, "Client")()


def generate_embedding(
    chunks: Union[str, list[str]],
    model: str = "voyage-4-large",
    input_type: str = "query",
) -> Union[list[float], list[list[float]]]:
    if isinstance(chunks, list):
        result = client.embed(chunks, model=model, input_type=input_type)
        return [[float(value) for value in vector] for vector in result.embeddings]

    result = client.embed([chunks], model=model, input_type=input_type)
    return [float(value) for value in result.embeddings[0]]





if __name__=="__main__":
    with open("./report.md", "r") as f:
        text=f.read()

    generate_embedding(text)
