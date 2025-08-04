# my-agentcore-browser
AgentCore Browser

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv version

uv venv
source .venv/bin/activate

uv add bedrock-agentcore playwright strands-agents

uv add google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

```bash
uv run main.py 
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "sheet_idのsheet_nameからデータを取得して給与明細を更新して"}'
```
