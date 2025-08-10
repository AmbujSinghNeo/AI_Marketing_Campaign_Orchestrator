# config.py (updated)
# --- CRITICAL: SQLite fix MUST be first ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
    print("✅ SQLite fix applied successfully.")
except ImportError:
    print("⚠️ pysqlite3 not found, skipping fix.")
# --- END SQLite FIX ---

import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
import sys
import time
import json
import hashlib
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from langchain_groq import ChatGroq

# --- Helpers ---
def ensure_dir(path):
    """Ensure that a directory exists. Create if it does not exist."""
    os.makedirs(path, exist_ok=True)

def sha1(text: str) -> str:
    """Return the SHA-1 hash of a given string."""
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

# --- Tools with caching and compression ---
class SummarizedSearchTool(BaseTool):
    """Search the internet and return top 3 concise results with title, URL, and snippet."""
    name: str = "Summarized Internet Search"
    description: str = "Search the web and return 3 concise results: title – url – 1-line snippet."

    def _run(self, search_query: str) -> str:
        # Use caching to avoid repeating the same search query
        ensure_dir("cache")
        key = f"cache/serper_{sha1(search_query)}.json"
        if os.path.exists(key):
            try:
                with open(key, "r", encoding="utf-8") as f:
                    return f.read()
            except:
                pass

        # Perform the search using SerperDevTool
        serper = SerperDevTool()
        try:
            raw = serper.run(search_query=search_query)
        except Exception as e:
            # Retry once if the search fails
            time.sleep(60)
            try:
                raw = serper.run(search_query=search_query)
            except Exception as e2:
                return f"Search failed: {e2}"

        # Extract top 3 results
        try:
            if isinstance(raw, dict):
                results = raw.get("organic", []) or raw.get("results", []) or []
            else:
                results = json.loads(raw).get("organic", []) if raw.strip().startswith("{") else []
        except Exception:
            results = []

        # Format output as list of lines
        lines = []
        for it in results[:3]:
            title = it.get("title") or ""
            link = it.get("link") or it.get("url") or ""
            snippet = (it.get("snippet") or it.get("description") or "")[:160]
            if title or link:
                lines.append(f"{title.strip()} – {link.strip()} – {snippet.strip()}")

        # Fallback if no formatted results found
        if not lines:
            text = str(raw)
            if len(text) > 1000:
                text = text[:1000]
            out = text
        else:
            out = "Top results:\n- " + "\n- ".join(lines)

        # Cache the results
        try:
            with open(key, "w", encoding="utf-8") as f:
                f.write(out)
        except:
            pass
        return out

class SummarizedScrapingTool(BaseTool):
    """Scrape a webpage and return a compact summary of top headings and key points."""
    name: str = "Intelligent Website Scraper"
    description: str = "Scrape a URL and return compact summary: top headings and 5 key points."

    def _run(self, website_url: str) -> str:
        # Use caching to avoid re-scraping same page
        ensure_dir("cache")
        key = f"cache/scrape_{sha1(website_url)}.txt"
        if os.path.exists(key):
            try:
                with open(key, "r", encoding="utf-8") as f:
                    return f.read()
            except:
                pass

        try:
            # Fetch the webpage with a standard User-Agent
            resp = requests.get(website_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=12)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'html.parser')

            # Extract headings
            headings = []
            for tag in soup.find_all(['h1', 'h2', 'h3'])[:5]:
                t = tag.get_text(strip=True)
                if t:
                    headings.append(t)

            # Extract up to 5 meaningful paragraphs
            paras = []
            for p in soup.find_all('p'):
                t = p.get_text(strip=True)
                if len(t) > 60:
                    paras.append(t)
                if len(paras) >= 8:
                    break

            headings = headings[:3]
            paras = paras[:5]

            # Build a clean summary
            summary = []
            if headings:
                summary.append("Headings:")
                summary.extend([f"- {h}" for h in headings])
            if paras:
                summary.append("\nKey Points:")
                summary.extend([f"- {p[:220]}" for p in paras])

            out = "\n".join(summary) if summary else "No meaningful content found."
            if len(out) > 1500:
                out = out[:1500]

            # Cache the scraped content
            with open(key, "w", encoding="utf-8") as f:
                f.write(out)
            return out
        except Exception as e:
            return f"Failed to scrape: {e}"
