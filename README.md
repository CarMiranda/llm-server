llm-server
---

Simple implementation of a server to chat with an LLM.

# Run the server
To run a server with an LLM:
```bash
uv run llm-api
```

This spawns a FastAPI server hosting a preloaded LLM. It currently uses `TinyLlama/TinyLlama-1.1B-Chat-v1.0` but this can be replaced in `src/llm_server/model.py`.

# Run the CLI
To run the CLI (chat) using the API:
```bash
uv run --group=cli llm-cli api --chat-id 0 http://0.0.0.0:3000
```

If you close and rerun the command with the same `chat-id`, you will continue the conversation, while the server is up.

To run the CLI against a local LLM directly:
```bash
uv run --group=cli llm-cli local
```

To end the chat, just enter the message "EOC".


# Roadmap

- Integrate more configuration options (e.g. select models)
- Add MCP options
- Add chat persistence
