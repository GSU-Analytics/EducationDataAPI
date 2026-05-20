from __future__ import annotations
from educationdata._result import EducationDataResult


def fetch_all_pages(session, url: str) -> EducationDataResult:
    all_results: list[dict] = []
    count = 0
    while url:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        if not count:
            count = data.get("count", 0)
        all_results.extend(data.get("results", []))
        url = data.get("next")
    return EducationDataResult(count=count, results=all_results)
