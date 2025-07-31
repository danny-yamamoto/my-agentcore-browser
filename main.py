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
