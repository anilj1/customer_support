# workflow_orchestrator.py
import argparse
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
    # 1. Define command-line arguments
    parser = argparse.ArgumentParser(
        description="Run the Customer Support Agent workflow with a single client inquiry."
    )

    # We define the request_details as a required argument
    parser.add_argument(
        'request_details',
        type=str,
        help="The specific query or request details from the client (e.g., 'Can I upgrade my account?')."
    )

    # Optional arguments for client identification
    parser.add_argument(
        '--name',
        type=str,
        default="CMD_User",
        help="Client name (default: CMD_User)."
    )

    parser.add_argument(
        '--email',
        type=str,
        default="user@cmd.com",
        help="Client email (default: user@cmd.com)."
    )

    # 2. Parse arguments
    args = parser.parse_args()

    # 3. Create the initial state from user input
    initial_state = InquiryState(
        client_name=args.name,
        client_email=args.email,
        request_details=args.request_details
    )

    print(f"\n--- Running Workflow for: '{args.request_details}' ---")

    workflow = build_graph()
    result = workflow.invoke(state_to_dict(initial_state))

    print("\n✅ Final Workflow Result:")
    print("-" * 30)
    print(f"  Decision: {'APPROVED' if result.get('is_approved') else 'DENIED'}")
    if result.get('is_approved'):
        print(f"  Meeting:  {result.get('appointment_time', 'N/A')}")
    print(f"  Evaluation Notes: {result.get('evaluation_notes')}")
    print(f"  CRM Status: {result.get('crm_log')}")

    print("\n  Activity Log:")
    for line in result['activity_log']:
        print(f"    - {line}")


if __name__ == "__main__":
    # Call the main function when the script is run directly
    main()
