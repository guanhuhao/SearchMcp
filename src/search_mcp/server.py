from fastmcp import FastMCP, Context
from .providers.grok import GrokSearchProvider
from .utils import format_search_results
from .logger import log_info
from .config import config
import asyncio

mcp = FastMCP("search-mcp")

grok_provider = GrokSearchProvider(config.grok_api_url, config.grok_api_key)

@mcp.tool(
    name="web_search",
    meta={"author": "GuDa"}
)
async def web_search(query: str, ctx: Context = None) -> str:
    """
    Performs a third-party web search based on the given query and returns the results
    as a JSON string.

    The `query` should be a clear, self-contained natural-language search query.
    When helpful, include constraints such as topic, time range, language, or domain
    (e.g., "过去一周的 AI 安全相关新闻", "site:fangde.com 检索检索平台文档").

    The tool automatically chooses an appropriate number of results; callers do not
    need to specify a limit explicitly.

    Returns
    -------
    str
        A JSON-encoded string representing a list of search results. Each result
        includes at least:
        - `url`: the link to the result
        - `title`: a short title
        - `summary`: a brief description or snippet of the page content.
    """
    await log_info(ctx, f"Begin Search: {query}", config.debug_enabled)
    results = await grok_provider.search(query, ctx)
    await log_info(ctx, "Search Finished!", config.debug_enabled)
    return results





def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
