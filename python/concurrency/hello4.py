import asyncio

async def tache():
    print("Étape 1 : début")
    await asyncio.sleep(1)  # Première attente
    print("Étape 2 : après 1 seconde")
    await asyncio.sleep(2)  # Deuxième attente
    print("Étape 3 : après 2 secondes supplémentaires")

# Exécuter la coroutine
asyncio.run(tache())
