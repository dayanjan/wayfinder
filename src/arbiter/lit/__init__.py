"""Multi-source literature retrieval for the PyZoBot Arbiter (fresh, new-work-only).

Direct API clients (no MCP; per user doctrine): Europe PMC, OpenAlex, Semantic Scholar,
keyed off the project `.env` where a key helps. Returns normalized paper records with
abstracts so downstream agents synthesize from real retrieved text, not memory. MIT.
"""
