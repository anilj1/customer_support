# agents/crm_update_agent.py

from state import InquiryState, state_to_dict


class CRMUpdateAgent:
    """
    Agent responsible for logging the final status in a simulated CRM system.
    In a real-world scenario, this would interface with a CRM API.
    """

    def __call__(self, state: InquiryState) -> dict:
        # Simulate interaction with a CRM API/database
        status = "Approved" if state.is_approved else "Denied"

        # Add logic to determine what specific fields to update
        update_detail = f"Status: {status}. Appointment: {state.appointment_time if state.is_approved else 'N/A'}."

        state.crm_log = f"CRM updated: {update_detail}"
        state.activity_log.append("CRM update completed.")
        print("[CRMUpdateAgent] Status logged.")
        return state_to_dict(state)
