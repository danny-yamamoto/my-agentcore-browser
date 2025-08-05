# my-agentcore-browser
AgentCore Browser - 給与明細自動更新システム

## アーキテクチャ図

```mermaid
graph TB
    User[👤 ユーザー] -->|💬 プロンプト| Agent[🤖 Strands Agent]
    
    subgraph Core ["🔧 main.py - コア処理"]
        Agent --> Tools{⚙️ ツール選択}
        
        Tools -->|📊 データ取得| GetSheet[📈 get_sheet_data]
        Tools -->|💰 給与更新| UpdateSalary[💼 update_salary_slip]
        
        subgraph DataFlow ["📊 get_sheet_data処理"]
            GetSheet --> EnvVar1[🔑 環境変数取得<br/>GOOGLE_SERVICE_ACCOUNT_JSON]
            EnvVar1 --> GoogleAuth[🔐 Google認証]
            GoogleAuth --> SheetsAPI[📋 Google Sheets API]
            SheetsAPI --> DataFormat[🔄 データ構造化<br/>列単位→JSON]
        end
        
        subgraph WebFlow ["🌐 update_salary_slip処理"]
            UpdateSalary --> EnvVar2[🔑 環境変数取得<br/>SALARY_URL<br/>LOGIN_ID<br/>PASSWORD]
            EnvVar2 --> Browser[🖥️ Playwright<br/>ブラウザ起動]
            Browser --> Login[🔓 サイトログイン]
            Login --> Search[🔍 従業員検索]
            Search --> Edit[✏️ 編集ボタン]
            Edit --> InputData[⌨️ データ入力<br/>WorkDays/WorkHours]
            InputData --> Calculate[🧮 再計算]
            Calculate --> Submit[✅ 登録]
            Submit --> Complete[🎉 処理完了]
        end
    end
    
    subgraph External ["🌍 外部システム"]
        GoogleSheets[(📊 Google Sheets<br/>従業員データ)]
        Bedrock[🧠 AWS Bedrock<br/>Claude Sonnet 4]
    end
    
    subgraph Config ["⚙️ 設定・ログ"]
        EnvFile[📄 .env<br/>環境変数]
        Logger[📝 ログシステム<br/>DEBUG/INFO/ERROR]
        Screenshots[📷 スクリーンショット<br/>デバッグ用]
    end
    
    SheetsAPI <-->|📡 API| GoogleSheets
    Agent <-->|🤝 AI| Bedrock
    
    EnvVar1 -.->|📖 読込| EnvFile
    EnvVar2 -.->|📖 読込| EnvFile
    UpdateSalary -.->|📝 出力| Logger
    Browser -.->|📸 保存| Screenshots
    
    %% 色設定 - 3色のテーマ
    %% プライマリー（青系）- コア機能
    style Agent fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style Tools fill:#64B5F6,stroke:#1976D2,stroke-width:2px,color:#fff
    style GetSheet fill:#90CAF9,stroke:#1976D2,stroke-width:2px,color:#000
    style UpdateSalary fill:#90CAF9,stroke:#1976D2,stroke-width:2px,color:#000
    
    %% セカンダリー（緑系）- 外部システム
    style GoogleSheets fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style Bedrock fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    
    %% アクセント（オレンジ系）- 設定・ログ
    style EnvFile fill:#FF9800,stroke:#F57C00,stroke-width:2px,color:#fff
    style Logger fill:#FFB74D,stroke:#F57C00,stroke-width:2px,color:#000
    style Screenshots fill:#FFB74D,stroke:#F57C00,stroke-width:2px,color:#000
    
    %% 処理ステップ（薄い青）
    style EnvVar1 fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style GoogleAuth fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style SheetsAPI fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style DataFormat fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style EnvVar2 fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style Browser fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style Login fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style Search fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style Edit fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style InputData fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style Calculate fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style Submit fill:#E3F2FD,stroke:#1976D2,stroke-width:1px,color:#000
    style Complete fill:#C8E6C9,stroke:#388E3C,stroke-width:2px,color:#000
```

## システム概要

本システムは、Google Sheetsから従業員データを取得し、Webベースの給与システムに自動でログインして給与明細を更新するAIエージェントです。

### 主要機能

1. **データ取得** (`get_sheet_data`)
   - Google Sheets APIで従業員データを取得
   - 列単位でのデータ構造化
   - 環境変数による認証情報管理

2. **給与明細更新** (`update_salary_slip`)
   - Playwrightによるブラウザ自動化
   - Webアプリへの自動ログイン
   - 従業員検索・選択・データ入力
   - 再計算・登録処理

3. **AI制御**
   - Strands フレームワークによるツール選択
   - AWS Bedrock Claude Sonnet 4 による自然言語処理

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

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AssumeRolePolicy",
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock-agentcore.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "XXXXXXXXXXXX"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:*"
        }
      }
    }
  ]
}
```

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ECRImageAccess",
      "Effect": "Allow",
      "Action": [
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ],
      "Resource": [
        "arn:aws:ecr:us-east-1:XXXXXXXXXXXX:repository/my-agentcore-browser"
      ]
    },
    {
      "Sid": "ECRTokenAccess",
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CloudWatchLogs",
      "Effect": "Allow",
      "Action": [
        "logs:DescribeLogStreams",
        "logs:CreateLogGroup",
        "logs:DescribeLogGroups"
      ],
      "Resource": [
        "arn:aws:logs:us-east-1:XXXXXXXXXXXX:log-group:/aws/bedrock-agentcore/runtimes/*",
        "arn:aws:logs:us-east-1:XXXXXXXXXXXX:log-group:*"
      ]
    },
    {
      "Sid": "CloudWatchLogsWrite",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "arn:aws:logs:us-east-1:XXXXXXXXXXXX:log-group:/aws/bedrock-agentcore/runtimes/*:log-stream:*"
      ]
    },
    {
      "Sid": "XRayAccess",
      "Effect": "Allow",
      "Action": [
        "xray:PutTraceSegments",
        "xray:PutTelemetryRecords",
        "xray:GetSamplingRules",
        "xray:GetSamplingTargets"
      ],
      "Resource": ["*"]
    },
    {
      "Sid": "CloudWatchMetrics",
      "Effect": "Allow",
      "Resource": "*",
      "Action": "cloudwatch:PutMetricData",
      "Condition": {
        "StringEquals": {
          "cloudwatch:namespace": "bedrock-agentcore"
        }
      }
    },
    {
      "Sid": "GetAgentAccessToken",
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:GetWorkloadAccessToken",
        "bedrock-agentcore:GetWorkloadAccessTokenForJWT",
        "bedrock-agentcore:GetWorkloadAccessTokenForUserId"
      ],
      "Resource": [
        "arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:workload-identity-directory/default",
        "arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:workload-identity-directory/default/workload-identity/*"
      ]
    },
    {
      "Sid": "BedrockModelInvocation",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/*",
        "arn:aws:bedrock:us-east-1:XXXXXXXXXXXX:*"
      ]
    }
  ]
}
```

```bash
agentcore status
```
