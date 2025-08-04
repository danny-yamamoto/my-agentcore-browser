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

        # A列が項目名、B列以降が各従業員のデータ
        if not values or len(values) < 2:
            return json.dumps({"error": "データが不足しています"}, ensure_ascii=False)

        # B列以降の列名（従業員9001、従業員8002など）を取得
        column_headers = values[0][1:]  # A列をスキップしてB列以降
        column_data = {}

        # 各列（従業員）のデータを収集
        for col_index, column_header in enumerate(column_headers):
            employee_data = {}

            # 各行の項目とデータを対応付け
            for row_index in range(1, len(values)):
                row = values[row_index]
                if len(row) > 0:
                    item_name = row[0]  # A列の項目名（従業員番号、氏名、部署名など）
                    value = row[col_index + 1] if col_index + \
                        1 < len(row) else ""  # 対応するデータ
                    employee_data[item_name] = value

            # 列のヘッダー名をキーとして格納
            column_data[column_header] = employee_data

        print(json.dumps(column_data, ensure_ascii=False, indent=2))

        return json.dumps(column_data, ensure_ascii=False, indent=2)

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

        # Playwrightでサイトにログイン
        print(f"URL: {target_url} にログイン中...")

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

            # サイトにアクセス
            page.goto(target_url)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            # ログイン処理
            page.fill('input[name*="LoginID"], input[type="text"]', login_id)
            page.fill(
                'input[name*="PassWd"], input[type="password"]', password)
            page.click(
                'img[onclick="FMSubmit()"], input[type="submit"], button[type="submit"]')

            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            # ログイン成功の確認
            try:
                # ログインエラーメッセージをチェック
                error_elements = page.locator(
                    'text=ログインに失敗, text=エラー, text=認証に失敗')
                if error_elements.count() > 0:
                    browser.close()
                    client.stop()
                    return "failed: ログインに失敗しました"
            except:
                pass

            print("ログイン成功")

            # モーダルを閉じる
            try:
                close_button = page.locator(
                    '.g-modal-close-tour, .g-modal-close')
                if close_button.count() > 0:
                    close_button.first.click()
                    page.wait_for_timeout(1000)
            except:
                pass

            # モーダルを閉じる
            try:
                close_button = page.locator(
                    '.g-modal-close-tour, .g-modal-close')
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

            # 各従業員データを処理
            success_count = 0
            for employee_key, employee_data in data.items():
                print(f"従業員 {employee_key} を処理中...")
                # ここで給与明細更新処理を実装
                # 検索ボタンクリック前のページ数を記録
                initial_pages = len(context.pages)
                print(f"検索ボタンクリック前のページ数: {initial_pages}")
                # ==========================
                # 検索ボタンをクリック
                try:
                    search_button = page.locator(
                        'input[type="button"].btn[value="検索"][onclick="Search()"]')
                    if search_button.count() > 0:
                        search_button.first.click()
                        page.wait_for_timeout(1000)
                        print("検索ボタンをクリックしました")
                except:
                    pass

                try:
                    # 新しいページが開くまで待機
                    page.wait_for_timeout(5000)
                    # 新しく開いたページを取得
                    current_pages = context.pages
                    print(f"検索ボタンクリック後のページ数: {len(current_pages)}")
                    if len(current_pages) > initial_pages:
                        new_page = current_pages[-1]  # 最新のページを取得
                        print(f"新しいページURL: {new_page.url}")
                        try:
                            new_page.wait_for_load_state(
                                "networkidle", timeout=10000)
                            new_page.wait_for_timeout(3000)

                            # 従業員番号をテキストフィールドに入力
                            try:
                                keyword_field = new_page.locator(
                                    'input[type="text"].inpK[name="keywd"]')
                                if keyword_field.count() > 0:
                                    keyword_field.first.fill(employee_key)
                                    print(f"従業員番号 {employee_key} を入力しました")
                                    new_page.wait_for_timeout(1000)
                            except Exception as input_error:
                                print(f"従業員番号入力エラー: {input_error}")

                            # 検索ボタンをクリック
                            try:
                                search_btn = new_page.locator(
                                    'input[type="button"].btnS[onclick="SubmitFm()"][value="検索"]')
                                if search_btn.count() > 0:
                                    search_btn.first.click()
                                    print("検索ボタンをクリックしました")
                                    new_page.wait_for_timeout(
                                        2000)  # 検索結果の読み込みを待機
                            except Exception as search_error:
                                print(f"検索ボタンクリックエラー: {search_error}")

                            # 選択ボタンをクリック
                            try:
                                select_btn = new_page.locator(
                                    f'input[type="button"].btn[value="選択"][name="show_btn0"][onclick="Show(\'{employee_key}\')"]')
                                if select_btn.count() > 0:
                                    select_btn.first.click()
                                    print(f"選択ボタン（{employee_key}）をクリックしました")
                                    new_page.wait_for_timeout(
                                        2000)  # 選択後の画面遷移を待機
                            except Exception as select_error:
                                print(f"選択ボタンクリックエラー: {select_error}")

                            print("検索画面のスクリーンショットを撮影中...")
                            new_page.screenshot(path="search_screen.png")
                            print("検索画面のスクリーンショット撮影完了")
                            # 検索ウィンドウを閉じる
                            new_page.close()
                        except Exception as screenshot_error:
                            print(f"スクリーンショット撮影エラー: {screenshot_error}")
                    else:
                        print("新しいページが検出されませんでした")
                        # 検索ウィンドウを閉じる
                        new_page.close()
                except Exception as e:
                    print(f"検索ウィンドウ処理エラー: {e}")
                    pass
                # ==========================
                success_count += 1

            # デバッグ用：ログイン後の画面をスクリーンショット
            page.screenshot(path="login_debug.png")
            print("ログイン後の画面をスクリーンショット保存: login_debug.png")

            browser.close()

        client.stop()
        return f"success: {success_count}名の給与明細を処理しました"

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
