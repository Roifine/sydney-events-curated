import asyncio
import os
import json
import re
from openai import AsyncOpenAI
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = AsyncOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

async def crawl_events(url):
    browser_config = BrowserConfig()
    run_config = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)
        return result.markdown

async def call_deepseek(markdown_text):
    prompt = (
        "Extract a list of events from the following content. Just provide the first 3 results. "
        "Return a JSON array with each item containing:\n"
        "- 'event title'\n"
        "- 'event description'\n"
        "- 'event link'\n"
        "- 'event time'\n"
        "Ensure the event time is in this format: Friday 23rd May"
        "- 'event location. Ensure the event location is a valid name, if it's not avialbale just write unknown as the value'\n\n"
        "Ensure valid JSON format with proper quotation marks and escaping.\n"
        "If one of the evnet values do not exist leave value as "".\n"
        "Only output the JSON array. Double check that the output could be saved as json file.\n\n"
        f"CONTENT:\n{markdown_text}"
    )

    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

def sanitize_json(json_str):
    json_str = re.sub(r"```(?:json)?", "", json_str)
    json_str = re.sub(r"```", "", json_str)
    json_str = json_str.strip()

    match = re.search(r"\[\s*{.*}\s*]", json_str, re.DOTALL)
    if match:
        return match.group(0)
    return json_str

def save_to_json(events_str, filename="events.json"):
    try:
        sanitized = sanitize_json(events_str)
        events = json.loads(sanitized)

        if not isinstance(events, list):
            raise ValueError("Top-level JSON is not a list.")

        for i, event in enumerate(events):
            for field in ['event title', 'event description', 'event link', 'event time', 'event location']:
                if field not in event:
                    raise ValueError(f"Missing field '{field}' in event {i+1}")

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {len(events)} events to {filename}")
    
    except Exception as e:
        print("❌ Error saving events:", str(e))
        print("Raw content returned from DeepSeek:")
        print(events_str)

async def main():
    for site, filename in [
        ("https://www.broadsheet.com.au/sydney/entertainment", "events_concrete.json"),
        ("https://www.enmoretheatre.com.au/?s&key=upcoming", "events_enmore.json"), ("https://www.ourgoldenage.com.au/live-music", "events_golden.json")
        , ("https://www.sff.org.au/program/", "events_film_fest.json")
    ]:
        print(f"🕸️ Crawling {site}...")
        markdown = await crawl_events(site)

        print("🤖 Sending content to DeepSeek...")
        result = await call_deepseek(markdown)

        print("📦 Extracted Events JSON:")
        print(result)

        print("\n🧹 Sanitized JSON:")
        print(sanitize_json(result))

        save_to_json(result, filename)

if __name__ == "__main__":
    asyncio.run(main())
