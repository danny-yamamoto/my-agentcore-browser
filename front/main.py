import json
import time
import uuid

import boto3
from botocore.config import Config
import streamlit as st

# タイムアウト設定を含むConfig
config = Config(
    read_timeout=300,  # 読み取りタイムアウト: 5分
    connect_timeout=60,  # 接続タイムアウト: 60秒
    retries={'max_attempts': 2}  # リトライ回数
)

# bedrock-agentcoreのクライアント
agent_core_client = boto3.client(
    "bedrock-agentcore", region_name="us-east-1", config=config)

# セッションID。33文字以上ないとエラーになる
session_id = str(int(time.time())) + "_" + str(uuid.uuid4()).replace("-", "")


st.title("PoC AI Agent Chat")
# st.write("Streamlit + Bedrock AgentCore + Strands Agents")

runtime_arn = st.text_input(label="AgentRuntime ARN")


if prompt := st.chat_input():
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner():
        try:
            response = agent_core_client.invoke_agent_runtime(
                agentRuntimeArn=runtime_arn,
                runtimeSessionId=session_id,
                payload=json.dumps({"prompt": prompt}),
                qualifier="DEFAULT",
            )
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            st.info("処理に時間がかかる場合は、従業員を少数ずつ処理してください")
        else:
            response_body = response["response"].read()
            response_data = json.loads(response_body)

            with st.chat_message("assistant"):
                for content in response_data["result"]["content"]:
                    st.write(content["text"])
