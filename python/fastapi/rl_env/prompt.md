### Prompt – Hackathon RL “Environment as a Service” en HTTP(S)

Je souhaite concevoir un service d’évaluation pour un hackathon d’apprentissage par renforcement.

Objectif : exposer un environnement Gymnasium via une API HTTP(S) afin que des agents distants (soumissions des participants) puissent interagir uniquement par requêtes réseau pour faire **de l’inférence uniquement** (pas d’entraînement).

#### Contraintes générales

* Chaque participant possède un **token d’authentification pré-défini**.
* Le serveur doit maintenir **un seul objet environnement par token**.
* Le protocole de communication est exclusivement **HTTP(S) + JSON**.
* Le serveur doit être **robuste aux requêtes simultanées** :

  * sérialisation des accès `step/reset` pour un même token,
  * parallélisme entre tokens différents,
  * pas de corruption d’état.
* Les appels bloquants (`env.step`, `env.reset`) ne doivent pas bloquer l’event loop.
* Il doit y avoir :

  * limite de nombre de pas par épisode,
  * TTL d’inactivité avec nettoyage automatique des environnements,
  * endpoint `/health`.

#### API attendue

* Authentification par header :

  ```
  Authorization: Bearer <token>
  ```

* `POST /reset`

  * body : `{ "seed": int | null, "options": dict | null }`
  * réponse : `{ "observation": ..., "info": {...} }`

* `POST /step`

  * body : `{ "action": int }`
  * réponse :

    ```
    {
      "observation": ...,
      "reward": float,
      "terminated": bool,
      "truncated": bool,
      "info": {...},
      "step_count": int
    }
    ```

* `GET /health`

  * réponse : `{ "status": "ok", "active_users": int, "env_id": str }`

#### Technologies imposées

* Python
* FastAPI
* Gymnasium
* Gestion de concurrence avec `anyio` (locks + `to_thread.run_sync`)

#### Environnement par défaut

* `FrozenLake-v1`

---

À partir de ce prompt, aide-moi à :

1. affiner l’architecture,
2. améliorer la sécurité,
3. ajouter des outils d’audit / replay,
4. préparer un déploiement propre pour un hackathon réel.
