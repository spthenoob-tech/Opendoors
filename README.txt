OPENDOORS — LIVE SEARCH PROTOTYPE

This version does NOT preload opportunity cards. The results area stays hidden until the user submits the profile. Every submission makes a fresh search request to Tavily and returns links/snippets from current indexed web pages.

IMPORTANT: a standalone HTML file cannot reliably search the live web by itself. This package includes a small backend. To run it:

1. Install Python 3.10+.
2. Open a terminal in this folder and run:
   pip install -r requirements.txt
3. Get a Tavily Search API key from https://tavily.com/ .
4. Set the key as an environment variable:
   Windows PowerShell:  $env:TAVILY_API_KEY="your_key_here"
   macOS/Linux:         export TAVILY_API_KEY="your_key_here"
5. Run:
   python server.py
6. Open http://127.0.0.1:8000

Do not put the API key in index.html or publish it in frontend JavaScript.

MATCHING / ACCURACY NOTES
- The profile is submitted only after clicking Find opportunities.
- No opportunity is described as a confirmed match. Search results are labelled Potential relevance because the search provider returns snippets, not authoritative eligibility decisions.
- Explicit female-only phrases are filtered for male profiles, but this is not a complete eligibility engine. Always inspect the official source.
- For a production-grade platform, add a structured opportunity database, official-source crawling, deadline expiry checks, and rule-based eligibility parsing with human verification. Search engines can return stale or incomplete results.
