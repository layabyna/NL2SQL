
# Natural Language to SQL Query Engine using LangGraph, LangChain & Gemini

This project enables users to ask natural language questions about a database and receive accurate answers by automatically generating and executing SQL queries. It uses Google's Gemini LLM, LangChain tools, and LangGraph for a structured, state-driven flow.

---

## Features

- Converts user questions to SQL queries using Gemini 2.0.
- Executes queries against an SQLite database (`Chinook.db`).
- Returns readable answers from SQL results.
- Offers a Flask API endpoint `/ask` for programmatic use.
- Manages flow using a LangGraph `StateGraph` pipeline.

---

## Tech Stack

- **LangGraph** – State-based execution for LLM workflows  
- **LangChain** – Toolkit for prompt engineering & SQL tools  
- **Gemini API (Google GenAI)** – Language model for query generation  
- **SQLite** – Sample database backend (`Chinook.db`)  
- **Flask** – API server  
- **Docker** – Containerized deployment  
- **Python** – Core logic and orchestration  
- **dotenv** – Load API keys securely from `.env`  

---

## Project Structure

```
.
├── app.py           # Flask API
├── Nl2Sql.py        # Core NL-to-SQL logic
├── Chinook.db       # SQLite sample database
├── Dockerfile       # Docker setup
├── .env             # Environment variables
└── requirements.txt # Python dependencies
```

---

## Setup Instructions (Manual)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/NL2SQL.git
cd NL2SQL
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

## Run Locally (Manual)

```bash
python app.py
```

The API will be available at:  
`http://127.0.0.1:5000/ask`  

Send a POST request with JSON like:

```json
{
  "question": "List all employees"
}
```

---

## Docker Instructions

### 1. Build the Docker Image

```bash
docker build -t nl2sql-api .
```

### 2. Run the Container

```bash
docker run -p 5000:5000 --env-file .env nl2sql-api
```

Now, access the API at:  
`http://localhost:5000/ask`

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

- Avoids `SELECT *` by default.
- Limits results unless instructed otherwise.
- Easily extensible for other LLMs or SQL engines.

---

## To-Do

- Add error handling for malformed input
- Support PostgreSQL or MySQL
- Add web UI using Streamlit or Gradio
