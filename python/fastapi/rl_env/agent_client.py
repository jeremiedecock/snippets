from __future__ import annotations

import random
import requests

BASE_URL = "http://<IP_OU_DNS_DU_SERVEUR>:8000"
TOKEN = "<TON_TOKEN_ICI>"


def main() -> None:
    headers = {"Authorization": f"Bearer {TOKEN}"}

    # reset
    r = requests.post(f"{BASE_URL}/reset", json={"seed": 0}, headers=headers, timeout=10)
    r.raise_for_status()
    obs = r.json()["observation"]

    episode_over = False
    total_reward = 0.0

    while not episode_over:
        action = random.randint(0, 3)  # FrozenLake
        r = requests.post(f"{BASE_URL}/step", json={"action": action}, headers=headers, timeout=10)
        r.raise_for_status()
        tr = r.json()

        obs = tr["observation"]
        total_reward += float(tr["reward"])
        episode_over = bool(tr["terminated"]) or bool(tr["truncated"])

    print("done:", {"total_reward": total_reward, "last_obs": obs})


if __name__ == "__main__":
    main()
