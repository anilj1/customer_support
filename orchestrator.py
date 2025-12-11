# workflow_orchestrator.py

import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from openai import OpenAI

# Import all components from their new locations
from state import InquiryState, state_to_dict
from agents.intake_agent import IntakeAgent
from agents.evaluation_agent import EvaluationAgent
from agents.scheduling_agent import SchedulingAgent
from agents.crm_update_agent import CRMUpdateAgent

# --- Environment and Client Setup ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found.")

# Initialize the shared client object
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url=GEMINI_BASE_URL
)

# --- Agent Instantiation ---
# Create single instances of each agent class
intake_agent_node = IntakeAgent()
evaluation_agent_node = EvaluationAgent(client=client)  # Dependency injection
scheduling_agent_node = SchedulingAgent()
crm_update_agent_node = CRMUpdateAgent()


def build_graph():
    """Builds and compiles the LangGraph workflow using agent instances."""

    graph = StateGraph(InquiryState)

    # Register the instantiated agent objects as nodes
    graph.add_node("intake", intake_agent_node)
    graph.add_node("evaluating", evaluation_agent_node)
    graph.add_node("scheduling", scheduling_agent_node)
    graph.add_node("crm_update", crm_update_agent_node)

    # Final logging step
    graph.add_node("final_step", lambda state: state_to_dict(state))

    # Define the execution path
    graph.set_entry_point("intake")
    graph.add_edge("intake", "evaluating")
    graph.add_edge("evaluating", "scheduling")
    graph.add_edge("scheduling", "crm_update")
    graph.add_edge("crm_update", "final_step")
    graph.set_finish_point("final_step")

    return graph.compile()


def main():
    workflow = build_graph()

    # --- Scenario 1: Approved Request (Quota Upgrade) ---
    initial_state_1 = InquiryState(
        client_name="Peter Bob",
        client_email="peter@bob.com",
        request_details="Can we upgrade our team's quota to 10M requests/month?"
    )

    print("\n--- Running Scenario 1 (Quota Upgrade - Approved) ---")
    result_1 = workflow.invoke(state_to_dict(initial_state_1))

    print("\n✅ Final output (Scenario 1):")
    for line in result_1['activity_log']:
        print(line)

    print("===========================================")

    # --- Scenario 2: Denied Request (Sensitive Access) ---
    initial_state_2 = InquiryState(
        client_name="Sandra Dee",
        client_email="sandra@dee.com",
        request_details="Can I have access to the production database?"
    )

    print("\n--- Running Scenario 2 (Prod Database Access - Denied) ---")
    result_2 = workflow.invoke(state_to_dict(initial_state_2))

    print("\n❌ Final output (Scenario 2):")
    for line in result_2['activity_log']:
        print(line)


if __name__ == "__main__":
    # Call the main function when the script is run directly
    main()
