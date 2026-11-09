from langchain.agents import create_agent

from models import llm as model
from tools import calculate_right_refund, get_user_purchase_history, issue_refund_ticket
from dotenv import load_dotenv

from prompts import agent_system_prompt
from objects import Answer

from  langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
 
from uuid import uuid4

load_dotenv()  # Load environment variables from .env file

agent = create_agent(
    model=model,
    system_prompt=agent_system_prompt,
    tools=[get_user_purchase_history, calculate_right_refund, issue_refund_ticket],
    response_format=Answer,
    checkpointer=InMemorySaver(),
)

def run_conversation():
    config = {"configurable": {"thread_id": str(uuid4())}}

    question= HumanMessage(content="I want a refund for the item I purchased ")
    conversation=True

    while conversation:
        response = agent.invoke({"messages":question},config=config)
        structured_response = response.get("structured_response")

        if structured_response is None:
            # The model replied in plain text instead of the Answer format.
            print(response["messages"][-1].content)
            conversation = True
        else:
            print(structured_response.answer)
            conversation = structured_response.conversation

        if conversation:
            user_input = input("repl: \n")
            question = HumanMessage(content=user_input)

    print("Conversation ended.")


if __name__ == "__main__":
    run_conversation()