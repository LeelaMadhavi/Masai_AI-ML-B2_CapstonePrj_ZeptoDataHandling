Zepto Data & AI Platform
An end-to-end Data Engineering, Advanced RAG, LangGraph, and FastAPI capstone project designed to demonstrate data ingestion, processing, semantic retrieval, intelligent question answering, workflow orchestration, and API deployment.
An AI/ML engineer is expected to move comfortably across the full stack: pulling raw data from the wild, cleaning and storing it properly, understanding it visually, building and evaluating predictive models on it, and — increasingly — wrapping intelligence around it with a deployed GenAI service. In this capstone you are joining Zepto's analytics guild as an incoming AI/ML engineer, and your first assignment is to ship one connected platform made of three internally-linked capabilities: a data-engineering pipeline that turns raw scraped data into a clean relational store, an analytics pipeline that profiles and models a customer-style dataset end to end, and a GenAI support assistant that answers policy questions grounded in Zepto's own documents. All three live together in one repository — this is a single, coherent submission, not three unrelated exercises. Every technique required below is a standard, well-documented technique in professional AI/ML practice, with widely available tooling and documentation support.
You may build the three modules in any order, but they are meant to read as one story: a data pipeline feeds Zepto's analysts clean structured data (/data_pipeline), an analytics pipeline shows how Zepto would profile and predict customer/passenger-style outcomes end to end (/analytics), and a support assistant shows how Zepto would put a grounded GenAI service in front of its own policies (/support_assistant). 
1. Project Overview
Zepto Data & AI Platform is an AI-powered data handling and question-answering platform built around a Retrieval-Augmented Generation (RAG) architecture.
The project combines:
Web/data ingestion and preprocessing
Structured data handling
Exploratory Data Analysis
Semantic embeddings
ChromaDB vector database
Advanced Retrieval-Augmented Generation (RAG)
LangGraph workflow orchestration
Pydantic-based structured responses
FastAPI REST API
Groq LLM integration
Mock LLM mode for deterministic testing
The application processes user queries, identifies the query intent, retrieves relevant Zepto policy information when required, and returns a structured response.
2. Technology Stack
Technology
Purpose
Python
Core programming language
Pandas
Data processing and analysis
BeautifulSoup
Web scraping/data extraction
Sentence Transformers
Text embeddings
ChromaDB
Vector database and semantic retrieval
LangGraph
AI workflow orchestration
Groq
LLM inference
Pydantic
Data validation and structured output
FastAPI
REST API development
Uvicorn
ASGI application server
Git/GitHub
Version control

3. Project Architecture
The overall application follows this workflow:
                        ┌───────────────────────┐
                         │       User Query      │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      FastAPI API      │
                         │       POST /ask       │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      LangGraph        │
                         │    StateGraph Flow    │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   Intent Classifier   │
                         └───────────┬───────────┘
                                     │
                       ┌─────────────┴─────────────┐
                       │                           │
                       ▼                           ▼
             ┌──────────────────┐       ┌──────────────────┐
             │ Policy Question  │       │ General Question │
             └────────┬─────────┘       └────────┬─────────┘
                      │                           │
                      ▼                           ▼
             ┌──────────────────┐       ┌──────────────────┐
             │ Query Embedding  │       │  Direct Answer   │
             └────────┬─────────┘       └────────┬─────────┘
                      │                           │
                      ▼                           │
             ┌──────────────────┐                 │
             │    ChromaDB     │                 │
             │ Vector Retrieval │                 │
             └────────┬─────────┘                 │
                      │                           │
                      ▼                           │
             ┌──────────────────┐                 │
             │ Top-K Retrieved  │                 │
             │     Chunks       │                 │
             └────────┬─────────┘                 │
                      │                           │
                      ▼                           │
             ┌──────────────────┐                 │
             │   LLM / Mock     │◄────────────────┘
             │ Answer Generation│
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Pydantic Response│
             │ Validation       │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │   JSON Response  │
             │ answer/sources/  │
             │ confidence       │
             └──────────────────┘

4. Advanced RAG Architecture
The RAG component uses semantic embeddings and vector similarity search to retrieve relevant Zepto policy information before generating an answer.
            Zepto Policy Documents
                       │
                       ▼
             ┌───────────────────┐
             │ Document Loading  │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ Text Processing   │
             │ & Chunking        │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ Sentence          │
             │ Transformer       │
             │ Embeddings        │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │     ChromaDB      │
             │   Vector Store    │
             └───────────────────┘


User Query
    │
    ▼
┌──────────────────────┐
│ Query Embedding      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ ChromaDB Similarity  │
│ Search               │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Top-3 Relevant       │
│ Document Chunks      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Grounded Prompt      │
│ Construction         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ LLM Answer           │
│ Generation            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Pydantic Validation  │
└──────────┬───────────┘
           │
           ▼
      Structured JSON
RAG Features
Semantic rather than keyword-only retrieval
Sentence Transformer embeddings
ChromaDB vector storage
Top-3 relevant chunk retrieval
Context-grounded answer generation
Source/document ID tracking
Pydantic response validation
Deterministic mock mode for testing
5. LangGraph Architecture
LangGraph is used to orchestrate the application as a state-based workflow.
                      START
                         │
                         ▼
              ┌─────────────────────┐
              │  classify_intent    │
              │                     │
              │ policy_question     │
              │        OR           │
              │ general_question    │
              └──────────┬──────────┘
                         │
                 Conditional Routing
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
 ┌──────────────────────┐   ┌──────────────────────┐
 │ retrieve_and_answer  │   │    direct_answer     │
 │                      │   │                      │
 │ Query Embedding      │   │ No Retrieval         │
 │       ↓              │   │                      │
 │ ChromaDB Retrieval   │   │ Mock/LLM Answer      │
 │       ↓              │   │                      │
 │ Top-3 Chunks         │   │                      │
 │       ↓              │   │                      │
 │ Mock/LLM Answer      │   │                      │
 └──────────┬───────────┘   └──────────┬───────────┘
            │                          │
            └────────────┬─────────────┘
                         │
                         ▼
                       END
LangGraph Nodes
1. classify_intent
Determines whether the incoming query is:
policy_question
general_question
In the default mock mode, classification uses predefined policy keywords.
2. retrieve_and_answer
For policy questions:
Generates an embedding for the user query.
Searches ChromaDB.
Retrieves the top-3 relevant chunks.
Generates a grounded response.
Returns retrieved source IDs.
3. direct_answer
For general questions:
No retrieval is performed.
In mock mode, a deterministic response is returned.
In real LLM mode, the query can be answered directly.
6. FastAPI Architecture
FastAPI provides the REST API layer around the LangGraph workflow.
            Client / User
                  │
                  │ POST /ask
                  ▼
        ┌──────────────────────┐
        │       FastAPI        │
        │                      │
        │ AskRequest           │
        │ {                    │
        │   "query": "..."     │
        │ }                    │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │      LangGraph       │
        │     StateGraph       │
        └──────────┬───────────┘
                   │
                   ▼
             RAG / Direct
               Workflow
                   │
                   ▼
        ┌──────────────────────┐
        │ Pydantic Validation  │
        └──────────┬───────────┘
                   │
                   ▼
             JSON Response

{
  "answer": "...",
  "sources": ["doc_01"],
  "confidence": 1.0
}
7. Project Setup
Step 1 — Clone the Repository
git clone git@github.com:LeelaMadhavi/Masai_AI-ML-B2_CapstonePrj_ZeptoDataHandling.git

Move into the project:
cd Masai_AI-ML-B2_CapstonePrj_ZeptoDataHandling

Step 2 — Create a Virtual Environment
python3 -m venv .venv
Activate it:   source .venv/bin/activate
After activation, the terminal should display something similar to:
(.venv) leela_madhavi@penguin:...
8. Install Dependencies
Install the required Python packages:
pip install -r requirements.txt
If requirements.txt is not available, install the main dependencies:
pip install pandas
pip install beautifulsoup4
pip install requests
pip install sentence-transformers
pip install chromadb
pip install langgraph
pip install fastapi
pip install uvicorn
pip install pydantic
pip install groq
pip install python-dotenv
9. Environment Configuration
Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key
MOCK_LLM=1
Mock LLM Mode
The project uses:
MOCK_LLM=1
as the default configuration.
Mock mode is recommended for the baseline implementation because:
It does not require an LLM API call.
Intent classification is deterministic.
Final responses are deterministic.
API testing is reproducible.
It satisfies the graded baseline requirements.
For optional real LLM execution:
MOCK_LLM=0
A valid GROQ_API_KEY is then required.
Security: Never commit .env or API keys to GitHub.
10. Prepare the Vector Database
The Zepto policy documents are embedded using a Sentence Transformer model and stored in ChromaDB.
Run the document ingestion/indexing script:
python <your_ingestion_script>.py
This creates the local ChromaDB vector store:
chroma_db/
The application subsequently performs semantic similarity searches against the stored documents.
11. Run the LangGraph Application
The LangGraph workflow can be executed from the application/test script:
python <your_langgraph_script>.py

The workflow follows:
User Query
    ↓
Intent Classification
    ↓
Conditional Routing
    ↓
Policy → Retrieval → Answer
    │
    └── General → Direct Answer

12. Run the FastAPI Application
Start the FastAPI server using Uvicorn:
uvicorn app:app --reload

The application will normally be available at:
http://127.0.0.1:8000

FastAPI automatically provides interactive API documentation at:
http://127.0.0.1:8000/docs

13. API Endpoint
POST /ask
The endpoint accepts a JSON request containing a user query.
Request
{
  "query": "How much does priority delivery cost?"
}
Response
{
  "answer": "Based on the retrieved context: ...",
  "sources": [
    "doc_01"
  ],
  "confidence": 1.0
}
14. API Testing
Example 1 — Policy Question
This query contains the keyword delivery, so it is classified as a policy question.
curl -X POST "http://127.0.0.1:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"query":"How much does priority delivery cost?"}'

Expected response structure:
{
  "answer": "Based on the retrieved context: ...",
  "sources": ["doc_01"],
  "confidence": 1.0
}

The exact retrieved text may vary depending on the indexed document content.
Example 2 — General Question
curl -X POST "http://127.0.0.1:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"query":"What is the capital of India?"}'

Expected response:
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}

For a general question, ChromaDB retrieval is not performed.
15. Structured Response Schema
The final API response is validated using Pydantic.
class FinalAnswer(BaseModel):
    answer: str
    sources: list[str]
    confidence: float
The confidence value is constrained between:
0.0 and 1.0
For mock mode:
Policy Question:
confidence = 1.0

General Question:
confidence = 1.0
16. Mock LLM and Real LLM Modes
The application supports two execution modes.
Mock Mode — Default
MOCK_LLM=1
The mock mode provides deterministic behavior for the graded baseline.
Component
Mock Behaviour
Intent Classification
Keyword heuristic
Retrieval
Real ChromaDB retrieval
Answer Generation
Deterministic response
Sources
Retrieved document IDs
Confidence
1.0


Real LLM Mode
MOCK_LLM=0
The application can use the Groq LLM for:
Intent classification
Context-grounded answer generation
Direct answers for general questions
The final response is still validated using the Pydantic schema.
17. Error Handling and Validation
The application validates LLM-generated responses using Pydantic.
For real LLM mode, if the generated response does not conform to the expected schema:
The response is validated.
A corrective instruction is sent to the LLM.
The process can retry up to two additional times.
If validation continues to fail, a clearly marked error response is returned.
This helps maintain a consistent API contract.
18. Security Considerations
The following sensitive files should not be committed to GitHub:
.env
*.pem
private SSH keys
API keys
credentials
Recommended .gitignore entries:
.env
.venv/
__pycache__/
chroma_db/
*.pyc
*.pkl
*.joblib
*.pem
*_sshkey
*_sshkey.pub

API keys should be loaded through environment variables rather than hard-coded in Python source code.
19. End-to-End Workflow
                ┌──────────────────────┐
                 │   Zepto Documents    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Preprocessing &      │
                 │ Document Chunking    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Sentence Transformer │
                 │ Embeddings           │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      ChromaDB        │
                 │    Vector Store      │
                 └──────────────────────┘


User
 │
 ▼
FastAPI /ask
 │
 ▼
LangGraph
 │
 ▼
Intent Classification
 │
 ├─────────────── Policy Question ───────────────┐
 │                                               │
 │                                               ▼
 │                                      Query Embedding
 │                                               │
 │                                               ▼
 │                                      ChromaDB Retrieval
 │                                               │
 │                                               ▼
 │                                      Top-3 Context Chunks
 │                                               │
 │                                               ▼
 │                                      Grounded Answer
 │                                               │
 └──────────── General Question ────────────────┐
                                                │
                                                ▼
                                         Direct Answer
                                                │
                                                ▼
                                      Pydantic Validation
                                                │
                                                ▼
                                         JSON Response
20. Project Outcome
The Zepto Data & AI Platform demonstrates an end-to-end implementation of a modern AI application combining:
Data handling and preprocessing
Semantic search
Vector databases
Retrieval-Augmented Generation
State-based AI workflows
LLM integration
Structured output validation
REST API development
Reproducible mock execution
Secure API-key management
The architecture separates retrieval, reasoning, orchestration, validation, and API serving, making the application modular and suitable for further extension.
Once implementation of all the three modules are ready and working fine, then you need to give following git commands in the same order:
git pull origin main --allow-unrelated-histories --no-rebase
Git status
Git add .
Git commit -m “relevant message”
Git remote -v
Git push -u origin main 
For implementation of Tasks in all the three Modules, kindly refer below description module-wise
Module-1 - (/data_pipeline)
Zepto's analysts need a way to benchmark catalog-style pricing and availability data before it ever reaches a dashboard. In this module you'll play that data-engineering role: scrape live product data from a public scraping-practice site, clean it, enrich it with the project's baseline fixed-rate currency conversion, and load it into a properly normalized relational database that you then query with both SQL and pandas — exactly the kind of raw-to-relational pipeline a catalog/competitive-intelligence workflow needs.

Data source: books.toscrape.com — a public website built specifically for scraping practice. It requires no login, no API key, and imposes no paid tier; you may scrape it freely. (The catalogue happens to be books rather than groceries — that's fine, the exercise is about the pipeline mechanics: scrape → clean → convert → store → query, which is identical regardless of product category.)

Tasks
1. Using the requests and BeautifulSoup libraries, scrape all books listed across at least 3               
    different book categories (or, if you prefer, the first 5 paginated listing pages of the "All                       
    products" catalogue — either scope is acceptable as long as your final dataset has at least 60        
    books). For each book capture: title, price (as listed, in GBP), star_rating (as text, e.g.     
    "Three"), availability (as listed text), and category.

2. Clean the scraped fields into proper types:
Strip the currency symbol from price and convert it to a float column price_gbp.
Convert the text star rating (One…Five) into an integer column rating (1–5). Parse the availability text into a boolean column in_stock.
If any field fails to parse for a given row (e.g., unexpected text), handle it with the median-imputation approach for numeric fields or drop the row (state and justify your choice) — do not leave the pipeline crashing on messy rows.
3. Convert price_gbp to a price_inr column using the project's fixed baseline conversion rate: 1       
    GBP = 105.50 INR. This is an artificial, project-defined constant for this assignment, not a live    
    or historical market rate, so it never needs a lookup or a date reference. This fixed-rate 
    conversion is the required, keyless baseline and is what gets graded for this task — it 
    requires no external API call and no network access; simply state this exact rate in your 
    README. (Optional, ungraded stretch — must not affect your required submission: if you 
    want extra practice with the requests library and explicit HTTP status-code handling, you may 
    additionally look up any free, keyless currency-conversion API of your own choosing, check 
    its response status code explicitly, and fall back to the fixed rate above on any failure. This is 
    entirely optional; your price_inr column must be fully correct using only the required fixed-rate 
    baseline, since that path alone is what gets graded.)
4. Design a normalized SQLite schema with at least two tables sharing a primary/foreign key 
     relationship, for example:
categories(category_id INTEGER PRIMARY KEY, category_name TEXT UNIQUE)
books(book_id INTEGER PRIMARY KEY, title TEXT, price_gbp REAL, price_inr REAL, rating INTEGER, in_stock INTEGER, category_id INTEGER REFERENCES categories(category_id))
5. (You may rename columns/tables, but the two-table PK/FK structure is required.)
6. Using Python's sqlite3 (or pandas.DataFrame.to_sql), insert your cleaned, converted data 
    into this schema. Then write and execute at least 5 SQL queries against the database that 
    collectively demonstrate: SELECT/WHERE, ORDER BY, LIMIT, DISTINCT, and (IN or  
    BETWEEN) — plus at least one JOIN between your two tables (e.g., "list the 10 highest-rated 
    books per category"). Save each query string and its output.
7. Read back at least two of the above query results into pandas DataFrames using 
    pd.read_sql(...), and separately reproduce the join-query's result using pd.merge(...) directly 
    on your in-memory DataFrames (no SQL) — show that both approaches produce equivalent 
    Output.

Module-2 - (/analytics)
This module is Zepto's analyst-to-data-scientist workflow in one pass: profile a dataset, handle its imperfections defensibly, tell a clear visual stor about it, and then build and rigorously evaluate a full predictive-modeling pipeline on top of the same data. Load the classic Titanic dataset once, through Seaborn's built-in loader: sns.load_dataset('titanic'). Note that this loader requires internet access the first time it runs, since it fetches the dataset from Seaborn's online data repository and caches it locally; subsequent runs on the same machine reuse the cache and do not need the network again.

This is deliberately one cohesive pipeline, not two disconnected exercises: you load the dataset once, clean it once, and every later step — EDA, modeling, tuning, the regression side-task — builds on that same cleaned data. A natural way to structure this inside /analytics is two clearly ordered notebooks that share one committed CSV — e.g. 01_eda.ipynb (loads the data, profiles it, cleans it, saves titanic.csv, and produces the full EDA story) followed by 02_modeling.ipynb (reads the same committed titanic.csv that 01_eda.ipynb produced, and continues straight into the modeling pipeline). Scripts instead of notebooks, or a single notebook, are equally acceptable — what matters is that the dataset is loaded from the network/cache exactly once, and every subsequent step is a continuation of that one load, never an independent second sns.load_dataset('titanic') call.

Tasks
Part A — Profiling, cleaning, and the data story

Load the dataset and profile it: print df.info(), df.describe(), and df.shape. Compute and report the percentage of missing values in every column that has any. Immediately after loading, save the loaded DataFrame as a committed offline fallback — df.to_csv("titanic.csv", index=False) — inside /analytics, so your submission can be graded via pd.read_csv("titanic.csv") even if sns.load_dataset(...) cannot reach the internet at grading time. This is the one and only load of the raw dataset; everything below — including the modeling pipeline — works from this same DataFrame or its saved CSV.

Apply missing-value handling per column, following this threshold rule (under 5% missing → drop those rows; 5%–30% missing → impute) — and for any column whose missing rate is so high that imputation would be unreliable, explicitly decide to either drop the column or encode "missing" as its own category, and justify that decision in writing. State the exact percentage you measured for each affected column before choosing its strategy.

Univariate analysis: plot a histogram and a box plot for both age and fare. Using the IQR rule (outliers are points outside [Q1 − 1.5×IQR, Q3 + 1.5×IQR]), report how many outliers each column has. Compute mean, median, and mode for fare, and state in writing whether its distribution is right-skewed, left-skewed, or symmetric, referencing the mean/median/mode ordering.

Outlier counts:
{'fare': 114, 'age': 65}


Bivariate analysis: using boolean masking (with &/| combinations), compute and report survival rate broken down by (a) sex, (b) pclass, and (c) sex and pclass together. Then compute a correlation matrix restricted to exactly these six columns: survived, pclass, age, sibsp, parch, and fare — the dataset's numeric columns, including survived (0/1-valued) as the natural numeric target. Exclude the boolean-typed columns adult_male and alone from the correlation matrix: they are derived/redundant flags (directly computable from sex/age and from sibsp+parch respectively), not independent measured features. Render the resulting 6×6 matrix as a heatmap using sns.heatmap, with a short written interpretation of the two strongest correlations you observe — defined precisely as the two feature pairs with the largest absolute off-diagonal correlation coefficients (rank all off-diagonal pairs by abs(correlation) and take the top two).
Multivariate "data story": produce at least 4 distinct charts (any combination of bar/box/scatter/heatmap/pair-plot) that together build a coherent argument about who was more likely to survive and why. Each chart must be accompanied by a 2–4 sentence written interpretation in your README/notebook — a chart with no interpretation does not count.
As an exploratory check (not yet the modeling pipeline's own preprocessing — that is handled separately in Task 8 below), standardize age and fare using the z-score formula z = (x − mean) / std on the full cleaned DataFrame (you may use StandardScaler or compute it manually). Show a before/after comparison (e.g., a printed summary of means/stds, or overlaid distribution plots) confirming the transformed columns have (approximately) mean 0 and standard deviation 1. This is purely an EDA-stage sanity check; it does not feed into the modeling pipeline, which performs its own train-only scaling.

Part B — Predictive modeling, continuing from the same cleaned data

Split the data into train/test sets first, using a stratified split (justify why stratification matters given the class balance you observed in Task 1). Use survived as the classification target.
Preprocessing (fit on training data only): handle missing values in the columns you use (you do not need to match your Task 2 strategy exactly, but state your choice), encode categorical columns (sex, embarked) with label or one-hot encoding, and scale numeric features with StandardScaler. Every preprocessing step (imputer, encoder, scaler) must be fit only on the training split, then applied in transform-only mode to the test split — never fit or refit any preprocessing step on the test data or on the full pre-split dataset, since that leaks test-set information into training. It is strongly recommended you implement this with a scikit-learn Pipeline/ColumnTransformer (a ColumnTransformer for per-column imputing/encoding/scaling, wrapped in a Pipeline with the final estimator) so the fit-on-train / transform-on-test separation is enforced structurally rather than left for you to remember by hand.
Train three classifiers on the same train/test split: Logistic Regression, Decision Tree, and Random Forest. For the Decision Tree, additionally render it with plot_tree, labeling feature names and class names.
Evaluate all three models with: a confusion matrix, accuracy, precision, recall, F1 score, and an ROC curve with AUC. Present these side by side in a single comparison table.
Imbalance handling comparison: report survived/not-survived class balance, then retrain (any one of the three models is enough for this sub-task) three ways — (a) baseline/no handling, (b) class_weight='balanced', (c) SMOTE oversampling applied only to the training fold (to avoid leakage) — and compare precision/recall/F1 across the three variants, with a short written conclusion on which imbalance strategy worked best and why.
Hyperparameter tuning: run GridSearchCV over the Random Forest's n_estimators, max_depth, and max_features, report the best parameter combination and the corresponding out-of-bag (OOB) score. Because oob_score_ is only populated when oob_score=True is passed at construction time, you must construct the estimator as RandomForestClassifier(oob_score=True, ...) (together with your other chosen/tuned parameters) — otherwise the OOB score will not be available to report.
Regression side-task: using the same dataset, predict fare from the other available features with a multivariate linear regression. Report MAE, RMSE, R², and Adjusted R², and produce a residual plot, stating in writing whether it shows heteroscedasticity (a non-random spread of residuals).
Write a model comparison table that presents the three classifiers' metrics (accuracy, precision, recall, F1, AUC) side by side, and the regression model's metrics (MAE, RMSE, R², Adjusted R²) side by side as their own separate columns. Classification metrics and regression metrics are on different scales and are not directly comparable numbers — the table must present them as two distinct metric groups (one per model type), not implied to be on a single shared scale. Add a 3–5 sentence final written recommendation of which classifier you would deploy and why, referencing specific metric values.
Save your best-performing complete pipeline — the fitted preprocessing steps (imputer/encoder/scaler, or your ColumnTransformer) together with the final estimator, as a single combined object (e.g. a scikit-learn Pipeline) — to disk using joblib.dump(full_pipeline, ...). Do not save the bare estimator alone: the saved artifact must be usable end-to-end on raw, unpreprocessed new data. Include a short script/cell that reloads it with joblib.load and confirms it still predicts correctly on raw input.

Module-3 - (/support_assistant)
This module asks you to build a small but complete GenAI service for Zepto: a document corpus you embed and index, a LangGraph-orchestrated flow that routes each query and retrieves grounded context, a structured-output guarantee, and a FastAPI wrapper you run locally. The entire pipeline is graded through a deterministic, fully offline mock mode for the LLM calls — no signup, no API key, and no network access to any LLM

LLM calls — offline mock is the graded baseline (read before starting): every LLM call in this module is gated behind a single environment variable, MOCK_LLM. Left unset, or set to MOCK_LLM=1, the service runs the fully deterministic, rule-based mock logic described in Task 3 below — no signup, no API key, and no network call to any LLM provider. Only when MOCK_LLM=0 is explicitly set does the service call a real LLM. set MOCK_LLM=0 and use Groq's API free tier (console.groq.com) as your LLM backend. 

Embeddings — no API needed: generate embeddings locally using the open-source sentence-transformers library with the all-MiniLM-L6-v2 model, and store them in ChromaDB — both run entirely on your machine at no cost and require no account.

Tasks
Load all 8 documents, chunk them (a simple per-document chunk, or a smaller fixed-size chunking scheme, is fine given their length), embed each chunk with all-MiniLM-L6-v2, and store the embeddings in a ChromaDB collection.
Design a structured prompt template following the role–context–task–format–length skeleton, including at least one explicit negative constraint (e.g., "do not answer using information not present in the provided context") and at least one few-shot example embedded in the prompt.
Build a LangGraph StateGraph with a TypedDict state and at least 3 nodes. Every node's generation step must branch on the MOCK_LLM toggle from above — the mock branch is the required, graded baseline; the real-LLM branch is the optional MOCK_LLM=0 extension:
classify_intent — classifies the incoming query as either policy_question (needs retrieval from the Zepto policy corpus) or general_question (does not need retrieval). Mock mode (MOCK_LLM unset or 1 — graded baseline): classify using a keyword heuristic — if the lowercased query contains any of "delivery", "return", "refund", "membership", "tracking", "cancel", "gift card", or "support hours", classify it policy_question; otherwise classify it general_question. No LLM call is made. Optional MOCK_LLM=0 extension: call the LLM to classify instead.
retrieve_and_answer — for policy_question queries: embeds the query and retrieves the top-3 most similar chunks from ChromaDB via cosine similarity — this retrieval step always runs for real, in both modes, since embedding and ChromaDB need no API key and no network call. Only the final answer-generation step branches on MOCK_LLM. Mock mode (graded baseline): instead of calling an LLM, return a canned templated answer of the form f"Based on the retrieved context: {top_chunk_snippet}", where top_chunk_snippet is a short excerpt (e.g. the first ~200 characters) of the single most similar retrieved chunk. Optional MOCK_LLM=0 extension: prompt the real LLM (using your structured template from Task 2) to answer grounded only in the retrieved chunks.
direct_answer — for general_question queries: mock mode (graded baseline): return a fixed canned string (e.g. "I can only answer questions about Zepto policies right now."), with no LLM call. Optional MOCK_LLM=0 extension: prompt the LLM directly, with no retrieval.
Wire a conditional edge from classify_intent that routes to retrieve_and_answer or direct_answer based on the classification, mirroring a graph-based intent router. This routing logic does not itself depend on MOCK_LLM — only the generation step inside each node does.
Enforce a JSON output schema on the final answer via a Pydantic model with fields answer (string), sources (list of chunk/document IDs used, empty for general_question answers), and confidence (float 0–1). In mock mode, populate this schema deterministically from your own code — there is no LLM output to fail validation, since none was generated: e.g. sources = the ids of the chunks retrieved for policy_question, empty for general_question; confidence = a fixed value such as 1.0. In the optional MOCK_LLM=0 extension, if the real LLM's raw output fails to validate against this schema, retry up to 2 additional times with a corrective instruction before giving up and returning a clearly marked error response.
Wrap the graph in a FastAPI application with a POST /ask endpoint that accepts a Pydantic request model ({"query": str}) and returns the validated Pydantic response model above. Run it locally with uvicorn and demonstrate at least 2 example calls (one that should trigger retrieval, one that should not) with their raw JSON responses recorded in your README — run with MOCK_LLM left at its default, since that is what gets graded.
Write a Dockerfile for the FastAPI app that builds successfully and, on docker run, serves the POST /ask endpoint locally (e.g. via CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"] or equivalent). This locally buildable-and-runnable Dockerfile is the required, graded baseline for containerization — you do not need to push it anywhere to earn full marks. (Optional, ungraded stretch — must not affect your required submission: if you want the extra practice, deploy the same Dockerfile to Hugging Face Spaces using the free community CPU tier (no payment required), storing your LLM API key as a Space secret — never hardcode it or commit it to the repository — and include the live Space URL in your README along with a note confirming which tier (free) you used. This is entirely optional; your Dockerfile must be fully correct and locally runnable using only the required baseline, since that alone is what gets graded.)
In your README, write a short architecture description of the full RAG pipeline, covering each stage in order — ingestion → embedding → retrieval → generation — stating in text which component handles each stage (e.g., which files/functions perform chunking and embedding, which ChromaDB collection stores the vectors, which LangGraph node performs retrieval, and which node/prompt produces the final generated answer) and how data flows between them. Also state which stage(s) branch on the MOCK_LLM toggle and what changes between its default (mock) state and the optional real-LLM state. A short labeled diagram made of text/ASCII boxes and arrows is welcome but not required — a clear prose walkthrough of the pipeline stages satisfies this task.

RAG Pipeline Architecture
The Zepto Data & AI Platform implements an end-to-end Retrieval-Augmented Generation (RAG) pipeline that transforms Zepto policy documents into searchable vector representations and uses semantic retrieval to provide grounded answers to user queries.
Full RAG Pipeline
┌──────────────────────────┐
│  1. INGESTION            │
│  Zepto Policy Documents  │
│  doc_01, doc_02, ...     │
└────────────┬─────────────┘
             │
             │ Documents / Text
             ▼
┌──────────────────────────┐
│  2. EMBEDDING            │
│  SentenceTransformer     │
│  all-MiniLM-L6-v2        │
│                          │
│  encode(documents)       │
└────────────┬─────────────┘
             │
             │ Vectors + IDs + Metadata
             ▼
┌──────────────────────────┐
│  ChromaDB                │
│  Collection:             │
│  "zepto_documents"       │
│                          │
│  Persistent: ./chroma_db │
└────────────┬─────────────┘
             │
             │ Semantic Search
             │ Top-3 Chunks
             ▼
┌──────────────────────────┐
│  3. RETRIEVAL            │
│  LangGraph Node:         │
│  retrieve_and_answer     │
│                          │
│  Query → Embedding →     │
│  ChromaDB → Top-3 Docs   │
└────────────┬─────────────┘
             │
             │ Retrieved Context
             ▼
┌──────────────────────────┐
│  4. GENERATION           │
│  LangGraph Node:         │
│  retrieve_and_answer     │
│                          │
│  Mock OR Groq LLM        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  FinalAnswer             │
│  answer                  │
│  sources                 │
│  confidence              │
└──────────────────────────┘

Stage 1 — Ingestion
The pipeline begins with the Zepto policy documents stored as text in the document dictionary. The documents contain information such as delivery policy, returns and refunds, membership tiers, and order tracking.
The ingestion/indexing code collects the document IDs and text:
ids = list(documents.keys())
texts = list(documents.values())

These documents are then passed to the embedding stage.
Stage 2 — Embedding
The project uses the Sentence Transformers model:
all-MiniLM-L6-v2

The documents are converted into numerical vector embeddings using:
embeddings = model.encode(
    texts,
    convert_to_numpy=True
).tolist()

The generated embeddings, document IDs, text, and metadata are stored in ChromaDB.
Stage 3 — Vector Storage and Retrieval
The embeddings are persisted in the ChromaDB collection:
Collection: zepto_documents
Storage:    ./chroma_db

During a user query, the same embedding model converts the query into a vector:
query_embedding = embedding_model.encode(
    [query],
    convert_to_numpy=True
).tolist()

The retrieve_and_answer LangGraph node then performs semantic search against the zepto_documents collection and retrieves the top 3 relevant documents/chunks:
results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

The retrieved documents and their IDs are passed forward as the grounding context for answer generation.
Stage 4 — Generation
The LangGraph retrieve_and_answer node is responsible for generating the final answer for policy-related questions.
The retrieved chunks are combined into the context:
context = "\n\n".join(retrieved_chunks)

In real-LLM mode, this context is supplied to a structured prompt that instructs the LLM to answer using only the retrieved information and return a validated FinalAnswer containing:
answer
sources
confidence

The final response is validated using the Pydantic FinalAnswer model before being returned by the FastAPI /ask endpoint.

LangGraph Control Flow
Before retrieval, the query passes through the classify_intent node.
                      ┌──────────────────────┐
                       │      User Query      │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │   classify_intent    │
                       └──────────┬───────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          policy_question              general_question
                    │                           │
                    ▼                           ▼
       ┌──────────────────────┐      ┌──────────────────────┐
       │ retrieve_and_answer  │      │    direct_answer     │
       │                      │      │                      │
       │ Query → Embedding →  │      │ Direct response      │
       │ ChromaDB → Top-3     │      │ without retrieval    │
       └──────────┬───────────┘      └──────────┬───────────┘
                  │                             │
                  └──────────────┬──────────────┘
                                 ▼
                         ┌───────────────┐
                         │  FinalAnswer  │
                         └───────────────┘

The routing decision is based on the classified intent and does not depend on MOCK_LLM.

MOCK_LLM Behaviour
The MOCK_LLM environment variable controls the generation/classification behaviour of the LangGraph nodes.
By default:
MOCK_LLM=1

the application runs in mock mode, which does not require a Groq API call.
Mock Mode
User Query
    │
    ▼
classify_intent
    │
    ├── policy_question ──► retrieve_and_answer
    │                         │
    │                         ├── Query embedding
    │                         ├── ChromaDB top-3 retrieval
    │                         └── Mock grounded response
    │
    └── general_question ──► direct_answer
                              │
                              └── Fixed mock response

For policy questions, retrieval still happens in mock mode. The retrieved context is used to construct a simple deterministic response.
For general questions, direct_answer returns the fixed mock response:
I can only answer questions about Zepto policies right now.

Real-LLM Mode
When:
MOCK_LLM=0

the optional Groq LLM is enabled.
The retrieval process remains the same:
Query
  ↓
Embedding
  ↓
ChromaDB
  ↓
Top-3 Retrieved Context
  ↓
Structured Grounding Prompt
  ↓
Groq LLM
  ↓
JSON
  ↓
Pydantic FinalAnswer Validation

In real-LLM mode:
classify_intent can use the LLM for intent classification.
retrieve_and_answer performs the same ChromaDB retrieval but uses the retrieved context in the LLM generation prompt.
direct_answer can generate a response using the LLM.
The generated JSON is validated against the FinalAnswer Pydantic schema.
Key Architecture Principle
The RAG retrieval pipeline is independent of the MOCK_LLM toggle. The toggle changes how the generation/classification stages behave, not whether semantic retrieval is performed for policy questions.
Therefore, the core data flow is:
Policy Documents
      ↓
SentenceTransformer
      ↓
ChromaDB: zepto_documents
      ↓
User Query
      ↓
LangGraph classify_intent
      ↓
retrieve_and_answer
      ↓
Top-3 Retrieved Context
      ↓
Mock Response OR Groq LLM
      ↓
Pydantic FinalAnswer
      ↓
FastAPI /ask

This architecture separates document indexing, semantic retrieval, orchestration, answer generation, and API serving, making each stage independently testable and allowing the real LLM to be enabled without changing the fundamental RAG retrieval workflow.
