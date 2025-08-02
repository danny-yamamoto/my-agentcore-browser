import sys

from bedrock_agentcore.tools.browser_client import BrowserClient
from playwright.sync_api import sync_playwright
from strands import Agent, tool
from strands.models import BedrockModel

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

        page.screenshot(path=file_name)

        browser.close()

    client.stop()

    return file_name


bedrock = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0", region_name=region)

agent = Agent(model=bedrock, tools=[capture_page, login_to_page])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('使用方法: python main.py "プロンプト"')
        sys.exit(1)

    prompt = sys.argv[1]
    agent(prompt)
