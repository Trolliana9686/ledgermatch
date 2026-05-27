from datetime import datetime
from Levenshtein import ratio


def parse_date(value):
    return datetime.strptime(str(value), "%Y-%m-%d").date()


def amount_within_tolerance(amount1, amount2, tolerance=0.01):
    return abs(float(amount1) - float(amount2)) <= tolerance


def date_within_tolerance(date1, date2, tolerance_days=1):
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    return abs((d1 - d2).days) <= tolerance_days


def classify_match(row1, row2, amount_match, date_match, desc_score):
    if amount_match and date_match and desc_score >= 0.90:
        return "strong_match"

    if amount_match and date_match:
        return "probable_match"

    if amount_match and not date_match:
        return "date_mismatch"

    if date_match and not amount_match:
        return "amount_mismatch"

    return "weak_match"


def reconcile_ledgers(df1, df2, amount_tolerance=0.01, date_tolerance_days=1):
    matches = []
    unmatched_internal = []
    unmatched_bank = []

    used_bank_rows = set()

    for i, row1 in df1.iterrows():
        best_match = None
        best_score = 0
        best_classification = None

        for j, row2 in df2.iterrows():
            if j in used_bank_rows:
                continue

            amount_match = amount_within_tolerance(
                row1["amount"],
                row2["amount"],
                amount_tolerance
            )

            date_match = date_within_tolerance(
                row1["date"],
                row2["date"],
                date_tolerance_days
            )

            desc_score = ratio(
                str(row1["description"]).lower(),
                str(row2["description"]).lower()
            )

            total_score = (
                (0.45 if amount_match else 0)
                + (0.35 if date_match else 0)
                + (0.20 * desc_score)
            )

            classification = classify_match(
                row1,
                row2,
                amount_match,
                date_match,
                desc_score
            )

            if total_score > best_score:
                best_score = total_score
                best_match = j
                best_classification = classification

        if best_match is not None and best_score >= 0.70:
            used_bank_rows.add(best_match)

            matches.append({
                "internal_description": row1["description"],
                "bank_description": df2.loc[best_match]["description"],
                "internal_date": row1["date"],
                "bank_date": df2.loc[best_match]["date"],
                "internal_amount": float(row1["amount"]),
                "bank_amount": float(df2.loc[best_match]["amount"]),
                "confidence_score": round(best_score, 2),
                "match_type": best_classification
            })
        else:
            unmatched_internal.append(row1.to_dict())

    for j, row2 in df2.iterrows():
        if j not in used_bank_rows:
            unmatched_bank.append(row2.to_dict())

    return {
        "summary": {
            "internal_transaction_count": len(df1),
            "bank_transaction_count": len(df2),
            "matched_count": len(matches),
            "unmatched_internal_count": len(unmatched_internal),
            "unmatched_bank_count": len(unmatched_bank),
            "match_rate": round(len(matches) / max(len(df1), 1), 2)
        },
        "matched_transactions": matches,
        "unmatched_internal": unmatched_internal,
        "unmatched_bank": unmatched_bank
    }