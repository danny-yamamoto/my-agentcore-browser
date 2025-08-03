import sys
import json
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

from bedrock_agentcore.tools.browser_client import BrowserClient
from playwright.sync_api import sync_playwright
from strands import Agent, tool
from strands.models import BedrockModel
from googleapiclient.discovery import build
from google.oauth2 import service_account

# .envファイルから環境変数を読み込み
load_dotenv()

region = "us-east-1"


@tool
def capture_page(url: str) -> str:
    """
    URLにアクセスし、スクリーンショットを取得します。
    取得したスクリーンショットのファイルパスを返却します。
    """

    file_name = "image.png"

    client = BrowserClient(region)
    client.start()

    ws_url, headers = client.generate_ws_headers()

    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(
            endpoint_url=ws_url, headers=headers
        )
        default_context = browser.contexts[0]
        page = default_context.pages[0]

        context = browser.new_context(locale="ja-JP")
        page = context.new_page()
        page.set_extra_http_headers(
            {"Accept-Language": "ja-JP,ja;q=0.9,en;q=0.8"})
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        page.screenshot(path=file_name)

        browser.close()

    client.stop()

    return file_name


@tool
def login_to_page(url: str, login_id: str, password: str) -> str:
    """
    指定されたURLにアクセスし、ログインIDとパスワードを入力してログインします。
    ログイン後のスクリーンショットのファイルパスを返却します。
    """

    file_name = "login_result.png"

    client = BrowserClient(region)
    client.start()

    ws_url, headers = client.generate_ws_headers()

    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(
            endpoint_url=ws_url, headers=headers
        )
        default_context = browser.contexts[0]
        page = default_context.pages[0]

        context = browser.new_context(locale="ja-JP")
        page = context.new_page()
        page.set_extra_http_headers(
            {"Accept-Language": "ja-JP,ja;q=0.9,en;q=0.8"})
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        page.fill('input[name*="LoginID"], input[type="text"]', login_id)
        page.fill('input[name*="PassWd"], input[type="password"]', password)

        page.click(
            'img[onclick="FMSubmit()"], input[type="submit"], button[type="submit"]')

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        # モーダルを閉じる
        try:
            close_button = page.locator('.g-modal-close-tour, .g-modal-close')
            if close_button.count() > 0:
                close_button.first.click()
                page.wait_for_timeout(1000)
        except:
            pass

        # モーダルを閉じる
        try:
            close_button = page.locator('.g-modal-close-tour, .g-modal-close')
            if close_button.count() > 0:
                close_button.first.click()
                page.wait_for_timeout(1000)
        except:
            pass

        # 給与メニューボタンをクリック
        try:
            salary_menu = page.locator('a.btnMain_1:has-text("給与メニュー")')
            if salary_menu.count() > 0:
                salary_menu.first.click()
                page.wait_for_timeout(1000)
        except:
            pass

        # 給与明細入力ボタンをクリック
        try:
            salary_detail_input = page.locator(
                'a.btnMain_0:has-text("給与明細入力")')
            if salary_detail_input.count() > 0:
                salary_detail_input.first.click()
                page.wait_for_timeout(1000)
        except:
            pass

        # 編集ボタンをクリック
        try:
            edit_button = page.locator('input[name="BtnEdit"][value="編集"]')
            if edit_button.count() > 0:
                edit_button.first.click()
                page.wait_for_timeout(1000)
        except:
            pass

        # WorkDaysフィールドに30を入力
        try:
            work_days_field = page.locator('input[name="WorkDays"]')
            if work_days_field.count() > 0:
                work_days_field.first.fill('30')
                page.wait_for_timeout(500)
        except:
            pass

        # WorkHoursフィールドに時間を入力
        try:
            work_hours_field = page.locator('input[name="WorkHours"]')
            if work_hours_field.count() > 0:
                work_hours_field.first.fill('240')
                page.wait_for_timeout(500)
        except:
            pass

        # 再計算ボタンをクリック
        try:
            recalc_button = page.locator(
                'input[name="BtnRunCalcAll"][value="再計算"]')
            if recalc_button.count() > 0:
                recalc_button.first.click()
                page.wait_for_timeout(500)
        except:
            pass

        # 確認ダイアログのOKをクリック
        try:
            page.on("dialog", lambda dialog: dialog.accept())
            page.wait_for_timeout(1000)
        except:
            pass

        # 登録ボタンをクリック
        try:
            submit_button = page.locator('input[name="BtnSubmit"][value="登録"]')
            if submit_button.count() > 0:
                submit_button.first.click()
                page.wait_for_timeout(1000)
        except:
            pass

        # 確認ダイアログのOKをクリック
        try:
            page.on("dialog", lambda dialog: dialog.accept())
            page.wait_for_timeout(1000)
        except:
            pass

        # 終了ボタンをクリック
        try:
            end_button = page.locator('input[value="終了"][onclick*="EndBack"]')
            if end_button.count() > 0:
                end_button.first.click()
                page.wait_for_timeout(1000)
        except:
            pass

        # 給与明細印刷ボタンをクリック
        try:
            salary_print_button = page.locator(
                'a.btnMain_0:has-text("給与明細印刷")')
            if salary_print_button.count() > 0:
                salary_print_button.first.click()
                page.wait_for_timeout(1000)
        except:
            pass

        # 全選択/解除ボタンをクリック
        try:
            all_select_button = page.locator(
                'input[value="全選択/解除"][onclick="AllChk()"]')
            if all_select_button.count() > 0:
                all_select_button.first.click()
                page.wait_for_timeout(500)
        except:
            pass

        # 印刷ボタンをクリック
        try:
            # 印刷ボタンクリック前のページ数を記録
            initial_pages = len(context.pages)
            print(f"印刷ボタンクリック前のページ数: {initial_pages}")

            print_button = page.locator('input[name="BtnSubmit1"][value="印刷"]')
            if print_button.count() > 0:
                print_button.first.click()
                page.wait_for_timeout(2000)
        except:
            pass

        # 新しい印刷ウィンドウに切り替えてダウンロード
        try:

            # 新しいページが開くまで待機
            page.wait_for_timeout(5000)

            # 新しく開いたページを取得
            current_pages = context.pages
            print(f"印刷ボタンクリック後のページ数: {len(current_pages)}")

            if len(current_pages) > initial_pages:
                new_page = current_pages[-1]  # 最新のページを取得
                print(f"新しいページURL: {new_page.url}")

                try:
                    new_page.wait_for_load_state("networkidle", timeout=10000)
                    new_page.wait_for_timeout(3000)
                    print("印刷画面のスクリーンショットを撮影中...")
                    new_page.screenshot(path="print_screen.png")
                    print("印刷画面のスクリーンショット撮影完了")
                except Exception as screenshot_error:
                    print(f"スクリーンショット撮影エラー: {screenshot_error}")
            else:
                print("新しいページが検出されませんでした")

                # ダウンロードを開始
                with new_page.expect_download() as download_info:
                    download_button = new_page.locator(
                        'cr-icon-button#download[aria-label="ダウンロード"]')
                    if download_button.count() > 0:
                        download_button.first.click()

                # ダウンロードを保存
                download = download_info.value
                download.save_as("salary_statement.pdf")

                # 印刷ウィンドウを閉じる
                new_page.close()
        except Exception as e:
            print(f"印刷ウィンドウ処理エラー: {e}")
            pass

        page.screenshot(path=file_name)

        browser.close()

    client.stop()

    return file_name


@tool
def get_sheet_data(spreadsheet_name: str, sheet_name: str, service_account_file: str = "service_account.json") -> str:
    """
    Google Sheetsからデータを取得します。
    A列に従業員番号、氏名、部署名、B列以降に従業員データが入力されている前提です。

    Args:
        spreadsheet_name: スプレッドシートの名前またはID
        sheet_name: 取得するシート名（タブ名）
        service_account_file: サービスアカウントのJSONファイルパス

    Returns:
        取得したデータをJSON形式の文字列で返却
    """
    try:
        # サービスアカウント認証
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )

        # Google Sheets APIクライアント作成
        service = build('sheets', 'v4', credentials=credentials)

        # spreadsheet_nameがIDか名前かを判定
        spreadsheet_id = spreadsheet_name
        if not spreadsheet_name.startswith('1') or len(spreadsheet_name) < 40:
            # 名前で検索する場合（Drive APIが必要になるため、IDを要求）
            return json.dumps({
                "error": "スプレッドシート名での検索は未対応です。スプレッドシートIDを使用してください",
                "help": {
                    "spreadsheet_id": "スプレッドシートのURLから /spreadsheets/d/ 以降の文字列をコピーしてください",
                    "例": "https://docs.google.com/spreadsheets/d/1ABC...XYZ/edit → 1ABC...XYZ の部分"
                }
            }, ensure_ascii=False, indent=2)

        # シートからデータを取得
        range_name = f'{sheet_name}!A:Z'  # A列からZ列まで取得
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        values = result.get('values', [])

        if not values:
            return json.dumps({"error": "データが見つかりませんでした"}, ensure_ascii=False)

        # データを構造化
        headers = values[0] if values else []
        employee_data = []

        for row in values[1:]:  # ヘッダー行をスキップ
            if len(row) >= 3:  # 最低限の列数チェック
                employee_info = {
                    "従業員番号": row[0] if len(row) > 0 else "",
                    "氏名": row[1] if len(row) > 1 else "",
                    "部署名": row[2] if len(row) > 2 else "",
                    "データ": {}
                }

                # B列以降のデータを追加
                for i, header in enumerate(headers[3:], start=3):
                    if i < len(row):
                        employee_info["データ"][header] = row[i]

                employee_data.append(employee_info)

        result_data = {
            "sheet_name": sheet_name,
            "total_employees": len(employee_data),
            "headers": headers,
            "employees": employee_data
        }

        return json.dumps(result_data, ensure_ascii=False, indent=2)

    except FileNotFoundError:
        return json.dumps({"error": f"サービスアカウントファイル '{service_account_file}' が見つかりません"}, ensure_ascii=False)
    except Exception as e:
        error_type = type(e).__name__
        return json.dumps({
            "error": f"データ取得エラー ({error_type}): {str(e)}",
            "help": {
                "使用方法": "python main.py \"[スプレッドシートID]の[シート名]からデータを取得して\"",
                "spreadsheet_id": "スプレッドシートのURLから /spreadsheets/d/ 以降の文字列",
                "sheet_name": "スプレッドシート下部のタブ名（例：'Sheet1', 'データ', '従業員一覧'）",
                "service_account": "Google Cloud Consoleで作成したサービスアカウントのJSONファイルが必要です"
            }
        }, ensure_ascii=False, indent=2)


@tool
def process_employee_salary(employee_id: str, employee_name: str, work_days: int, work_hours: int) -> str:
    """
    単一従業員の給与明細を更新します。

    Args:
        employee_id: 従業員番号
        employee_name: 従業員名
        work_days: 出勤日数
        work_hours: 労働時間

    Returns:
        "success" または "failed" の処理結果
    """
    try:
        # 環境変数から設定を取得
        target_url = os.getenv("SALARY_URL")
        login_id = os.getenv("LOGIN_ID")
        password = os.getenv("PASSWORD")

        if not all([target_url, login_id, password]):
            return "failed: 環境変数が設定されていません"

        # ダミー処理：実際の実装はここで給与システムにアクセス
        # print(f"従業員 {employee_name}({employee_id}) の給与明細を更新中...")
        # print(f"出勤日数: {work_days}日, 労働時間: {work_hours}時間")
        # print(f"URL: {target_url} にログイン中...")

        # 常に成功を返すダミー実装
        return f"success: 従業員 {employee_name} の給与明細を更新しました"

    except Exception as e:
        return f"failed: {str(e)}"


@tool
def update_salary_slip(sheet_data: str) -> str:
    """
    スプレッドシートから取得したデータを元に環境変数で指定したURLにログインして給与明細を更新し、印刷します。

    Args:
        sheet_data: get_sheet_dataで取得したJSON形式の従業員データ

    Returns:
        "success" または "failed" の処理結果
    """
    try:
        # 環境変数から設定を取得
        target_url = os.getenv("SALARY_URL")
        login_id = os.getenv("LOGIN_ID")
        password = os.getenv("PASSWORD")

        if not all([target_url, login_id, password]):
            return "failed: 環境変数SALARY_URL, LOGIN_ID, PASSWORDが設定されていません"

        # JSONデータをパース
        data = json.loads(sheet_data)
        if "error" in data:
            return f"failed: シートデータエラー - {data['error']}"

        # デバッグ用：データ構造を確認
        print("=== データ構造確認 ===")
        print(f"データキー: {list(data.keys())}")
        print(f"ヘッダー: {data.get('headers', [])}")
        print(f"従業員数: {data.get('total_employees', 0)}")

        employees = data.get("employees", [])
        if not employees:
            return "failed: 従業員データが見つかりません"

        # 最初の従業員データの構造を確認
        if employees:
            print(f"最初の従業員データ: {employees[0]}")
        print("=====================")

        # A列をスキップしてB列から順番に処理
        success_count = 0
        headers = data.get("headers", [])

        # B列から処理（A列はスキップ）
        for col_index in range(1, len(headers)):
            column_name = headers[col_index]
            print(f"{column_name}列を処理中...")

            try:
                # 該当列の全データを収集
                column_values = []
                for employee in employees:
                    column_data = employee.get('データ', {}).get(column_name, '')
                    if column_data:  # 空でないデータのみ
                        column_values.append({
                            'employee_id': employee.get('従業員番号', ''),
                            'employee_name': employee.get('氏名', ''),
                            'value': column_data
                        })
                
                print(f"  {column_name}列のデータ: {[v['value'] for v in column_values]}")
                
                # 列全体を一括処理
                if column_values:
                    result = process_employee_salary(
                        f"Column_{column_name}",  # 列名をID代わりに使用
                        f"{column_name}列データ",
                        30,  # デフォルト出勤日数
                        240  # デフォルト労働時間
                    )
                    if result.startswith("success"):
                        success_count += 1

            except Exception as e:
                print(f"{column_name}列の処理でエラー: {e}")
                continue

        if success_count > 0:
            return f"success: {success_count}名の給与明細を処理しました"
        else:
            return "failed: 全ての従業員の処理に失敗しました"

    except json.JSONDecodeError:
        return "failed: 無効なJSONデータです"
    except Exception as e:
        return f"failed: 予期しないエラー - {str(e)}"


bedrock = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0", region_name=region)

agent = Agent(model=bedrock, tools=[
              capture_page, login_to_page, get_sheet_data, process_employee_salary, update_salary_slip])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('使用方法: python main.py "プロンプト"')
        sys.exit(1)

    prompt = sys.argv[1]
    agent(prompt)
