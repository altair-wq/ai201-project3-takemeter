import os
import streamlit as st

# Set page configuration with custom title and icon
st.set_page_config(
    page_title="TakeMeter - Soccer Discourse Classifier",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling for UI polishing
st.markdown("""
<style>
    /* Custom styles for the app */
    .main-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        background: linear-gradient(135deg, #FF4B4B, #FF8F00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }
    .subtitle {
        font-family: 'Inter', sans-serif;
        color: #888888;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }
    .badge {
        padding: 0.35em 0.65em;
        font-size: 0.85em;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.375rem;
        color: white;
    }
    .badge-analysis { background-color: #00C851; }
    .badge-hot-take { background-color: #FF8800; }
    .badge-reaction { background-color: #0099CC; }
    
    .card {
        padding: 1.5rem;
        border-radius: 0.75rem;
        background-color: #1E1E24;
        border: 1px solid #2E2E38;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to find a model folder
def get_model_path():
    possible_paths = ["app/model", "model", "../model"]
    for path in possible_paths:
        # We look for config.json or safetensors/bin file to confirm HF model presence
        if os.path.exists(path) and (
            os.path.exists(os.path.join(path, "config.json")) or 
            os.path.exists(os.path.join(path, "pytorch_model.bin")) or
            os.path.exists(os.path.join(path, "model.safetensors"))
        ):
            return path
    return None

# Load HF model with caching to avoid reloading on each run
@st.cache_resource
def load_hf_classifier(model_path):
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch
        
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        return tokenizer, model
    except Exception as e:
        return None, str(e)

# Sidebar contents
st.sidebar.markdown("<h2 style='text-align: center;'>Soccer Discourse</h2>", unsafe_allow_html=True)
st.sidebar.image("https://img.icons8.com/isometric/100/soccer-ball.png", use_container_width=True)

st.sidebar.markdown("""
### Label Taxonomy
- **🟢 Analysis**: Explains play using tactics, stats, player roles, match context, or concrete evidence.
- **🟠 Hot Take**: A bold opinion, prediction, or judgment without supporting evidence.
- **🔵 Reaction**: High emotion, humor, hype, anger, sarcasm, or very short responses.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### Sample Comments to Try:")
st.sidebar.code("0.7 xG on 14 shots.", language="text")
st.sidebar.code("Croatia are simply not good enough to go far.", language="text")
st.sidebar.code("WHAT A GOAL OMG.", language="text")

# Main Page Layout
st.markdown('<h1 class="main-title">TakeMeter ⚽</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">An intelligent classifier for soccer and World Cup discourse quality</p>', unsafe_allow_html=True)

# Determine model availability
model_dir = get_model_path()
has_real_model = False
tokenizer, model = None, None
model_error = ""

if model_dir:
    try:
        tokenizer, model = load_hf_classifier(model_dir)
        if model is not None:
            has_real_model = True
        else:
            model_error = tokenizer # Contains error details
    except Exception as e:
        model_error = str(e)

# Mode configuration
if not has_real_model:
    st.warning("⚠️ **No trained model found.** Export your fine-tuned model folder from Colab to `app/model/` to run real local neural network predictions. Using interactive **Mock Mode** instead.")
    mode = "Mock Mode (Rule-Based Heuristics)"
else:
    st.success(f"🤖 Loaded fine-tuned model from: `{model_dir}`")
    mode = "Fine-Tuned Neural Classifier"

# User inputs
st.markdown("### Test a Comment")
input_text = st.text_area(
    "Enter a comment from a soccer discussion thread:",
    placeholder="e.g., With how the groups have shaped up, a draw against Ghana will probably be enough...",
    height=120
)

# Heuristic Mock Prediction logic
def mock_predict(text):
    text_lower = text.lower().strip()
    if not text_lower:
        return "reaction", 0.50, [0.15, 0.15, 0.70]
        
    # Analysis cues: numbers, stats, tactics, formations, terms
    analysis_cues = ["xg", "expected goals", "percent", "stats", "tactical", "formation", "draw", "points", "math", "group", "qualify", "3-5-2", "4-3-3", "subbed", "possession", "defense", "pressing", "counter"]
    # Hot take cues: claims without proof, extreme judgments, predictions
    hot_take_cues = ["never", "always", "finished", "fraud", "worst", "best", "washed", "win the world cup", "not good enough", "overrated", "underrated"]
    # Reaction cues: caps, short exclamation, emotes, emojis, sarcasm
    reaction_cues = ["omg", "lol", "lmao", "wtf", "blind", "ref", "goal", "night guys", "vamos", "wow", "siuu", "fcs", "haha", "shit"]

    # Simple heuristic counts
    analysis_score = sum(1 for cue in analysis_cues if cue in text_lower)
    hot_take_score = sum(1 for cue in hot_take_cues if cue in text_lower)
    reaction_score = sum(1 for cue in reaction_cues if cue in text_lower)
    
    # Text length adjustment
    word_count = len(text_lower.split())
    if word_count < 5:
        reaction_score += 2
    elif word_count > 15:
        analysis_score += 1

    # Final logic
    if analysis_score > hot_take_score and analysis_score > reaction_score:
        probs = [0.75, 0.15, 0.10]
        return "analysis", 0.75, probs
    elif hot_take_score > analysis_score and hot_take_score > reaction_score:
        probs = [0.10, 0.80, 0.10]
        return "hot_take", 0.80, probs
    elif reaction_score > 0:
        probs = [0.05, 0.05, 0.90]
        return "reaction", 0.90, probs
    else:
        # Default fallback
        if word_count > 10:
            return "hot_take", 0.55, [0.25, 0.55, 0.20]
        else:
            return "reaction", 0.60, [0.10, 0.30, 0.60]

# Perform prediction when button clicked
if st.button("Classify Comment", type="primary"):
    if not input_text.strip():
        st.error("Please enter a valid, non-empty comment to classify.")
    else:
        st.markdown("---")
        st.subheader("Classification Results")
        
        if has_real_model:
            # Real neural classification
            import torch
            import torch.nn.functional as F
            
            inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = model(**inputs)
                probs = F.softmax(outputs.logits, dim=-1)[0]
                
            labels = ["analysis", "hot_take", "reaction"]
            # Look up model config mapping if custom mapping was exported
            if hasattr(model.config, "id2label") and model.config.id2label:
                labels = [model.config.id2label.get(i, labels[i]) for i in range(len(labels))]
                
            prob_list = probs.tolist()
            pred_id = torch.argmax(probs).item()
            predicted_label = labels[pred_id]
            confidence = prob_list[pred_id]
            
        else:
            # Mock mode classification
            predicted_label, confidence, prob_list = mock_predict(input_text)
            
        # Display the result card
        badge_style = "badge-analysis" if predicted_label == "analysis" else "badge-hot-take" if predicted_label == "hot_take" else "badge-reaction"
        label_title = predicted_label.upper().replace("_", " ")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h3>Predicted Discourse Class</h3>
                <span class="badge {badge_style}" style="font-size: 1.5rem; padding: 0.5rem 1rem;">
                    {label_title}
                </span>
                <h4 style="margin-top: 1.5rem;">Confidence</h4>
                <h1 style="color: #FF4B4B; margin-top:-0.5rem;">{confidence:.2%}</h1>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("### Class Probabilities")
            classes = ["Analysis", "Hot Take", "Reaction"]
            for cls_name, prob in zip(classes, prob_list):
                st.write(f"**{cls_name}**")
                st.progress(prob)
                st.write(f"Probability: `{prob:.2%}`")
        
        if not has_real_model:
            st.caption("ℹ️ *Note: This prediction is based on rule-based keyword heuristics (Mock Mode) because no model weights were uploaded. Export your model from Colab to get real outputs.*")
