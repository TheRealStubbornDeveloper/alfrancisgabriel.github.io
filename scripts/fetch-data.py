#!/usr/bin/env python3
"""Fetch GitHub repo analytics data and write static JSON files."""
import json
import os
import subprocess
import sys
from datetime import datetime

import requests

USERNAME = "TheRealStubbornDeveloper"
GITHUB_API = "https://api.github.com"
OUTPUT_DIR = os.environ.get(
    "ANALYTICS_OUTPUT_DIR",
    os.path.join(os.path.dirname(__file__), "..", "analytics", "data")
)

def gh_headers():
    """Get GitHub token from env or gh CLI."""
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        try:
            r = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0:
                token = r.stdout.strip()
        except FileNotFoundError:
            pass
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers

def gh_get(path, params=None):
    url = f"{GITHUB_API}{path}"
    r = requests.get(url, headers=gh_headers(), params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def gh_get_all(path, params=None):
    if params is None:
        params = {}
    params["per_page"] = 100
    page = 1
    results = []
    while True:
        params["page"] = page
        r = requests.get(f"{GITHUB_API}{path}", headers=gh_headers(), params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        results.extend(data)
        page += 1
    return results

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Fetching repos for {USERNAME}...")
    repos = gh_get_all(f"/users/{USERNAME}/repos", {"sort": "updated"})
    repos = [r for r in repos if not r["fork"]]

    # Build repos list
    repo_list = []
    for r in repos:
        repo_list.append({
            "name": r["name"],
            "description": r["description"],
            "stars": r["stargazers_count"],
            "forks": r["forks_count"],
            "language": r["language"],
            "open_issues": r["open_issues_count"],
            "size": r["size"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "url": r["html_url"],
            "homepage": r["homepage"],
        })
    # Sort by stars desc, then name
    repo_list.sort(key=lambda x: (-x["stars"], x["name"]))

    # Summary
    total_stars = sum(r["stars"] for r in repo_list)
    total_forks = sum(r["forks"] for r in repo_list)
    total_size = sum(r["size"] for r in repo_list)
    lang_counts = {}
    for r in repo_list:
        if r["language"]:
            lang_counts[r["language"]] = lang_counts.get(r["language"], 0) + 1
    top_lang = max(lang_counts, key=lang_counts.get) if lang_counts else None
    most_starred = max(repo_list, key=lambda x: x["stars"]) if repo_list else None

    summary = {
        "total_repos": len(repo_list),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "total_size_mb": round(total_size / 1024, 1),
        "languages_used": len(lang_counts),
        "top_language": top_lang,
        "most_starred": most_starred["name"] if most_starred else None,
        "most_starred_count": most_starred["stars"] if most_starred else 0,
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }

    # Language overview (fetch per-repo langs)
    print("Fetching language breakdowns...")
    all_langs = {}
    for repo in repos:
        try:
            langs = gh_get(f"/repos/{USERNAME}/{repo['name']}/languages")
            for lang, bytes_ in langs.items():
                all_langs[lang] = all_langs.get(lang, 0) + bytes_
        except Exception as e:
            print(f"  Skipping langs for {repo['name']}: {e}")

    total = sum(all_langs.values())
    lang_overview = [
        {"name": lang, "bytes": bytes_, "pct": round(bytes_ / total * 100, 1)}
        for lang, bytes_ in sorted(all_langs.items(), key=lambda x: -x[1])
    ]

    # Write files
    print(f"Writing to {OUTPUT_DIR}/")
    with open(os.path.join(OUTPUT_DIR, "repos.json"), "w") as f:
        json.dump(repo_list, f, indent=2)
    with open(os.path.join(OUTPUT_DIR, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    with open(os.path.join(OUTPUT_DIR, "languages.json"), "w") as f:
        json.dump(lang_overview, f, indent=2)

    print(f"Done. {len(repo_list)} repos → {len(lang_overview)} languages")
    print(f"Total stars: {total_stars} | Top lang: {top_lang}")

if __name__ == "__main__":
    main()
