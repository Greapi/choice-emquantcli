from __future__ import annotations

from typing import Any


def normalize_emquant_data(emq_data: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    codes = list(getattr(emq_data, "Codes", []) or [])
    indicators = list(getattr(emq_data, "Indicators", []) or [])
    dates = list(getattr(emq_data, "Dates", []) or [])
    payload = getattr(emq_data, "Data", None)

    if isinstance(payload, dict):
        for code, values in payload.items():
            if isinstance(values, list) and values and isinstance(values[0], list):
                for i, indicator in enumerate(indicators):
                    per_date = values[i] if i < len(values) else []
                    for j, date in enumerate(dates):
                        rows.append(
                            {
                                "code": code,
                                "indicator": indicator,
                                "date": date,
                                "value": per_date[j] if j < len(per_date) else None,
                            }
                        )
            elif isinstance(values, list):
                for i, indicator in enumerate(indicators):
                    rows.append(
                        {
                            "code": code,
                            "indicator": indicator,
                            "date": dates[0] if dates else None,
                            "value": values[i] if i < len(values) else None,
                        }
                    )
            else:
                rows.append(
                    {
                        "code": code,
                        "indicator": indicators[0] if indicators else None,
                        "date": dates[0] if dates else None,
                        "value": values,
                    }
                )
    elif isinstance(payload, list):
        for idx, value in enumerate(payload):
            rows.append(
                {
                    "code": codes[0] if codes else None,
                    "indicator": indicators[idx] if idx < len(indicators) else None,
                    "date": dates[idx] if idx < len(dates) else None,
                    "value": value,
                }
            )
    elif payload is not None:
        rows.append(
            {
                "code": codes[0] if codes else None,
                "indicator": indicators[0] if indicators else None,
                "date": dates[0] if dates else None,
                "value": payload,
            }
        )

    meta = {
        "codes": codes,
        "indicators": indicators,
        "dates": dates,
        "row_count": len(rows),
    }
    return rows, meta
