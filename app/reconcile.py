from Levenshtein import ratio

def reconcile_ledgers(df1, df2):
    matches = []
    unmatched_internal = []
    unmatched_bank = []

    used_bank_rows = set()

    for i, row1 in df1.iterrows():
        best_match = None
        best_score = 0

        for j, row2 in df2.iterrows():

            if j in used_bank_rows:
                continue

            amount_match = row1['amount'] == row2['amount']

            desc_score = ratio(
                str(row1['description']).lower(),
                str(row2['description']).lower()
            )

            total_score = (
                (0.7 if amount_match else 0)
                + (0.3 * desc_score)
            )

            if total_score > best_score:
                best_score = total_score
                best_match = j

        if best_match is not None and best_score >= 0.75:
            used_bank_rows.add(best_match)

            matches.append({
                'internal_description': row1['description'],
                'bank_description': df2.loc[best_match]['description'],
                'amount': row1['amount'],
                'confidence_score': round(best_score, 2)
            })

        else:
            unmatched_internal.append(row1.to_dict())

    for j, row2 in df2.iterrows():
        if j not in used_bank_rows:
            unmatched_bank.append(row2.to_dict())

    return {
        'matched_transactions': matches,
        'unmatched_internal': unmatched_internal,
        'unmatched_bank': unmatched_bank,
        'match_rate': round(
            len(matches) / max(len(df1), 1),
            2
        )
    }
