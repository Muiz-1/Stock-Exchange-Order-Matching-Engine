"""
compareResults.py
-----------------
Compares old vs new evaluation CSVs and shows accuracy changes per file.

Usage:
    python compareResults.py <old_csv> <new_csv>

Example:
    python compareResults.py VaryingForm/results_old.csv VaryingForm/evaluation_LTL4_seperately.csv
"""

import csv
import sys
import os

if len(sys.argv) < 3:
    print("Usage: python compareResults.py <old_csv> <new_csv>")
    sys.exit(1)

old_path = sys.argv[1]
new_path = sys.argv[2]

def load_best_acc(csv_path):
    best = {}
    with open(csv_path, newline='') as f:
        for row in csv.DictReader(f):
            fname = row['file']
            acc   = float(row['qpai_accuracy'])
            if fname not in best or acc > best[fname]:
                best[fname] = acc
    return best

old = load_best_acc(old_path)
new = load_best_acc(new_path)

all_files = sorted(set(old) | set(new))

improved  = 0
worsened  = 0
same      = 0
new_perfect = 0

print(f"\n{'='*70}")
print(f"  {'File':<35}  {'Old':>6}  {'New':>6}  {'Change':>8}")
print(f"{'='*70}")

for fname in all_files:
    old_acc = old.get(fname, None)
    new_acc = new.get(fname, None)

    if old_acc is None:
        print(f"  {fname:<35}  {'N/A':>6}  {new_acc:>6.4f}  {'NEW':>8}")
        continue
    if new_acc is None:
        print(f"  {fname:<35}  {old_acc:>6.4f}  {'N/A':>6}  {'MISSING':>8}")
        continue

    diff = new_acc - old_acc
    if diff > 0.001:
        tag = f'+{diff:.4f} ↑'
        improved += 1
        if new_acc == 1.0:
            new_perfect += 1
    elif diff < -0.001:
        tag = f'{diff:.4f} ↓'
        worsened += 1
    else:
        tag = '—'
        same += 1

    print(f"  {fname:<35}  {old_acc:>6.4f}  {new_acc:>6.4f}  {tag:>8}")

print(f"{'='*70}")
print(f"\n  Improved : {improved} files")
print(f"  Worsened : {worsened} files")
print(f"  Same     : {same} files")
print(f"  Newly perfect (1.0): {new_perfect} files")

old_avg = sum(old.values()) / len(old) if old else 0
new_avg = sum(new.values()) / len(new) if new else 0
print(f"\n  Avg accuracy OLD : {old_avg:.4f}")
print(f"  Avg accuracy NEW : {new_avg:.4f}")
print(f"  Overall change   : {new_avg - old_avg:+.4f}")
print()
