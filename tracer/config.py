import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    GPU_LIST: tuple[str, ...] = tuple(os.getenv("GPU_LIST", "A10").split(","))
    SAMPLING_MS: int = int(os.getenv("SAMPLING_MS", 100))
    PROMPT_DIR: str = os.getenv("PROMPT_DIR", str(ROOT / "data" / "inputs"))
    PROMPT_FILE: str = os.getenv("PROMPT_FILE", "for_tracing_prefill.csv")
    TRACE_DIR: str = os.getenv("TRACE_DIR", str(ROOT / "data" / "surf_traces"))
    SURF_URL: str = os.getenv("SURF_URL")
    SURF_API_KEY: str = os.getenv("SURF_API_KEY")
    SURF_HOST: str = os.getenv("SURF_HOST")
    SURF_USER: str = os.getenv("SURF_USER")
    SURF_KEY_PATH: str = os.getenv("SURF_KEY_PATH")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-8B")


CFG = Settings()
