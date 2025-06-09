from langgraph.graph import START, StateGraph
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
import getpass
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from langchain_community.utilities import SQLDatabase
from pydantic import BaseModel, Field

load_dotenv()

# importing the database by using sqlite library
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
print(db.dialect)  # type of database
print(db.get_usable_table_names())  # table names of the db
db.run("SELECT * FROM Artist LIMIT 10;")

# creating a class and passing required parameters
# TypeDict allows you to specify dictionary-like objects with a fixed structure and types for each key.


class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str


# To pass the API Key of the LLM we use, Gemini API Key is passed here
# setting the environment varaiable for the api key if it is not set already.
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("API")

# Initializes a lightweight Gemini 2.0 chat model using that API key.
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")


# Passing a message to the LLM
system_message = """
Given an input question, create a syntactically correct {dialect} query to
run to help find the answer. Unless the user specifies in his question a
specific number of examples they wish to obtain, always limit your query to
at most {top_k} results. You can order the results by a relevant column to
return the most interesting examples in the database.

Never query for all the columns from a specific table, only ask for a the
few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema
description. Be careful to not query for columns that do not exist. Also,
pay attention to which column is in which table.

Only use the following tables:
{table_info}
"""

# Building a prompt template system to define and inspect a structured chat prompt before sending it to Gemini(LLM)
# This defines a template string where {input} is a placeholder.
user_prompt = "Question: {input}"


# Sends system level instructions and user's input to the LLM
query_prompt_template = ChatPromptTemplate(
    [("system", system_message), ("user", user_prompt)]
)


# Loops through messages(system+user)
for message in query_prompt_template.messages:
    message.pretty_print()
# Annotated allows you to add extra metadata to type hints
    from typing_extensions import Annotated


# Class to generate Sql query by the llm

# query is of string and has some meta data.
class QueryOutput(BaseModel):
    query: str = Field(..., description="Syntactically valid SQL query.")


def write_query(state: State):
    """Generate SQL query to fetch information."""

    # Fill in system message
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )

    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result.query}



'''telling the model to produce a query as an output, 
    Sends the prompt (built from the user’s question + table info) to the LLM
    Returns the query'''

# example of passing the question.
# print(write_query({"question": "How many Employees are there?"}))


'''QuerySQLDatabaseTool is a utility from LangChain that:
Takes a SQL query string.
Executes it on the given database.
Returns the results in a readable format.'''


def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}


def generate_answer(state: State):
    """Answer question using retrieved information as context.
    sending prompt to the model to return an answer
    """

    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}


# This code builds and runs a workflow/pipeline graph that processes a question
# Passing the functions to State
graph_builder = StateGraph(State).add_sequence(
    [write_query, execute_query, generate_answer]
)
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile()

def database_question(question):
    steps = list(graph.stream({"question": question}, stream_mode="updates"))
    print(steps)
    return steps
        
