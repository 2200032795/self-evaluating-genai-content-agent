# Self-Evaluating GenAI Content Agent

## Project Overview

The Self-Evaluating GenAI Content Agent is an AI-powered application that generates beginner-friendly educational lessons, evaluates their quality using a strict seven-criterion rubric, rejects lessons that fail evaluation, and regenerates improved content using evaluator feedback.

The system also maintains persistent memory using SQLite to retrieve previous failures and guide future content generation.

## Problem Statement

AI-generated educational content may contain incorrect information, unexplained technical terms, or incomplete explanations.

This project addresses these issues through an automated generation, evaluation, rejection, and regeneration workflow.

## Key Features

- AI-powered lesson generation using Google Gemini.
- Beginner-friendly educational content generation.
- Seven binary evaluation criteria.
- Automatic PASS/FAIL decisions.
- Automatic rejection of failed lessons.
- Regeneration using evaluator feedback.
- Maximum of three generation attempts.
- Persistent memory using SQLite.
- Rejection logs and run history.
- Interactive Streamlit dashboard.
- Offline demonstration using previously saved results.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Google Gemini API | Lesson generation and AI evaluation |
| Streamlit | Interactive user interface |
| SQLite | Persistent memory |
| JSON | Evaluation results and rejection logs |
| Python-dotenv | Environment variable management |

## System Architecture

User Input
    |
    v
Lesson Generator (Gemini)
    |
    v
Lesson Evaluator
    |
    v
Seven-Criterion Evaluation
    |
    +---- PASS ----> Save Approved Lesson
    |
    +---- FAIL ----> Record Rejection
                         |
                         v
                  Evaluator Feedback
                         |
                         v
                  Regenerate Lesson
                         |
                         v
                  Evaluate Again

SQLite Memory stores previous failures and run history for future runs.

## Evaluation Criteria

1. Accuracy
2. Beginner Friendliness
3. Examples
4. Jargon Explanation
5. Topic Coverage
6. Teaching Flow
7. Completeness

Each criterion receives a binary PASS or FAIL result.

A lesson is approved only when all seven criteria pass.

## Regeneration Strategy

The system allows a maximum of three attempts:

- Initial lesson generation.
- First regeneration after evaluation failure.
- Second regeneration if another failure occurs.

If the lesson does not pass within the limit, it is not approved.

Temporary API service failures are handled separately from content-quality failures.

## Persistent Memory

SQLite maintains two tables:

- `run_history`: Stores topic, final status, number of attempts, and execution time.
- `failure_memory`: Stores rejected evaluation criteria and failure explanations.

Previous failure information is retrieved and supplied as guidance during future generation runs.

This is feedback-based memory, not model retraining.

## Project Structure

GenAI-Content-Agent/
|
|-- app.py
|-- agent.py
|-- generator.py
|-- evaluator.py
|-- memory.py
|-- config.py
|-- prompts.py
|-- test_connection.py
|-- test_evaluator.py
|-- requirements.txt
|-- .gitignore
|-- .env
|
|-- data/
|   |-- agent_memory.db
|
|-- outputs/
    |-- generated_lesson.md
    |-- final_lesson.md
    |-- evaluation.json
    |-- rejection_log.json

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd GenAI-Content-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash
```

Never upload your API key to GitHub.

### 6. Run the application

```bash
streamlit run app.py
```

Open:

http://localhost:8501

## Testing

Test Gemini connectivity:

```bash
python test_connection.py
```

Test deliberate-error detection:

```bash
python test_evaluator.py
```

Run the complete agent demonstration:

```bash
python agent.py
```

## Demonstrated Results

The project successfully demonstrated:

- Generation of a beginner-friendly RAG lesson.
- Evaluation using seven quality criteria.
- Detection and rejection of a deliberately inserted false claim.
- Regeneration using evaluator feedback.
- Successful evaluation of the regenerated lesson.
- Storage and retrieval of previous failure information using SQLite.

## Limitations

- AI-based evaluation may still make incorrect judgments.
- The local deliberate-error detector checks specific known false claims and is not a general-purpose fact checker.
- Gemini API availability and free-tier quotas may affect live generation.
- Offline demonstration displays previously saved results rather than generating new content.

## Future Improvements

- Add reference-based factual verification.
- Expand deterministic quality checks.
- Support multiple educational topics.
- Add evaluation analytics and memory insights.
- Improve retry and API failure handling.

## Author

Developed as a GenAI engineering assignment.
