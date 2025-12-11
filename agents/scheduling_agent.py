# agents/scheduling_agent.py

import datetime
from state import InquiryState, state_to_dict


class SchedulingAgent:
    """
    Agent responsible for scheduling an appointment if the request is approved.
    In a real-world scenario, this would interface with a calendar API.
    """

    def __call__(self, state: InquiryState) -> dict:
        if state.is_approved:
            # Calculate the meeting time
            meeting_time = datetime.datetime.now() + datetime.timedelta(days=1, hours=2)
            state.appointment_time = meeting_time.strftime("%Y-%m-%d %H:%M:%S")
            state.activity_log.append(f"Meeting scheduled for {state.appointment_time}")
            print("[SchedulingAgent] Appointment time set.")
        else:
            state.activity_log.append("Scheduling skipped (Request was denied).")
            print("[SchedulingAgent] Skipping due to denial.")

        return state_to_dict(state)
