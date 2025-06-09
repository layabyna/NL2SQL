# Natural Language to SQL Query Engine using LangGraph, LangChain & Gemini

This project enables users to ask natural language questions about a database and receive accurate answers by automatically generating and executing SQL queries. It uses Google's Gemini LLM, LangChain tools, and LangGraph for a structured, state-driven flow.

---

## Features

- Converts user questions to SQL queries using Gemini 2.0.
- Executes queries against an SQLite database (`Chinook.db`).
- Returns readable answers from SQL results.
- Manages flow using a LangGraph `StateGraph` pipeline.

---

## Tech Stack

- **LangGraph** – State-based execution for LLM workflows  
- **LangChain** – Toolkit for prompt engineering & SQL tools  
- **Gemini API (Google GenAI)** – Language model for query generation  
- **SQLite** – Sample database backend (`Chinook.db`)  
- **Python** – Core logic and orchestration  
- **dotenv** – Load API keys securely from `.env`  

---

## Project Structure

```
.
├── main.py          # Core project logic
├── Chinook.db       # SQLite sample database
├── .env             # Environment variables
└── requirements.txt # Python dependencies
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/NL2SQL.git
cd nl2sql-gemini
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

Create a `.env` file in the project root:

```env
API=your_gemini_api_key_here
```

---

## How to Run

```bash
python NL2SQL.py
```

You will see step-by-step outputs of query generation, execution, and response.

---

## Example

**Input:**
```
Question: List all employees
```

**LLM Output SQL Query:**
```sql
SELECT FirstName, LastName FROM Employee;
```

**Final Answer:**
```
There are 8 employees. Their names are: Andrew Adams, Nancy Edwards, ...
```

---

## Notes

- Only specific table and column names are used — no `SELECT *`.
- Top-K limit is enforced unless specified by the user.
- Easily extendable to other databases or LLMs.

---

## To-Do

- Add error handling for invalid SQL
- Add support for multiple database dialects
- Integrate with Streamlit or Gradio for a UI
