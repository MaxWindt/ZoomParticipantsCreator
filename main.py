import flet as ft
import asyncio
from playwright.async_api import async_playwright, expect
import threading


class ZoomLinkOpener:
    def __init__(self):
        self.browser_contexts = []
        self.running = False
        self.stop_event = asyncio.Event()

    async def open_browser_windows(self, link, count, on_complete=None):
        if "https://us05web.zoom.us/j/" in link:
            link = link.replace("https://us05web.zoom.us/j/", "https://app.zoom.us/wc/")
            link = link.replace("?pwd=", "/join?pwd=")
        self.running = True
        self.stop_event.clear()

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=True,
                args=[
                    "--mute-audio --no-first-run --disable-sync --disable-extensions --disable-component-update --disable-background-networking"
                ],
            )
            
            # Create a list of tasks to open browser contexts concurrently
            tasks = []
            for i in range(count):
                if not self.running:
                    break
                tasks.append(self.create_browser_context(browser, link, i+1))
            
            # Run all the browser context creation tasks concurrently
            if tasks:
                # Use gather with return_exceptions=True to prevent one failure from stopping all tasks
                await asyncio.gather(*tasks, return_exceptions=True)

            # Wait until stop button is clicked
            await self.stop_event.wait()

            # Clean up browser contexts
            for context in self.browser_contexts:
                await context.close()
            await browser.close()

            self.browser_contexts = []
            self.running = False

            print("Test completed successfully!")

            if on_complete:
                await on_complete()
    
    async def create_browser_context(self, browser, link, index=0):
        """Create a single browser context and navigate to the Zoom meeting"""
        try:
            context = await browser.new_context(
                viewport={"width": 420, "height": 680},
                locale="en-US",
                permissions=[],
            )
            self.browser_contexts.append(context)
            page = await context.new_page()
            
            # Add timeout to page operations
            page.set_default_timeout(30000)  # 30 seconds timeout
            
            await page.goto(link)
            
            try:
                # Wait for and click "Accept Cookies" if it exists
                if await page.get_by_role("button", name="Accept Cookies").count() > 0:
                    await page.get_by_role("button", name="Accept Cookies").click()
                
                # Wait for and click "I Agree" if it exists
                if await page.get_by_role("button", name="I Agree").count() > 0:
                    await page.get_by_role("button", name="I Agree").click()
                
                await page.get_by_label("Your Name").fill(generate_random_name())
                await page.get_by_label("Your Name").press("Enter")
                await page.get_by_role("button", name="Join").click()
                
                print(f"Participant {index} joined successfully")
                
                # Try to stop incoming video to save bandwidth
                try:
                    await asyncio.sleep(1)  # Short delay to ensure UI is loaded
                    if await page.get_by_label("More meeting control").count() > 0:
                        await page.get_by_label("More meeting control").evaluate(
                            """
                            button => button.click()
                            """
                        )
                        
                        if await page.get_by_label("Stop Incoming Video").count() > 0:
                            await page.get_by_label("Stop Incoming Video").evaluate(
                                """
                                button => button.click()
                                """
                            )
                            print(f"Stopped incoming video for participant {index}")
                except Exception as e:
                    print(f"Stopping incoming video was not successful for participant {index}: {str(e)}")
            except Exception as e:
                print(f"Error during meeting join process for participant {index}: {str(e)}")
                # Close this context if there was an error during the join process
                await context.close()
                # Remove from tracking list
                if context in self.browser_contexts:
                    self.browser_contexts.remove(context)
        except Exception as e:
            print(f"Error creating browser context for participant {index}: {str(e)}")


def main(page: ft.Page):
    page.title = "Zoom Participants Creator"
    page.padding = 20
    page.window.height = 400
    page.window.width = 500

    zoom_opener = ZoomLinkOpener()

    # UI Components
    link_input = ft.TextField(
        label="Zoom Link", hint_text="Paste Zoom meeting link here", width=600
    )

    count_input = ft.TextField(
        label="Number of Participants",
        hint_text="Enter the number of random participants",
        width=200,
        value="1",
    )

    status_text = ft.Text(value="Ready", color=ft.colors.GREEN)

    async def start_process():
        try:
            link = link_input.value
            count = int(count_input.value)

            if not link:
                status_text.value = "Please enter a Zoom link"
                status_text.color = ft.colors.RED
                page.update()
                return

            if count <= 0:
                status_text.value = "Please enter a positive number of windows"
                status_text.color = ft.colors.RED
                page.update()
                return
            
            # Add a warning for high numbers of participants
            if count > 10:
                status_text.value = "Warning: Creating many participants may use significant system resources"
                status_text.color = ft.colors.ORANGE
                page.update()
                await asyncio.sleep(2)  # Show warning for 2 seconds

            status_text.value = f"Joining with {count} participants..."
            status_text.color = ft.colors.BLUE
            start_button.text = "Stop"
            page.update()

            async def on_complete():
                await update_ui_after_stop()

            # Start browser opening in a separate thread
            threading.Thread(
                target=lambda: asyncio.run(
                    zoom_opener.open_browser_windows(link, count, on_complete)
                )
            ).start()

        except ValueError:
            status_text.value = "Please enter a valid number of participants"
            status_text.color = ft.colors.RED
            page.update()

    async def stop_process():
        zoom_opener.running = False
        zoom_opener.stop_event.set()

    async def update_ui_after_stop():
        start_button.text = "Start"
        status_text.value = "Ready"
        status_text.color = ft.colors.GREEN
        page.update()

    async def handle_button_click(e):
        if start_button.text == "Start":
            await start_process()
        else:
            await stop_process()

    start_button = ft.ElevatedButton(
        text="Start",
        width=100,
        on_click=handle_button_click,
    )

    # Layout
    page.add(
        ft.Column(
            [
                ft.Text(
                    "Zoom Participants Creator", size=24, weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Enter a Zoom link and specify how many participants should join"
                ),
                ft.Container(height=20),
                link_input,
                ft.Container(height=10),
                count_input,
                ft.Container(height=20),
                start_button,
                ft.Container(height=20),
                status_text,
            ],
            spacing=0,
        )
    )


import random
import string


def generate_random_name():
    # Random prefixes
    prefixes = ["DE", "DE/EN", "EN", "NT"]

    # Random names
    german_names = [
        "Hans",
        "Heidi",
        "Lena",
        "Matthias",
        "Sabine",
        "Klaus",
        "Maria",
        "Dieter",
        "Anna",
        "Markus",
    ]

    spanish_names = [
        "Alejandro",
        "Elena",
        "Diego",
        "Sofía",
        "Javier",
        "Isabella",
        "Carlos",
        "Carmen",
        "Antonio",
        "Lucía",
    ]

    us_names = [
        "John",
        "Emily",
        "Michael",
        "Sarah",
        "William",
        "Jessica",
        "David",
        "Ashley",
        "James",
        "Jennifer",
    ]

    # Merge all names
    names = german_names + spanish_names + us_names

    # Generate random prefix
    random_prefix = random.choice(prefixes)

    # Generate random name
    random_name = random.choice(names)

    # Generate unique identifier (random letters)
    unique_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

    # Concatenate prefix, name, and unique string
    random_string = f"{random_prefix} - {random_name} - {unique_string}"

    return random_string


# Run the application
if __name__ == "__main__":
    ft.app(target=main)