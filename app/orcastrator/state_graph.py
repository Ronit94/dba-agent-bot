from typing import TypedDict
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from app.orcastrator.memory import get_memory, add_to_memory
from app.config import groq_api_key

class MyState(TypedDict):
    input: str
    session_id: str
    response: str


def build_agent(vectorstore) -> Runnable:
    
    model = ChatGroq(model="llama3-70b-8192", api_key=groq_api_key)

    def respond(state):
        print(state)
        session_id = state["session_id"]
        history = get_memory(session_id)

        # Use retriever
        retriever = vectorstore.as_retriever()
        context_docs = retriever.get_relevant_documents(state["input"])
        context_text = "\n".join(doc.page_content for doc in context_docs)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Use the following context:\n{context}"),
            *history,
            ("human", "{input}")
        ])

        chain = prompt | model

        result = chain.invoke({
            "input": state["input"],
            "context": context_text
        })

        # Store messages in memory
        add_to_memory(session_id, HumanMessage(content=state["input"]))
        add_to_memory(session_id, AIMessage(content=result.content))

        return {"response": result.content, "session_id": session_id, "input": state["input"]}

    graph = StateGraph(state_schema=MyState)
    graph.add_node("respond", respond)
    graph.set_entry_point("respond")

    return graph.compile()
