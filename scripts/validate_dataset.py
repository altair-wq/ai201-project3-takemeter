#!/usr/bin/env python3
"""
TakeMeter Dataset Validator
Checks that the dataset file matches all structural and distribution requirements
for the CodePath TakeMeter assignment.
"""

import sys
import os
import pandas as pd

def validate_csv(csv_path):
    print(f"=== Starting Validation for: {csv_path} ===")

    # 1. Check if the file exists
    if not os.path.exists(csv_path):
        print(f"ERROR: Dataset file not found at {csv_path}")
        print("Please place your takemeter_dataset.csv file in the data/ folder.")
        sys.exit(1)

    # 2. Try loading the CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"ERROR: Failed to read CSV file. Details: {e}")
        sys.exit(1)

    errors_found = False

    # 3. Check required columns
    required_cols = {'text', 'label'}
    allowed_cols = {'text', 'label', 'notes', 'source', 'review_status'}
    current_cols = set(df.columns)

    missing_cols = required_cols - current_cols
    if missing_cols:
        print(f"ERROR: Missing required columns: {missing_cols}")
        errors_found = True

    extra_cols = current_cols - allowed_cols
    if extra_cols:
        print(f"WARNING: Found unexpected columns (ignored): {extra_cols}")

    # If critical columns are missing, we cannot proceed with other validation
    if errors_found:
        print("Validation FAILED due to missing columns. Exiting.")
        sys.exit(1)

    # 4. Check row count
    row_count = len(df)
    print(f"Total row count: {row_count}")
    if row_count < 200:
        print(f"ERROR: Dataset must have at least 200 rows. Found: {row_count}")
        errors_found = True

    # 5. Check for null/empty values
    null_text_count = df['text'].isna().sum()
    if null_text_count > 0:
        print(f"ERROR: Found {null_text_count} empty values in 'text' column.")
        errors_found = True

    null_label_count = df['label'].isna().sum()
    if null_label_count > 0:
        print(f"ERROR: Found {null_label_count} empty values in 'label' column.")
        errors_found = True

    # Check for empty strings after trimming whitespace
    if 'text' in df.columns:
        empty_text_strings = (df['text'].astype(str).str.strip() == '').sum()
        if empty_text_strings > 0:
            print(f"ERROR: Found {empty_text_strings} blank/whitespace-only rows in 'text'.")
            errors_found = True

    # 6. Check label values
    allowed_labels = {'analysis', 'hot_take', 'reaction'}
    unique_labels = set(df['label'].dropna().unique())
    invalid_labels = unique_labels - allowed_labels
    if invalid_labels:
        print(f"ERROR: Found invalid labels: {invalid_labels}")
        print(f"Allowed labels are exactly: {allowed_labels}")
        errors_found = True

    # 7. Check label distribution and imbalance warnings
    label_counts = df['label'].value_counts()
    print("\n--- Label Distribution ---")
    for label in allowed_labels:
        count = label_counts.get(label, 0)
        percentage = (count / row_count) * 100 if row_count > 0 else 0
        print(f"  {label}: {count} rows ({percentage:.2f}%)")

        # Warnings for extreme imbalance
        if percentage > 70.0:
            print(f"  [WARNING]: '{label}' dominates the dataset with {percentage:.2f}% (above 70%).")
        elif percentage < 20.0:
            print(f"  [WARNING]: '{label}' is underrepresented at {percentage:.2f}% (below 20%).")

    # 8. Check for duplicates in text
    duplicate_count = df['text'].duplicated().sum()
    if duplicate_count > 0:
        print(f"\nWARNING: Found {duplicate_count} duplicate text entries. Consider cleaning if appropriate.")

    # 9. Final Decision
    print("\n==================================")
    if errors_found:
        print("Validation FAILED. Please correct the errors listed above.")
        sys.exit(1)
    else:
        print("Validation SUCCESSFUL! The dataset is structurally sound and ready for training.")
        sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_dataset.py <path_to_csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    validate_csv(csv_path)
