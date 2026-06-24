# TakeMeter: Soccer Discourse Classifier

## Overview
TakeMeter is a machine learning text classifier designed to categorize soccer-related comments from public discussion threads into three distinct categories: `analysis`, `hot_take`, or `reaction`. The objective of this project is to build a classifier that identifies the quality and nature of soccer discourse rather than making simple subjective judgments about whether a comment is "good" or "bad."

## Community Choice and Reasoning
* **Community**: Public Reddit discussion boards, specifically **r/soccer** and **r/worldcup**.
* **Reasoning**: Soccer is a global sport that attracts a massive online community. The discourse within these subreddits varies heavily depending on the context:
  - **Match threads** capture live-game emotions, humor, excitement, or despair (mostly **reactions**).
  - **Post-match threads** contain intense, highly debatable declarations, blame assignments, or bold future predictions (mostly **hot takes**).
  - **Tactical/Weekly discussion threads** feature structured assessments of tactical patterns, player attributes, match statistics, or tournament scenarios (mostly **analysis**).
  
  Categorizing comments into these classes helps filter noisy discussion and highlights comments that provide empirical or tactical reasoning.

## Label Taxonomy

| Label | Definition | Examples |
| :--- | :--- | :--- |
| **`analysis`** | A comment explaining gameplay using tactics, statistics, player roles, match context, team structure, tournament math, or specific evidence. | • *"Colombia are the better team right now, but they can’t crack the DR Congo defense."*<br>• *"0.7 xG on 14 shots."* |
| **`hot_take`** | A strong, highly subjective opinion, judgment, or prediction about a team/player/coach without supporting evidence or detailed reasoning. | • *"Croatia are simply not good enough to go far."*<br>• *"United are finished."* |
| **`reaction`** | A comment that contains mostly emotion, humor, hype, anger, sarcasm, or is a brief immediate response. | • *"WHAT A GOAL OMG."*<br>• *"Ref is blind lol."* |

## Dataset
* **Dataset File**: [takemeter_dataset.csv](file:///Users/altairadilkhan/.gemini/antigravity/scratch/ai201-project3-takemeter/data/takemeter_dataset.csv)
* **Source**: Public soccer and World Cup Reddit threads (mainly r/soccer and r/worldcup).
* **Collection Method**: Comments were manually copied from public threads. AI-assisted cleaning was used to strip formatting and noise, and initial label recommendations were suggested by AI. All comments and labels were manually reviewed and verified by the student before training.
* **Total Rows**: 220
* **Label Distribution**:

| Label | Count | Percentage |
| :--- | :---: | :---: |
| **analysis** | 80 | 36.36% |
| **hot_take** | 70 | 31.82% |
| **reaction** | 70 | 31.82% |

## Difficult-to-Label Examples

We identified several complex boundary comments where taxonomy rules had to be strictly applied:

1. **"0.7 xG on 14 shots."**
   - *Possible labels*: `analysis` vs. `reaction`.
   - *Final label*: `analysis`.
   - *Reason*: Despite being brief, it utilizes specific match statistics (Expected Goals, shot volume) to describe the performance.
2. **"Croatia don’t look great but they didn’t look great in 2022 either and still made a deep run."**
   - *Possible labels*: `analysis` vs. `hot_take`.
   - *Final label*: `analysis`.
   - *Reason*: The statement uses historical comparison (their 2022 tournament run) to support its assessment of Croatia's performance rather than asserting a blind opinion.
3. **"This has all the hallmarks of a thrilling nil-nil draw."**
   - *Possible labels*: `reaction` vs. `hot_take`.
   - *Final label*: `reaction`.
   - *Reason*: The comment uses sarcasm to express immediate boredom/frustration with a slow game. It is not an actual prediction of a draw, but an emotional reaction to match play.

## Fine-Tuning Approach
* **Base Model**: `distilbert-base-uncased` (a lightweight, resource-efficient version of BERT).
* **Environment**: Google Colab utilizing a free T4 GPU.
* **Split**: 70% Train (154 comments), 15% Validation (33 comments), 15% Test (33 comments)
* **Hyperparameters**:
  - `epochs`: 3
  - `learning rate`: 2e-5
  - `batch size`: 16
* **Rationale**: DistilBERT is well-suited for a small dataset (~200 comments) because it preserves 95% of BERT's language understanding capability while training very rapidly on a free GPU without overfitting.

## Baseline Comparison
We compare the performance of our fine-tuned DistilBERT model against a zero-shot LLM baseline utilizing **Groq Llama-3.3-70b-versatile**. The baseline evaluates whether a general-purpose large language model can categorize these comments accurately out-of-the-box without custom parameter fine-tuning.

We evaluate the baseline model using the following exact zero-shot prompt:

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

## Evaluation Results

*These results are templates. Please populate them after completing your training notebook.*

### Model Accuracy Comparison

| Model | Accuracy | Notes |
| :--- | :---: | :--- |
| **Groq Zero-Shot Baseline (Llama-3.3)** | 39.39% | Zero-shot performance on 33 test comments |
| **Fine-Tuned DistilBERT Classifier** | 48.48% | Trained for 3 epochs (9.09% improvement) |

### Per-Class Performance Metrics (Groq Zero-Shot Baseline)

| Label | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **analysis** | 0.750 | 0.250 | 0.375 | 12 |
| **hot_take** | 0.000 | 0.000 | 0.000 | 11 |
| **reaction** | 0.370 | 1.000 | 0.541 | 10 |

### Per-Class Performance Metrics (Fine-Tuned DistilBERT Model)

| Label | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **analysis** | 0.414 | 1.000 | 0.585 | 12 |
| **hot_take** | 0.000 | 0.000 | 0.000 | 11 |
| **reaction** | 1.000 | 0.400 | 0.571 | 10 |

## Confusion Matrix

| True Label | Predicted analysis | Predicted hot_take | Predicted reaction |
| :--- | :---: | :---: | :---: |
| **analysis** | 12 | 0 | 0 |
| **hot_take** | 11 | 0 | 0 |
| **reaction** | 6 | 0 | 4 |

### Interpretation
The fine-tuned model improved over the Groq zero-shot baseline by 9.09 percentage points, but performance is still weak overall. The model learned to identify analysis and some reaction comments, but it completely failed to predict hot_take on the test set. The confusion matrix shows that every hot_take example was misclassified as analysis. This suggests the model over-relied on soccer-specific wording and treated opinionated comments as analysis whenever they included match context or football terms.

*Note: The visualized confusion matrix graph is saved at [results/confusion_matrix.png](file:///Users/altairadilkhan/.gemini/antigravity/scratch/ai201-project3-takemeter/results/confusion_matrix.png).*

## Wrong Prediction Analysis

### Wrong Prediction 1
* **Text**: "Colombia had them on the ropes in the first quarter but Congo got their act together after the water break. They looked way more organized and effective"
* **True label**: hot_take
* **Predicted label**: analysis
* **Confidence**: 0.40
* **Why it failed**: The model likely saw football-specific language like “organized,” “water break,” and match-flow description, so it treated the comment as analysis. However, the original label is hot_take because the comment makes a broad judgment about team performance without deeper tactical evidence.
* **What would help**: Adding training examples of hot takes that discuss match events or use team performance descriptors.

### Wrong Prediction 2
* **Text**: "nations league isnt a real tournament, in what world do u take lamine yamal and pedri off in a final that you’re trying to win, its just a tournament that replaced friendlies to make more money"
* **True label**: hot_take
* **Predicted label**: analysis
* **Confidence**: 0.41
* **Why it failed**: The model likely focused on named entities and competition context, such as Nations League, Lamine Yamal, and Pedri. But the comment is mainly an unsupported judgment about the tournament’s legitimacy, so hot_take is more appropriate.
* **What would help**: Adding training examples that express opinions about competitions or player selections without tactical/statistical analysis.

### Wrong Prediction 3
* **Text**: "What is the logic that a call can be changed from a corner to a goal kick but not the other way around?"
* **True label**: hot_take
* **Predicted label**: analysis
* **Confidence**: 0.40
* **Why it failed**: The model likely interpreted this as reasoning because it asks about “logic” and refereeing rules. However, in the dataset it functions more as a frustrated judgment about officiating rather than a detailed rules analysis.
* **What would help**: Adding training examples of questions/complaints about refereeing rules labeled as hot takes or reactions.

## Sample Classifications

| Comment | Predicted Label | Confidence | Why it makes sense |
| :--- | :---: | :---: | :--- |
| "Because the last one was 4 years ago and so many things could have happened by the time you have to defend it. In fact, out of all the defending champions in the 21st century, only Brazil 2006 and France 2022 weren't eliminated in the group stage. Personally I think Argentina will do fine though." | analysis | 0.45 | It contains specific tournament math, historical stats, and detailed context about group stage elimination history. |
| "Colombia had them on the ropes in the first quarter but Congo got their act together after the water break. They looked way more organized and effective" | analysis | 0.40 | It uses technical descriptors like "organized and effective" and discusses match flow context. |
| "nations league isnt a real tournament, in what world do u take lamine yamal and pedri off in a final that you’re trying to win, its just a tournament that replaced friendlies to make more money" | analysis | 0.41 | It references player names, tournament names, and a final match scenario. |
| "What is the logic that a call can be changed from a corner to a goal kick but not the other way around?" | analysis | 0.40 | It references refereeing logic and rule details. |
| "Is it just me but Team England is not getting much mention or love across social compared to other teams? Im in USA." | analysis | 0.40 | It evaluates comparative media coverage across social platforms. |

## Reflection: What the Model Learned vs. What I Intended
* The model learned that longer comments with soccer-specific terms often look like analysis.
* It learned reaction somewhat well when comments were clearly short or emotional.
* It failed to learn hot_take as a separate class.
* The biggest failure pattern was hot_take → analysis.
* This likely happened because many hot takes still include soccer-specific vocabulary, player names, competition names, or match context.
* To improve the model, I would add more hot_take examples, especially examples that contain soccer-specific terms but are still unsupported opinions.

## Spec Reflection
* **Spec Benefit**: Writing down the label taxonomy and mapping out hard edge cases before collecting the final dataset forced rigorous validation. It minimized label ambiguity during dataset creation.
* **Implementation Divergence**: Instead of writing a complex scraper for the Reddit API (which would require developer credentials, rate-limiting handlers, and authentication scripts), public Reddit match threads were manually inspected and copied into CSV format, with AI assistance to strip metadata noise. This allowed faster creation of clean data while remaining aligned with course guidelines.

## AI Usage
* AI was utilized to help clean raw scraped Reddit comment logs, strip noise (ads, usernames, links), and provide initial label suggestions.
* AI was used to format the markdown structure of `planning.md` and `README.md` to ensure all assignment guidelines are present.
* The student reviewed all final label definitions, proofread data rows, executed the notebook, analyzed evaluation outputs, and interpreted the wrong predictions.
* No model results, metrics, or graphs were AI-fabricated.

## How to Run Validation
Run the validation and label analysis scripts locally to confirm formatting and inspect data:
```bash
python scripts/validate_dataset.py data/takemeter_dataset.csv
python scripts/analyze_labels.py data/takemeter_dataset.csv
```

## Colab Training Instructions
To fine-tune the classifier:
1. Refer to [notebooks/TakeMeter_Colab_Instructions.md](file:///Users/altairadilkhan/.gemini/antigravity/scratch/ai201-project3-takemeter/notebooks/TakeMeter_Colab_Instructions.md) for step-by-step setup details.
2. Upload `data/takemeter_dataset.csv` into your Colab runtime.
3. Configure your `GROQ_API_KEY` under Colab Secrets.
4. Execute all cells to baseline Groq and fine-tune DistilBERT.
5. Save the resulting files into this project's `results/` folder.

## Streamlit Interface
To launch the interactive classification interface:
```bash
cd app
pip install -r requirements.txt
streamlit run app.py
```
*Note: If you have downloaded and placed your fine-tuned model inside `app/model/`, the application will perform live neural network inference. Otherwise, the UI will fall back to a rule-based mock mode for demonstration purposes.*

## Demo Video
[Watch the TakeMeter Demo Video](https://www.loom.com/share/9cd4d4fd6a5e4e1f96325f6aae1956dd)
