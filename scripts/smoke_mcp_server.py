"""End-to-end STDIO smoke test for the DietaryIndex MCP server."""

from __future__ import annotations

import asyncio
import argparse
import os
import sys
import tempfile
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", default=sys.executable)
    parser.add_argument("command_args", nargs=argparse.REMAINDER)
    options = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="dietaryindex-mcp-smoke-") as temp_dir:
        temp_root = Path(temp_dir)
        allowed_root = temp_root / "allowed"
        output_root = temp_root / "outputs"
        allowed_root.mkdir()
        allowed_file = allowed_root / "preview.csv"
        allowed_file.write_text("participant_id,fruit\n1,2.5\n", encoding="utf-8")
        blocked_file = temp_root / "blocked.csv"
        blocked_file.write_text("participant_id,fruit\n2,3.5\n", encoding="utf-8")
        server_env = os.environ.copy()
        server_env["DIETARYINDEX_MCP_ALLOWED_ROOTS"] = str(allowed_root)
        server_env["DIETARYINDEX_MCP_OUTPUT_ROOT"] = str(output_root)
        server = StdioServerParameters(
            command=options.command,
            args=options.command_args or ["-m", "dietaryindex.mcp_server"],
            env=server_env,
        )
        async with stdio_client(server) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools = await session.list_tools()
                names = {tool.name for tool in tools.tools}
                expected = {
                    "list_indices",
                    "get_index",
                    "preview_dataset",
                    "suggest_dataset_mapping",
                    "compute_index",
                    "search_fii_foods",
                    "get_fii_food",
                }
                missing = expected - names
                if missing:
                    raise RuntimeError(f"Missing MCP tools: {sorted(missing)}")

                index_result = await session.call_tool("get_index", {"index_key": "DASH"})
                if index_result.is_error:
                    raise RuntimeError("get_index returned an MCP error")
                detail = index_result.structured_content or {}
                if detail.get("score_scale") != "8-40":
                    raise RuntimeError(f"packaged index metadata is stale: {detail.get('score_scale')!r}")

                food_result = await session.call_tool(
                    "search_fii_foods",
                    {"query": "apple", "limit": 3},
                )
                if food_result.is_error:
                    raise RuntimeError("search_fii_foods returned an MCP error")

                preview_result = await session.call_tool(
                    "preview_dataset",
                    {"file_path": str(allowed_file), "rows": 1},
                )
                if preview_result.is_error:
                    raise RuntimeError("preview_dataset rejected a file inside the configured root")

                blocked_result = await session.call_tool(
                    "preview_dataset",
                    {"file_path": str(blocked_file), "rows": 1},
                )
                if not blocked_result.is_error:
                    raise RuntimeError("preview_dataset accepted a file outside the configured root")

    print(f"DietaryIndex MCP smoke test passed ({len(names)} tools).")


if __name__ == "__main__":
    asyncio.run(run())
