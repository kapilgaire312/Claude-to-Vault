import asyncio
import logging

from playwright.async_api import TimeoutError, async_playwright

logger = logging.getLogger(__name__)


async def scrape_claude_chat(url: str) -> list[dict[str, str]]:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
        )
        try:
            page = await browser.new_page()
            await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60_000,
            )
            # await asyncio.sleep(5)
            # rather than randomly waiting for chat to load, wait till the chat wrapper div is visible
            transcript = page.locator('[data-testid="transcript-list"]')
            try:
                await transcript.wait_for(
                    state="visible",
                    timeout=10_000,
                )
            except TimeoutError:
                logger.warning("Transcript did not appear within timeout; checking for bot verification.")
                # check cloudflare bot detection
                body_text = await page.locator("body").inner_text()

                if "Performing security verification" in body_text:
                    logger.warning("Cloudflare verification required; waiting for user input.")
                    input("Complete the human verification and hit enter...")

                # wait for the transcipt to load
                await transcript.wait_for(state="visible", timeout=20_000)

            """
        user_messages = transcript.locator('[data-testid="user-message"]')
        print("no of user messages", await user_messages.count())
        for i in range(await user_messages.count()):
            print(await user_messages.nth(i).inner_text())

        assistant_messages = transcript.locator("[data-perf-reply-text]")
        print("no of assistant messages", await assistant_messages.count())
        """
            # to get the chat in order, we can give both selectors to the locator, it will give the elements in the order they appear in DOM
            nodes = transcript.locator(
                '[data-testid="user-message"], [data-perf-reply-text]'
            )

            total_message_count = await nodes.count()

            user_message_count = await transcript.locator(
                '[data-testid="user-message"]'
            ).count()
            claude_message_count = await transcript.locator(
                "[data-perf-reply-text]"
            ).count()

            logger.info("Total messages: %s", total_message_count)
            logger.info("User messages count: %s", user_message_count)
            logger.info("Claude messages count: %s", claude_message_count)

           

            if user_message_count == 0:
                raise Exception("User mesage count is 0. Failed to read user messages.")

            if claude_message_count == 0:
                raise Exception(
                    "Claude message count is 0. Failed to read claude messages."
                )
            # construct the chat
            messages = []
            for i in range(await nodes.count()):
                node = nodes.nth(i)

                testid = await node.get_attribute("data-testid")
                if testid == "user-message":
                    role = "Developer"

                else:
                    role = "AI Tutor"

                content = (await node.inner_text()).strip()
                messages.append({"role": role, "content": content})

            return messages

        finally:
            await browser.close()


async def main():
    url = "https://claude.ai/share/49eddefd-3a84-4ca9-81af-b9637ad7a3b6"
    messages = await scrape_claude_chat(url)
    logger.info(f"Scraped messages: {messages}")


if __name__ == "__main__":
    asyncio.run(main())
