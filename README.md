# HumanSense 🎬

HumanSense is a context-aware movie recommendation system that goes beyond
ratings and popularity. It models *human intent* — why a user wants to watch
something, how they see themselves, and how much cognitive or emotional load
they can handle — to produce more meaningful recommendations.

## Key Features
Unlike traditional recommenders, HumanSense introduces:
- Purpose-driven intent modeling (RELAX, UPLIFT, DISTRACT, EXPLORE)
- Identity-aware biasing (casual vs artistic viewers)
- Cognitive load regulation
- Controlled novelty injection
  
This creates recommendations that feel *human-aligned*, not algorithmic.

## Tech Stack
- Python, Pandas, NumPy
- Sentence Transformers (for semantic embeddings)
- Custom hybrid recommendation engine
- Streamlit (UI)
- Jupyter Notebook (primary evaluation artifact)

## Project Structure
HumanSense/
├── notebooks/ # Final evaluation notebook (.ipynb)
├── src/ # Core recommendation logic
├── models/ # Precomputed embeddings
├── data/ # Sample dataset
├── ui_app.py # Streamlit interface
├── requirements.txt
└── README.md

## How to Run

## How to Run
```bash
pip install -r requirements.txt
streamlit run src/ui_app.py
