# Campus AI Assistant (AI & DS Final Year Project)

Two AI modules in one Streamlit app:
1. **RAG Enquiry Chatbot** - answers from college documents (knowledge_base/*.txt), shows source + confidence, handles spelling mistakes & Tanglish, says "I don't know" instead of guessing.
2. **Early-Warning Dashboard** - upload class CSV -> fail-risk %, risk level, reasons, suggested mentor action, downloadable report.

## Run (VS Code -> Terminal)
    pip install -r requirements.txt
    streamlit run app.py

## MAKE IT YOURS (this is what makes it unique!)
1. app.py line 6: change COLLEGE to your college name
2. Edit knowledge_base/*.txt with your REAL college rules, fees, timings, hostel, placement info
   (paragraphs separated by a blank line; add new .txt files for new topics)
3. Add Tanglish/local words in SYNONYMS in chatbot.py
4. Replace data/sample_class.csv with real/class data (same column names)

## Files
- app.py        : Streamlit UI (Chatbot / Risk Dashboard / Analytics / About)
- chatbot.py    : retrieval engine (TF-IDF word + char n-grams, cosine similarity)
- risk.py       : data generation, training, model comparison, explanations
- knowledge_base/ : college documents    - data/ : sample class csv    - model/ : saved model    - logs/ : chatbot usage

## Architecture
Docs -> chunks -> TF-IDF vectors -> cosine similarity with user query -> best chunk + source
CSV -> features -> best of (LogReg / RF / GB by ROC-AUC) -> risk % ; Logistic coefficients x scaled values -> per-student reasons

## Viva Q&A
- What is RAG? Retrieve relevant documents first, then answer from them, so answers are grounded in real data. Here retrieval is TF-IDF; can be upgraded to embeddings + LLM.
- Why char n-grams? They match words even with spelling mistakes (attendence ~ attendance).
- Why not just use ChatGPT? It can hallucinate college rules; this answers only from official documents and shows the source.
- How are reasons explained? Logistic Regression coefficients x standardized feature values; most negative contributors = reasons for risk.
- Why ROC-AUC? Measures ranking quality across all thresholds - important for prioritising students.
- Is the training data real? Synthetic (generated with realistic rules); replace with real college data for deployment. Pipeline is unchanged.
- Privacy? Runs locally, no data leaves the machine.
- Future scope: sentence-transformer embeddings, LLM answer generation, Tamil voice input, WhatsApp bot, auto SMS to parents/mentors, real LMS data.
