# state.py

from dataclasses import field, dataclass, asdict
from typing import List


@dataclass
class InquiryState:
    """ Tracks the inquiry lifecycle state and is passed between agents. """
    client_name: str
    client_email: str
    request_details: str
    is_approved: bool = False
    evaluation_notes: str = ""
    appointment_time: str = ""
    crm_log: str = ""
    activity_log: List[str] = field(default_factory=list)


def state_to_dict(state: InquiryState) -> dict:
    """ Utility function to convert the dataclass state to a dictionary for LangGraph. """
    return asdict(state)
