import json
from pathlib import Path
from psi_project.common import protocol

ROOT = Path(__file__).resolve().parent.parent.parent  # project root
KEYS_DIR = ROOT / "keys"
KEYS_DIR.mkdir(exist_ok=True)

def generate_system_keys():
    N, e, d = protocol.GENRSA(64)
    with open(KEYS_DIR / "server_keys.json", "w") as f:
        json.dump({"N": N, "e": e, "d": d}, f)
    with open(KEYS_DIR / "client_keys.json", "w") as f:
        json.dump({"N": N, "e": e}, f)
    print("Keys generated at", KEYS_DIR)

if __name__ == "__main__":
    generate_system_keys()