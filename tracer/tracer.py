import argparse, csv, queue, sys, time
from pathlib import Path
import requests
from tracer.config import CFG
from tracer.sampler import start_remote_sampler
from tracer.logger import TraceLogger

HEADERS = {"Content-Type": "application/json"}
if CFG.SURF_API_KEY:
    HEADERS["Authorization"] = f"Bearer {CFG.SURF_API_KEY}"


def _completion(prompt: str, max_tokens: int | None = None, temp: float = 0.8) -> str:
    p = {"model": CFG.MODEL_NAME, "prompt": prompt, "temperature": temp}
    if max_tokens:
        p["max_tokens"] = max_tokens
    r = requests.post(CFG.SURF_URL, json=p, headers=HEADERS, timeout=300)
    r.raise_for_status()
    return r.json()["choices"][0]["text"]


def _load(fname: str) -> dict[int, list[tuple[int, str]]]:
    fp = Path(CFG.PROMPT_DIR) / fname
    if not fp.exists():
        sys.exit(f"missing {fp}")
    d = {}
    with fp.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = int(row["size"])
            pid = int(row.get("iteration") or row.get("topic") or 0)
            d.setdefault(s, []).append((pid, row["prompt"]))
    return d


def run(csv_name: str):
    data = _load(csv_name)
    for size, items in data.items():
        q: queue.Queue[str] = queue.Queue()
        samp = start_remote_sampler(q)
        log = TraceLogger(q, size, CFG.MODEL_NAME)
        time.sleep(CFG.SAMPLING_MS / 1000 * 2)
        for pid, prompt in items:
            t0 = time.time()
            resp = _completion(prompt)
            lat = time.time() - t0
            print(f"id={pid} size={size} lat={lat:.3f}s len={len(resp.split())}")
            log.mark(pid, len(prompt.split()), len(resp.split()))
        time.sleep(CFG.SAMPLING_MS / 1000 * 5)
        log.close()
        samp.join(timeout=1)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=CFG.PROMPT_FILE)
    args = ap.parse_args()
    run(args.csv)

if __name__ == "__main__":
    main()