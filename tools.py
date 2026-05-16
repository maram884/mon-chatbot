def is_medical_question(text):

    keywords = [
        "maladie",
        "diabète",
        "fièvre",
        "douleur",
        "symptôme",
        "infection",
        "cancer",
        "traitement",
        "hypertension",
        "virus",
        "médical"
    ]

    return any(word in text.lower() for word in keywords)

def safety_warning():

    return (
        "\n⚠️ Ceci est un assistant éducatif "
        "et ne remplace pas un médecin."
    )

def format_context(context):

    formatted = ""

    used_sources = set()

    for doc, source in context:

        formatted += f"\n📌 Source : {source}\n"
        formatted += f"{doc[:300]}...\n"

        used_sources.add(source)

    return formatted