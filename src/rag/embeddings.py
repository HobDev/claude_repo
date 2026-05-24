from dotenv import load_dotenv
import voyageai

load_dotenv()

client = voyageai.Client()


def generate_embedding(text, model="voyage-3-large", input_type="query"):
    result= client.embed([text], model=model, input_type=input_type)

    print(result.embeddings[0])





if __name__=="__main__":
    with open("./report.md", "r") as f:
        text=f.read()

    generate_embedding(text)
