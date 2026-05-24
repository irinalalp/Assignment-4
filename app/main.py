from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.memory.sqlalchemy_session import SQLAlchemySession
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent, ResponseReasoningTextDeltaEvent, ResponseFunctionToolCall
from app.llm_models import model
from app.models import engine
import asyncio
from app.tools import edit,exec_command, write

load_dotenv()

session = SQLAlchemySession(engine=engine, session_id="coding-2", create_tables=True)

SYSTEM_PROMPT = """
You are an expert in building simple browser games using HTML, CSS, and JavaScript.

Action Space:
- use write tool to write game files into a path
- use edit tool to fix or update existing game files
- use exec_command for terminal ops like reading files
"""

agent = Agent(
    "assistant",
    instructions="You are a helpful agent, always answer with a good energy",
    model=model,
    tools=[write,edit,exec_command],
)

async def run_agent():
    while True:
        user_input = input("Enter your message: ")
        if user_input == "exit":
            break

        runner = Runner.run_streamed(
            agent,
            input=user_input,
            max_turns=20,
            session=session
        )

        async for event in runner.stream_events():
            if event.type == "raw_response_event":
                if isinstance(event.data, ResponseTextDeltaEvent): #type: ignore
                    print(event.data.delta, flush=True, end="") #type: ignore
                elif isinstance(event.data, ResponseReasoningTextDeltaEvent): #type: ignore
                    print(event.data.delta, flush=True, end="") #type: ignore
            elif event.type == "run_item_stream_event":
                if event.name == "tool_called": #type: ignore
                    if isinstance( event.item.raw_item, ResponseFunctionToolCall): #type: ignore
                        print(event.item.raw_item.name) #type: ignore
                        print(event.item.raw_item.arguments) #type: ignore
                elif event.name == "tool_output": #type: ignore
                    print(event.item.raw_item) #type: ignore
            elif event.type == "agent_updated_stream_event":
                pass

        print("\n")

if __name__ == "__main__":
    asyncio.run(run_agent())