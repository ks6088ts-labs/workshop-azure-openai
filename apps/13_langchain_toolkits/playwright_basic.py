import asyncio
import logging
import time

import typer
from dotenv import load_dotenv
from playwright.async_api import Page, async_playwright
from playwright.sync_api import sync_playwright

load_dotenv()
logger = logging.getLogger(__name__)
app = typer.Typer()


async def scrape_task(page: Page, page_number: int):
    url = f"https://expert.visasq.com/issue/?keyword=&is_started_only=true&page={page_number}"
    print(f"Downloading {url}...")
    try:
        await page.goto(url)
        await page.wait_for_load_state()
        await page.screenshot(
            path=f"screenshot_{page_number}.png",
            full_page=True,
        )
    except Exception as e:
        logger.error(f"error: {e}, url: {url}")
    print(f"Downloaded {url}")


async def _get_visasq_cases():
    tasks = []
    async with async_playwright() as p:
        logger.debug("Launch browser")

        browser = await p.chromium.launch()
        context = await browser.new_context()

        for i in range(1, 20):
            page = await context.new_page()
            tasks.append(
                asyncio.create_task(
                    scrape_task(
                        page=page,
                        page_number=i,
                    )
                )
            )
        await asyncio.gather(*tasks)

        # Finalize
        await context.close()
        await browser.close()


@app.command()
def get_visasq_cases(
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    start = time.time()
    asyncio.run(_get_visasq_cases())
    end = time.time()
    elapsed_time = end - start
    print(f"経過時間:{elapsed_time:.2f} 秒")


@app.command()
def get_yahoo_realtime_trends(
    verbose: bool = False,
) -> None:
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    with sync_playwright() as p:
        logger.debug("Launch browser")
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        logger.debug("Go to Yahoo Realtime Trends")
        page.goto(url="https://search.yahoo.co.jp/realtime")
        trends = []
        for i in range(20):
            keyword = page.get_by_role("link", name=f"{i+1}", exact=True).text_content()
            trends.append(
                {
                    "rank": i + 1,
                    "keyword": keyword,
                },
            )
        # Finalize
        context.close()
        browser.close()

    print(trends)


if __name__ == "__main__":
    app()
