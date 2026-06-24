#!/usr/bin/env python3
"""
TakeMeter Label Profiler / Analyzer
Prints label counts, text length statistics, and lists sample comments for inspection.
"""

import sys
import os
import pandas as pd

def analyze_labels(csv_path):
    print(f"=== Starting Label Analysis for: {csv_path} ===")

    # 1. Check if file exists
    if not os.path.exists(csv_path):
        print(f"ERROR: File not found at {csv_path}")
        sys.exit(1)

    # 2. Load dataset
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"ERROR: Failed to read CSV. Details: {e}")
        sys.exit(1)

    if 'text' not in df.columns or 'label' not in df.columns:
        print("ERROR: CSV must contain 'text' and 'label' columns.")
        sys.exit(1)

    # Clean NaNs for analysis
    df = df.dropna(subset=['text', 'label'])
    total_rows = len(df)
    print(f"Total valid rows loaded: {total_rows}\n")

    # 3. Label distribution
    label_counts = df['label'].value_counts()
    print("--- Label Distribution ---")
    for label, count in label_counts.items():
        pct = (count / total_rows) * 100
        print(f"  {label:<12}: {count:>3} rows ({pct:.2f}%)")
    print()

    # 4. Text length metrics (character and word count)
    df['char_len'] = df['text'].apply(len)
    df['word_len'] = df['text'].apply(lambda x: len(x.split()))

    print("--- Text Length Statistics (Character Count) ---")
    char_stats = df.groupby('label')['char_len'].agg(['mean', 'min', 'max', 'std'])
    print(char_stats.to_string())
    print()

    print("--- Text Length Statistics (Word Count) ---")
    word_stats = df.groupby('label')['word_len'].agg(['mean', 'min', 'max', 'std'])
    print(word_stats.to_string())
    print()

    # 5. Show 3 sample comments per label
    print("--- Sample Examples Per Label ---")
    for label in sorted(df['label'].unique()):
        print(f"\nLabel: {label.upper()}")
        print("-" * 40)
        label_df = df[df['label'] == label]
        samples = label_df.sample(min(3, len(label_df)), random_state=42)
        
        for idx, row in enumerate(samples.itertuples(), 1):
            text_cleaned = row.text.replace("\n", " ")
            # Truncate output if very long for clean display
            if len(text_cleaned) > 150:
                text_cleaned = text_cleaned[:147] + "..."
            print(f"  {idx}. \"{text_cleaned}\"")
            if hasattr(row, 'notes') and pd.notna(row.notes):
                print(f"     (Notes: {row.notes})")

    print("\n==================================")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_labels.py <path_to_csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    analyze_labels(csv_path)
