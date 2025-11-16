from langgraph.graph import StateGraph, START,END
from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import os
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver,InMemorySaver 
import sqlite3

load_dotenv()

class ResponseState(TypedDict):
    message : Annotated[list[BaseMessage],add_messages]
    

model = ChatGoogleGenerativeAI(model='gemini-2.0-flash',api_key=os.getenv('API_KEY'))

def genRes(state : ResponseState):
    text = state['message']
    response = model.invoke(text).content
    return {'message':[response]}
    

def get_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add()
    
graph = StateGraph(ResponseState)
graph.add_node('genRes',genRes)

graph.add_edge(START,'genRes')
graph.add_edge('genRes',END)

# first i create database file that return conn to that database which we then pass to SqliteSaver
conn = sqlite3.connect('chatbot.db',check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)

workflow = graph.compile(checkpointer=checkpointer)

# to get all threads list from db
def get_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)
    

