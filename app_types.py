from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Offers:
    users_info: List[Dict]
    offer_text: str
