import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import random
import pandas as pd

async def mouse_moves(page):
    # Simulate human-like mouse movements
    viewport=page.viewport_size
    if viewport:
        width=viewport["width"]
        height=viewport["height"]
        x=random.randint(0,width)
        y=random.randint(0,height)
        await page.mouse.move(x,y,steps=random.randint(5,15))
        await asyncio.sleep(1)

async def scroll_humanly_to_bottom(page, scroll_times=10):
    for i in range(scroll_times):
        # Fixed: Single set of quotes and properly awaited
        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        await asyncio.sleep(random.uniform(1, 2))
        await mouse_moves(page)

        new_height = await page.evaluate("document.body.scrollHeight")
        print(f"Scrolled {i+1} times, new height: {new_height}")

async def main():
    async with async_playwright() as p:
        stealth_engine = Stealth()
        products = []
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        await stealth_engine.apply_stealth_async(context)

        page = await context.new_page()
        print("Navigating to Jumia Kenya...")
        await page.goto("https://www.jumia.co.ke/smartphones", wait_until="domcontentloaded",timeout=60000)
        await asyncio.sleep(random.uniform(2,4)) #wait for the page to load completely and simulate human reading
        await mouse_moves(page)

        print("waiting for products to appear...")
        try: 
            await page.wait_for_selector("article.prd", timeout=10000)
            await scroll_humanly_to_bottom(page, scroll_times=5)

            # Get the list of locators correctly
            product_cards = await page.locator("article.prd").all()
            # Use len() because product_cards is now a list
            count = len(product_cards)
            print(f"Found {count} products on the page.")

            for i, product in enumerate(product_cards):
                try:
                    # We don't 'await' the locator itself, only the extraction
                    name_el = product.locator(".name")
                    price_el = product.locator(".prc")
                    
                    # Extract text safely
                    name = await name_el.inner_text() if await name_el.count() > 0 else "N/A"
                    price = await price_el.inner_text() if await price_el.count() > 0 else "N/A"
                    
                    products.append({"name": name.strip(), "price": price.strip()})
                    
                    if i % 10 == 0: # Print progress every 10 items
                        print(f"Processed {i} products...")
                        await mouse_moves(page)

                except Exception as e:
                    print(f"Error extracting product {i+1}")

        except Exception as e:
            print(f"Error: {e}")
            await page.screenshot(path="debug_screen.png")
        
        finally:
            if products:
                df = pd.DataFrame(products)
                df.to_csv("jumia_products.csv", index=False)
                print(f"Saved {len(products)} products to jumia_products.csv")
            else:
                print("No products found to save.")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())