import threading, subprocess, queue
from tracer.config import CFG


def start_remote_sampler(out: queue.Queue, loop_ms: int = CFG.SAMPLING_MS):
    cmd = [
        "ssh",
        "-i", CFG.SURF_KEY_PATH,
        "-o", "StrictHostKeyChecking=no",
        f"{CFG.SURF_USER}@{CFG.SURF_HOST}",
        f"nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory --format=csv,noheader,nounits --loop-ms={loop_ms}"]

    def _reader():
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
        try:
            for line in proc.stdout:
                out.put(line.strip())
        finally:
            proc.kill()

    t = threading.Thread(target=_reader, daemon=True)
    t.start()
    return t
