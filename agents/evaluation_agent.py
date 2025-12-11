# agents/evaluation_agent.py

from state import InquiryState, state_to_dict
from openai import OpenAI

# Configuration Constants (often externalized in a real service)
GEMINI_MODEL = "gemini-2.5-flash"


class EvaluationAgent:
    """
    Agent responsible for using the LLM to approve or deny the request.
    This agent requires the OpenAI client dependency.
    """

    def __init__(self, client: OpenAI):
        self.client = client
        self.model = GEMINI_MODEL

    def __call__(self, state: InquiryState) -> dict:
        try:
            # System instruction is crucial for guiding the LLM's decision
            system_instruction = (
                f"Approve or deny the following client request. Respond only with 'approved' or 'denied'. "
                f"Strictly deny any request that involves access to production systems, code repositories, "
                f"or sensitive customer data. "
            )

            state.activity_log.append(f"Request details: {state.request_details}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Client request: {state.request_details}"}
                ],
                temperature=0.2,
                max_tokens=200
            )

            decision = response.choices[0].message.content.strip().lower()
            state.is_approved = "approved" in decision

            if state.is_approved:
                state.evaluation_notes = "Approved: Request is within policy limits."
            else:
                state.evaluation_notes = f"Denied: LLM decision was '{decision}'. Request violates policy."

            state.activity_log.append("Evaluation: " + state.evaluation_notes)
            print(f"[EvaluationAgent] Decision made: {'APPROVED' if state.is_approved else 'DENIED'}.")

        except Exception as e:
            state.is_approved = False
            state.evaluation_notes = f"Evaluation failed due to API error: {e}"
            state.activity_log.append("Evaluation error")

        return state_to_dict(state)
