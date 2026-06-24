#!/usr/bin/env python3
"""
TakeMeter Confusion Matrix Formatter
Reads results/evaluation_results.json and outputs a formatted Markdown table
for copy-pasting directly into README.md.
"""

import os
import json

def format_matrix():
    results_path = os.path.join("results", "evaluation_results.json")
    
    # Check if the results file exists
    if not os.path.exists(results_path):
        print(f"INFO: File not found at: {results_path}")
        print("--- Instructions ---")
        print("If this script cannot detect the matrix, copy the confusion matrix from Colab and paste it into README manually.")
        return

    # Attempt to load JSON
    try:
        with open(results_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to parse {results_path} as JSON. Details: {e}")
        print("--- Instructions ---")
        print("If this script cannot detect the matrix, copy the confusion matrix from Colab and paste it into README manually.")
        return

    # Look for confusion matrix key (case-insensitive and partial matches)
    matrix = None
    possible_keys = ["confusion_matrix", "confusion", "matrix", "confusionMatrix"]
    
    for key in data.keys():
        if any(pk in key.lower() for pk in possible_keys):
            matrix = data[key]
            break

    # Also check nested structures or print keys if not found
    if matrix is None:
        print("ERROR: Could not find a confusion matrix field in the JSON structure.")
        print(f"Available keys in JSON: {list(data.keys())}")
        print("--- Instructions ---")
        print("If this script cannot detect the matrix, copy the confusion matrix from Colab and paste it into README manually.")
        return

    # Ensure matrix is list of lists
    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        print("ERROR: Confusion matrix is not in the expected format (list of lists).")
        print(f"Found format: {matrix}")
        print("--- Instructions ---")
        print("If this script cannot detect the matrix, copy the confusion matrix from Colab and paste it into README manually.")
        return

    # Validate shape (expecting 3x3)
    if len(matrix) != 3 or not all(len(row) == 3 for row in matrix):
        print(f"WARNING: The matrix shape is {len(matrix)}x{[len(r) for r in matrix]}. Standard TakeMeter is 3x3.")

    # Class ordering
    classes = ["analysis", "hot_take", "reaction"]

    print("=== Formatted Confusion Matrix Table ===")
    print("Copy the markdown table below and paste it into your README.md:\n")
    
    # Print Markdown table header
    header = "| True Label | Predicted analysis | Predicted hot_take | Predicted reaction |"
    divider = "| :--- | :---: | :---: | :---: |"
    print(header)
    print(divider)
    
    # Print table rows
    for i, row_label in enumerate(classes):
        if i < len(matrix):
            cells = [str(val) for val in matrix[i]]
            # Fill up to 3 if shorter
            while len(cells) < 3:
                cells.append("?")
            row_str = f"| **{row_label}** | {cells[0]} | {cells[1]} | {cells[2]} |"
            print(row_str)
        else:
            print(f"| **{row_label}** | ? | ? | ? |")
            
    print("\n=========================================")

if __name__ == "__main__":
    format_matrix()
