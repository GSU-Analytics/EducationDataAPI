from __future__ import annotations
from dataclasses import dataclass


@dataclass
class EducationDataResult:
    count: int
    results: list[dict]

    def to_dict(self) -> list[dict]:
        return self.results

    def to_df(self):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for .to_df(). Install it with: pip install urban-education-data[df]"
            )
        df = pd.DataFrame(self.results)
        df.attrs["count"] = self.count
        return df
