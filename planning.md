# TakeMeter Planning Document

## Project Overview
TakeMeter is a text classifier designed to categorize soccer and World Cup discourse quality and type. The goal is to build an automated classifier that parses public comments from community forums and groups them into three distinct communication styles: `analysis`, `hot_take`, or `reaction`. This helps identify higher-value analytical contributions, highly subjective/speculative opinions, and immediate emotional reactions within online soccer communities.

## Community Choice
* **Community**: Public soccer and World Cup discussion threads, mainly **r/soccer** and **r/worldcup** on Reddit.
* **Reasoning**: These subreddits are highly active, text-heavy, and contain a broad spectrum of soccer discourse. 
  - **Match threads** (live threads during games) are dominated by fast-paced emotional expressions, exclamation, hype, and sarcasm.
  - **Post-match threads** tend to host strong opinions, bold predictions, and blame/credit judgments ("hot takes").
  - **Weekly discussion threads** and tactical threads contain longer-form tactical breakdowns, historical comparisons, tournament qualification math, and statistical evidence ("analysis").
  This rich variety makes the community an ideal fit for testing a multi-class discourse classifier.

## Label Taxonomy
The taxonomy consists of three mutually exclusive labels:

1. **`analysis`**
   - *Definition*: A soccer comment that explains the game using tactics, statistics, player roles, match context, team structure, tournament math, or specific evidence.
   - *Example 1*: *"Colombia are the better team right now, but they can’t crack the DR Congo defense."*
   - *Example 2*: *"With how the groups have shaped up, a draw against Ghana will probably be enough for Croatia to qualify as a third-place team."*

2. **`hot_take`**
   - *Definition*: A strong opinion, prediction, or judgment about a player, team, manager, or match outcome without sufficient support, data, or detailed reasoning.
   - *Example 1*: *"Croatia are simply not good enough to go far."*
   - *Example 2*: *"Portugal will not win the World Cup."*

3. **`reaction`**
   - *Definition*: A comment that is mostly emotion, humor, hype, anger, sarcasm, or a short immediate response.
   - *Example 1*: *"WHAT A GOAL OMG."*
   - *Example 2*: *"Ref is blind lol."*

## Why the Labels Are Mutually Exclusive
The three categories capture distinct levels of reasoning and intent:
* `analysis` focuses on *evidence* (tactics, stats, match situations, mathematical outcomes).
* `hot_take` focuses on *opinion/judgment without reasoning* (subjective, speculative, binary claims).
* `reaction` focuses on *emotion/humor/brevity* (expressive, conversational filler, short remarks).

**Decision Hierarchy Rules**:
* If a comment has tactical/statistical evidence, label it `analysis` even if it sounds highly opinionated.
* If a comment makes a bold claim or prediction but lacks evidence or reasoning, label it `hot_take`.
* If a comment is short, emotional, sarcastic, or primarily a joke, label it `reaction`.
* Every example maps to exactly one label. No vague or "other" categories are permitted.

## Hard Edge Cases

1. **"0.7 xG on 14 shots."**
   - *Possible labels*: `analysis` vs. `reaction`.
   - *Final decision*: `analysis`.
   - *Reason*: Despite being extremely short and potentially written in frustration, it contains concrete statistical evidence (Expected Goals - xG, shot count) to evaluate performance.
   
2. **"Croatia don’t look great but they didn’t look great in 2022 either and still made a deep run."**
   - *Possible labels*: `analysis` vs. `hot_take`.
   - *Final decision*: `analysis`.
   - *Reason*: Although it starts with an opinion, it justifies this using a clear historical comparison (performance in 2022) to support its reasoning.
   
3. **"This has all the hallmarks of a thrilling nil-nil draw."**
   - *Possible labels*: `reaction` vs. `hot_take`.
   - *Final decision*: `reaction`.
   - *Reason*: This is a sarcastic, humorous comment about a boring game. It is not a serious analytical prediction (`hot_take`), but rather an emotional reaction to the flow of the match.

## Data Collection Plan
* **Source**: Public soccer and World Cup Reddit threads (mainly r/soccer and r/worldcup).
* **Collection Method**: Manually copy public text comments from active threads into a local spreadsheet. AI assistance is used to clean up formatting (stripping Markdown tags, user handles, etc.) and suggest initial labels.
* **Human Review**: The student manually reviews all labels to ensure alignment with the taxonomy rules.
* **Target Size**: At least 200 labeled examples (specifically aiming for 220 comments).
* **Target Distribution**:
  - `analysis`: ~80 examples (36%)
  - `hot_take`: ~70 examples (32%)
  - `reaction`: ~70 examples (32%)

## What I Will Do If a Label Is Underrepresented
If any label falls below 20% of the dataset, target-specific data collection will be performed:
* Underrepresented `analysis`: Extract comments from dedicated post-match tactical analysis or stats-based discussion threads.
* Underrepresented `hot_take`: Extract comments from daily pre-match prediction threads, opinion polls, or unpopular opinion threads.
* Underrepresented `reaction`: Extract comments directly from live match threads during major fixtures (e.g., goals, red cards, controversial decisions).

## Evaluation Metrics
We will evaluate both the Groq baseline model and the fine-tuned DistilBERT model using:
* **Accuracy**: Overall fraction of correct predictions.
* **Precision** (per-class): Out of all comments predicted as a label, how many were actually that label.
* **Recall** (per-class): Out of all actual examples of a label, how many did the model find.
* **F1 Score** (per-class): Harmonic mean of precision and recall.
* **Confusion Matrix**: A table showing actual vs. predicted classifications to visualize boundary errors.

### Why Accuracy Alone Is Insufficient
An imbalanced dataset can inflate accuracy if the model overpredicts the majority class. Evaluating per-class F1 scores ensures the model is learning the distinctive linguistic traits of all three classes. The confusion matrix is critical because the boundary between `hot_take` and `analysis` (opinion with vs. without reasoning) is linguistically subtle, and the matrix will show if the model is confusing these two.

## Definition of Success
* **Random Chance**: For a 3-class balanced dataset, random guessing yields 33.3% accuracy.
* **Success Threshold**: The fine-tuned model should significantly outperform random chance, with a target accuracy of **65% to 75%+**.
* **Per-Class F1 Goal**: An F1 score of **~0.70** or higher for all classes represents high classification success.
* **Groq Comparison**: The fine-tuned model should ideally outperform or match the zero-shot Groq baseline (`llama-3.3-70b-versatile`). If it does not, the project is still considered successful if we clearly analyze and document the failure modes.

## AI Tool Plan
1. **Label Stress-Testing**: Using an LLM to generate edge cases for the defined labels to verify if the decision boundaries are clear and mutually exclusive.
2. **Annotation Assistance**: Cleaning raw scraped comments and generating initial label recommendations, which are then manually verified/corrected by the student.
3. **Failure Analysis**: Using an LLM to help identify semantic patterns in the false positive/false negative groups generated during test-set evaluation.

## Stretch Feature Plan
A Streamlit web interface will be built to showcase the model. 
* Users can input their own comments.
* The app runs model inference and shows the predicted category along with prediction confidence.
* If the exported PyTorch/HuggingFace model is not present, the app will gracefully show a warning and run in an optional interactive mock mode for demonstration purposes.
