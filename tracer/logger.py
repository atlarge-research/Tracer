import csv, os, queue, threading
from datetime import datetime
from tracer.config import CFG


class TraceLogger:
    def __init__(self, q: queue.Queue, prompt_size: int, model: str):
        self.q = q
        self.meta = {"pid": None, "in": None, "out": None, "size": prompt_size, "model": model}
        os.makedirs(CFG.TRACE_DIR, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self.f = open(os.path.join(CFG.TRACE_DIR, f"trace_{ts}.csv"), "a", newline="")
        self.w = csv.writer(self.f)
        self.w.writerow(
            ["gpu_ts", "gpu_util", "mem_util", "logged_at", "prompt_id", "in_toks", "out_toks", "prompt_size", "model"])
        self.run = True
        self.t = threading.Thread(target=self._consume, daemon=True)
        self.t.start()

    def mark(self, pid: int, i: int, o: int):
        self.meta.update({"pid": pid, "in": i, "out": o})

    def close(self):
        self.run = False
        self.t.join()
        self.f.close()

    def _consume(self):
        while self.run or not self.q.empty():
            try:
                line = self.q.get(timeout=0.05)
            except queue.Empty:
                continue
            gpu_ts, gpu_u, mem_u = [x.strip() for x in line.split(",")]
            self.w.writerow([gpu_ts, gpu_u, mem_u, datetime.utcnow().isoformat(), self.meta["pid"], self.meta["in"],
                             self.meta["out"], self.meta["size"], self.meta["model"]])
