import asyncio

from playwright.async_api import TimeoutError, async_playwright


async def scrape_claude_chat(url: str):
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
                print("timed out")
                # check cloudflare bot detection
                body_text = await page.locator("body").inner_text()

                if "Performing security verification" in body_text:
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

            print("Total messages:", await nodes.count())

            # construct the chat
            messages = []
            for i in range(await nodes.count()):
                node = nodes.nth(i)

                testid = await node.get_attribute("data-testid")
                if testid == "user-message":
                    role = "user"

                else:
                    role = "assistant"

                content = (await node.inner_text()).strip()
                messages.append({"role": role, "content": content})

            return messages

        finally:
            await browser.close()


async def main():
    url = "https://claude.ai/share/49eddefd-3a84-4ca9-81af-b9637ad7a3b6"
    messages = await scrape_claude_chat(url)
    print(messages)


if __name__ == "__main__":
    asyncio.run(main())
