# TakeMeter Google Colab Instructions

Follow these step-by-step instructions to fine-tune your model and evaluate the baseline on Google Colab using the CodePath TakeMeter starter notebook.

## Setup Instructions

1. **Open Notebook**: Open the CodePath TakeMeter starter Colab notebook.
2. **Save Copy**: Click **File → Save a copy in Drive** to save your personal working copy.
3. **Hardware Acceleration**: Go to **Runtime → Change runtime type**, select **T4 GPU** under hardware accelerators, and click Save.
4. **Upload Dataset**: In the left sidebar, click the Files icon and upload your `data/takemeter_dataset.csv` file.
5. **Configure API Key**: 
   - Get a free API key from [Groq Console](https://console.groq.com/).
   - In Colab, click the key icon (Secrets) in the left sidebar.
   - Add a new secret with the name `GROQ_API_KEY` and paste your key.
   - Toggle the switch to grant notebook access to this key.

## Coding and Configuration

Make sure your notebook defines the correct label-to-ID mapping before training:

```python
label2id = {
    "analysis": 0,
    "hot_take": 1,
    "reaction": 2
}
id2label = {v: k for k, v in label2id.items()}
```

## Running the Experiment

1. **Section 1 (Load Dataset)**: Run the cells to import packages, verify the GPU, load `takemeter_dataset.csv`, and check the label counts.
2. **Section 2 (Split & Tokenize)**: Split the dataset (70% train, 15% val, 15% test) and tokenize using `distilbert-base-uncased`.
3. **Section 5 (Groq Zero-Shot Baseline)**:
   - Run the Groq zero-shot evaluation on the test set.
   - The prompt used for Groq Llama-3.3-70b-versatile is:

```text
You are classifying comments from soccer and World Cup discussion communities.

Choose exactly one label:
analysis
hot_take
reaction

Definitions:
analysis = The comment explains soccer using tactics, statistics, player roles, match context, tournament math, or specific evidence.
hot_take = The comment makes a strong opinion, prediction, or judgment without enough supporting evidence.
reaction = The comment is mostly emotion, humor, hype, anger, sarcasm, or a short immediate response.

Decision rules:
- If the comment gives tactical reasoning, stats, tournament math, player-role explanation, or specific match evidence, choose analysis.
- If the comment makes a bold claim but does not explain much, choose hot_take.
- If the comment is mostly emotional, funny, sarcastic, or very short, choose reaction.

Return only the label name. Do not explain.

Comment:
{text}
```

4. **Section 3 (Fine-tune DistilBERT)**: Fine-tune `distilbert-base-uncased` with the following hyperparameters:
   - epochs: 3
   - learning rate: 2e-5
   - batch size: 16
5. **Section 4 (Evaluate Fine-Tuned Model)**: Generate the evaluation metrics (Accuracy, Precision, Recall, F1) on the test set and print the confusion matrix.
6. **Section 6 (Export Results)**: Run the export code to download:
   - `evaluation_results.json`
   - `confusion_matrix.png`
   - The fully trained model weights folder (if downloading to run the local Streamlit app).

## Post-Training Steps

1. **Download Outputs**: Download `evaluation_results.json` and `confusion_matrix.png` from the Colab Files tab.
2. **Save to Repository**: Place them in:
   - `results/evaluation_results.json`
   - `results/confusion_matrix.png`
3. **Update README.md**: Open `README.md` and replace all `TODO` placeholders under the "Evaluation Results", "Confusion Matrix", "Wrong Prediction Analysis", and "Sample Classifications" sections with your real metrics and observations.
4. **Export Model for Streamlit**: Zip and download the trained model directory, unpack it, and place it at `app/model/` to run predictions locally in the Streamlit app.
5. **Security Reminder**: Ensure `GROQ_API_KEY` is **never** committed or written to any file in your public repository.
