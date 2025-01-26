import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from langserve import add_routes
import uvicorn


_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

llm = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()

SYSTEM_TEMPLATE = 'Translate the following into {langauge}:'

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ('system', SYSTEM_TEMPLATE),
    ('user', '{text}')
])

CHAIN = PROMPT_TEMPLATE | llm | parser

app = FastAPI (
    title="LinguaSetu",
    version="1.0",
    description="A Simple API server using LangChain's Runable Interface"
)

add_routes(
    app,
    CHAIN,
    path="/chain",
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)