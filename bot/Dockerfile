FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN useradd -m bot
USER bot
RUN curl -fsSL https://claude.ai/install.sh | bash
ENV PATH="/home/bot/.local/bin:$PATH" PYTHONUNBUFFERED=1

WORKDIR /app
COPY --chown=bot . .
RUN pip install --user -e .
CMD ["bot"]
