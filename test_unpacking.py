import polars as pl
import competitions.aimo.bundled_submission as sub

# Simulate predict(row_df, id_df)
row = pl.DataFrame({'id': ['id123'], 'problem': ['p456']})
id_df = row.select('id')

print("Testing predict(row, id_df)...")
res = sub.predict(row, id_df)
print(f"Result:\n{res}")

# Simulate predict(id_series, prob_series)
id_s = pl.Series('id', ['s1'])
prob_s = pl.Series('problem', ['s2'])
print("\nTesting predict(id_series, prob_series)...")
res = sub.predict(id_s, prob_s)
print(f"Result:\n{res}")
