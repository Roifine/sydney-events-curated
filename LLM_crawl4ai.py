import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def main():
    # Setup content filtering and markdown generator
    md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.3, threshold_type="fixed")
    )

    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator
    )

    url = "https://concreteplayground.com/sydney/events"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)
        markdown = result.markdown.fit_markdown

        print("\n--- Extracted Markdown ---\n")
        print(markdown[:2000])  # print first 2000 chars for quick proof-of-concept

# Run the crawler
asyncio.run(main())
