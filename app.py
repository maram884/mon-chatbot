from data_loader import documents, sources
from embeddings import get_embeddings
from vector_store import VectorStore
from agent import medilearn_agent

print("⚙️ Initialisation MediLearn...")

embeddings = get_embeddings(documents)

vector_store = VectorStore(embeddings)

vector_store.set_data(documents, sources)

print("\n🏥 MediLearn prêt !")
print("Tape 'exit' pour quitter.\n")

while True:

    question = input("💬 Question : ")

    if question.lower() == "exit":
        print("👋 Au revoir")
        break

    if question.strip() == "":
        continue

    try:

        response = medilearn_agent(
            question,
            vector_store
        )

        print("\n" + response)

    except Exception as e:

        print(f"❌ Erreur : {e}")

    print("\n" + "-" * 50 + "\n")