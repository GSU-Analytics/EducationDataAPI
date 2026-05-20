"""Unit tests for _result.py and _pagination.py (no network calls)."""
import pytest
from unittest.mock import MagicMock, patch
from educationdata._result import EducationDataResult
from educationdata._pagination import fetch_all_pages


# ---------------------------------------------------------------------------
# EducationDataResult
# ---------------------------------------------------------------------------

class TestEducationDataResult:
    def test_to_dict_returns_results(self):
        rows = [{"a": 1}, {"a": 2}]
        r = EducationDataResult(count=2, results=rows)
        assert r.to_dict() == rows

    def test_count_attribute(self):
        r = EducationDataResult(count=42, results=[])
        assert r.count == 42

    def test_to_df_returns_dataframe(self):
        pd = pytest.importorskip("pandas")
        rows = [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
        r = EducationDataResult(count=2, results=rows)
        df = r.to_df()
        assert list(df.columns) == ["x", "y"]
        assert len(df) == 2
        assert df.attrs["count"] == 2

    def test_to_df_missing_pandas_raises(self):
        r = EducationDataResult(count=0, results=[])
        with patch.dict("sys.modules", {"pandas": None}):
            with pytest.raises(ImportError, match="pandas"):
                r.to_df()

    def test_to_dict_identity(self):
        rows = [{"k": "v"}]
        r = EducationDataResult(count=1, results=rows)
        assert r.to_dict() is rows


# ---------------------------------------------------------------------------
# fetch_all_pages
# ---------------------------------------------------------------------------

def _make_response(data: dict) -> MagicMock:
    resp = MagicMock()
    resp.json.return_value = data
    resp.raise_for_status.return_value = None
    return resp


class TestFetchAllPages:
    def test_single_page(self):
        session = MagicMock()
        session.get.return_value = _make_response(
            {"count": 2, "next": None, "results": [{"id": 1}, {"id": 2}]}
        )
        result = fetch_all_pages(session, "http://example.com/api/")
        assert result.count == 2
        assert result.to_dict() == [{"id": 1}, {"id": 2}]
        session.get.assert_called_once_with("http://example.com/api/")

    def test_multiple_pages(self):
        session = MagicMock()
        session.get.side_effect = [
            _make_response(
                {"count": 3, "next": "http://example.com/api/?page=2", "results": [{"id": 1}]}
            ),
            _make_response(
                {"count": 3, "next": "http://example.com/api/?page=3", "results": [{"id": 2}]}
            ),
            _make_response(
                {"count": 3, "next": None, "results": [{"id": 3}]}
            ),
        ]
        result = fetch_all_pages(session, "http://example.com/api/")
        assert result.count == 3
        assert result.to_dict() == [{"id": 1}, {"id": 2}, {"id": 3}]
        assert session.get.call_count == 3

    def test_count_taken_from_first_page(self):
        session = MagicMock()
        session.get.side_effect = [
            _make_response({"count": 10, "next": "http://example.com/p2", "results": [{"id": 1}]}),
            _make_response({"count": 999, "next": None, "results": [{"id": 2}]}),
        ]
        result = fetch_all_pages(session, "http://example.com/p1")
        assert result.count == 10

    def test_empty_results(self):
        session = MagicMock()
        session.get.return_value = _make_response(
            {"count": 0, "next": None, "results": []}
        )
        result = fetch_all_pages(session, "http://example.com/api/")
        assert result.count == 0
        assert result.to_dict() == []

    def test_http_error_propagates(self):
        session = MagicMock()
        resp = MagicMock()
        resp.raise_for_status.side_effect = Exception("404 Not Found")
        session.get.return_value = resp
        with pytest.raises(Exception, match="404 Not Found"):
            fetch_all_pages(session, "http://example.com/api/")
