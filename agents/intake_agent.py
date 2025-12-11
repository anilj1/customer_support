# agents/intake_agent.py

import datetime
from state import InquiryState, state_to_dict


class IntakeAgent:
    """
    Agent responsible for logging the initial request and marking the start.
    """

    def __call__(self, state: InquiryState) -> dict:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state.activity_log.append(
            f"Request received from {state.client_name} ({state.client_email}) at {timestamp}."
        )
        print(f"[IntakeAgent] Request logged for {state.client_name}.")
        return state_to_dict(state)
