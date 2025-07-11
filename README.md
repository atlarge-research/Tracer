# Tracer

Tracer is a utilitarian tool engineered as part of an effort to 
evaluate Kavier ([see thesis here](https://github.com/Radu-Nicolae/On-Simulating-LLM-Ecosystems-under-Inference))
and to collect the [LLM Trace Archive](https://github.com/atlarge-research/LLMTraceArchive/tree/70bcc9c601b5d2493aa798be159a76af6c363f5c).

## 1. What it does
1. Reads a CSV of prompts (`size, …, prompt`).
2. Sends each prompt to the **/v1/completions** HTTP endpoint exposed by vLLM.
3. In parallel, SSHes into the GPU host and samples  
   `nvidia-smi --loop-ms=<SAMPLING_MS>` (timestamp, core %, mem %).
4. Correlates every GPU sample with the current prompt-ID, input-/output-token counts,
   and writes one line per sample to `data/sample_outputs/trace_<timestamp>.csv`.

## 2. Quick start

### 2.1 Requirements
* Python ≥ 3.10  
* `requests`, `python-dotenv` (installed automatically below)  
* A running **vLLM** server you can reach over HTTP and (optionally) SSH.

### 2.2 Install
```bash
git clone https://github.com/atlarge-research/Tracer.git
cd Tracer
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt    # just 2 tiny deps
pip install -e .                   # editable install, gives the `tracer` CLI
```

### 2.3 Setup your .env file

This is how we set our .env file:
```dotenv
export SURF_URL=http://<gpu-host>:8000/v1/completions
export SURF_HOST=<gpu-host>
export SURF_USER=<ssh_user>
export SURF_KEY_PATH=keys/surf_key        # private key for SSH
# optional
export SAMPLING_MS=100                    # ms between nvidia-smi samples
export PROMPT_DIR=$(pwd)/data/sample_inputs
export TRACE_DIR=$(pwd)/data/sample_outputs
```

### 2.4.1 Run the Ecosystem serving LLM inference

### 2.4.2 Run tracer
```bash
tracer --csv for_tracing_prefill.csv
```

or

```bash
tracer --csv sample_inputs/for_tracing_decode.csv
```

### 2.5 Output
CLI will show e.g.,
```
id=0 size=64 lat=0.753s len=7
id=1 size=128 lat=0.760s len=12
...
```

CSV traces will appear in `$TRACE_DIR/trace_<timestamp>.csv`.

## 3. CSV Formats

We already provide an example of how input traces should look like and how output trace will look like.

For this, see `data/`.

## 4. License

Tracer is distributed under the MIT license. See [LICENSE.txt](/LICENSE.txt).
