#!/usr/bin/env python3

# Src : https://github.com/langchain-ai/learning-langchain/tree/master/ch2/py

# C.f.
# - https://github.com/langchain-ai/langchain/tree/master/libs/text-splitters#readme
# - https://reference.langchain.com/python/langchain-text-splitters
# - https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter
# - https://reference.langchain.com/python/langchain-text-splitters/base/TextSplitter


from langchain_text_splitters import RecursiveCharacterTextSplitter

texts = [
    "Hello, this is a sample text that will be split into smaller chunks using the RecursiveCharacterTextSplitter.\nThe splitter will use the specified separators to determine where to split the text.\nThis allows for more control over how the text is divided, ensuring that it is split in a way that makes sense for the content.",
    "Bonjour, voici un texte d'exemple qui sera divisé en fragments plus petits à l'aide de la fonction `RecursiveCharacterTextSplitter`.\nLe diviseur utilisera les séparateurs spécifiés pour déterminer où diviser le texte.\nCela permet un meilleur contrôle sur la manière dont le texte est divisé, en garantissant qu'il soit divisé de manière cohérente par rapport au contenu ",
    "Hola, este es un texto de ejemplo que se dividirá en fragmentos más pequeños utilizando el RecursiveCharacterTextSplitter.\nEl divisor utilizará los separadores especificados para determinar dónde dividir el texto.\nEsto permite un mayor control sobre cómo se divide el texto, asegurando que se divida de una manera que tenga sentido para el contenido.",
]

metadatas = [
    {"language": "English", "length": len(texts[0])},
    {"language": "French", "length": len(texts[1])},
    {"language": "Spanish", "length": len(texts[2])},
]

splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=100,
    chunk_overlap=20,
)
splitted_docs = splitter.create_documents(texts, metadatas=metadatas)

for doc in splitted_docs:
    print(f"\n{doc}\n")