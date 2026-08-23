# syntax=docker/dockerfile:1.7@sha256:a57df69d0ea827fb7266491f2813635de6f17269be881f696fbfdf2d83dda33e
FROM ghcr.io/astral-sh/uv:0.12.5-python3.12-trixie-slim@sha256:4677e08839853fe91c523b593f822ec1e87c7b91ba4c6b30929016b2e0933cd5

ENV PATH="/opt/venv/bin:${PATH}" \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /opt/skill

COPY scripts/run_reference_inference.py scripts/run_reference_inference.py.lock ./scripts/
COPY scripts/profiles/ ./scripts/profiles/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv /opt/venv \
    && uv export --locked --script scripts/run_reference_inference.py \
        --output-file /tmp/requirements.txt \
    && uv pip install --python /opt/venv/bin/python \
        --require-hashes --requirements /tmp/requirements.txt \
    && rm /tmp/requirements.txt \
    && python -c "import accelerate, PIL, torch, transformers"

RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin worker
USER 10001:10001

ENTRYPOINT ["python", "/opt/skill/scripts/run_reference_inference.py"]
CMD ["--help"]
