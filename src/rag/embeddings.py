from dotenv import load_dotenv
import voyageai

load_dotenv()

client = voyageai.Client()


def generate_embedding(chunks, model="voyage-3-large", input_type="query"):
    input= chunks if is_list else [chunks]
    result= client.embed(input, model=model, input_type=input_type)
    embeddings= result.embeddings if is_list else result.embeddings[0]
    print(embeddings)





if __name__=="__main__":
    with open("./report.md", "r") as f:
        text=f.read()

    generate_embedding(text)
