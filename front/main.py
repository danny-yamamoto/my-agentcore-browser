import json
import time
import uuid

import boto3
from botocore.config import Config
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="AI Agent Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    /* メインカラー設定 */
    :root {
        --primary-color: #F04600;
        --primary-dark: #D03A00;
        --primary-light: #FF6B35;
        --bg-color: #FAFAFA;
        --card-bg: #FFFFFF;
        --text-color: #333333;
        --border-color: #E0E0E0;
    }
    
    /* ヘッダースタイル */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(240, 70, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* 入力フィールドスタイル */
    .stTextInput > div > div > input {
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(240, 70, 0, 0.1);
    }
    
    /* チャットメッセージスタイル */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 1rem;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* ボタンスタイル */
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: var(--primary-dark);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(240, 70, 0, 0.2);
    }
    
    /* エラー・情報メッセージ */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    /* スピナー */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
    }
    
    /* 全体の背景 */
    .main {
        background-color: var(--bg-color);
        padding: 2rem;
    }
    
    /* カード風のコンテナ */
    .content-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# タイトル部分
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Agent Chat</h1>
    <p class="subtitle">Powered by AWS Bedrock AgentCore & Claude</p>
</div>
""", unsafe_allow_html=True)

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


# サイドバー
with st.sidebar:
    st.markdown("""
    ### 📋 使い方
    
    1. **AgentRuntime ARN**を入力
    2. チャット欄にメッセージを入力
    3. AIエージェントが自動で応答します
    
    ### 🚀 機能
    - Google Sheetsからデータ取得
    - 給与明細の自動更新
    - Webブラウザ自動操作
    
    ### ⏱️ タイムアウト設定
    - 読み取り: 5分
    - 接続: 60秒
    - リトライ: 2回
    
    ---
    
    <small>Powered by AWS Bedrock AgentCore</small>
    """, unsafe_allow_html=True)

# 設定セクション
with st.container():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    runtime_arn = st.text_input(
        label="AgentRuntime ARN",
        placeholder="arn:aws:bedrock-agentcore:us-east-1:...",
        help="AWS Bedrock AgentCore RuntimeのARNを入力してください"
    )
    st.markdown('</div>', unsafe_allow_html=True)


# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# チャット入力
if prompt := st.chat_input("メッセージを入力してください..."):
    # ユーザーメッセージを履歴に追加
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("🔄 AIエージェントが処理中..."):
        try:
            response = agent_core_client.invoke_agent_runtime(
                agentRuntimeArn=runtime_arn,
                runtimeSessionId=session_id,
                payload=json.dumps({"prompt": prompt}),
                qualifier="DEFAULT",
            )
        except Exception as e:
            st.error(f"⚠️ エラーが発生しました: {str(e)}")
            st.info("💡 処理に時間がかかる場合は、従業員を少数ずつ処理してください")
        else:
            response_body = response["response"].read()
            response_data = json.loads(response_body)

            # アシスタントの応答を結合
            assistant_response = ""
            for content in response_data["result"]["content"]:
                assistant_response += content["text"] + "\n"
            
            # アシスタントメッセージを履歴に追加
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            with st.chat_message("assistant"):
                st.write(assistant_response)
