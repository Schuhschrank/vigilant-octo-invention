from collections import defaultdict
from typing import Optional

from engine.Action import Action
from engine.Stage import Stage
from engine.staging import key_stage


class TravelAction(Action):

    def __init__(
            self,
            new_stage: Stage,
            description: str,
            success_text: str,
            failure_text: str = "",
            auto_disable: bool = False,
            is_enabled: bool = True,
            consequences: Optional[dict] = None,
            conditions: Optional[dict] = None,
            prerequisites: Optional[dict] = None
    ):
        super().__init__(description=description, success_text=success_text, failure_text=failure_text,
                         auto_disable=auto_disable, is_enabled=is_enabled, consequences=consequences,
                         conditions=conditions, prerequisites=prerequisites)
        self.consequences[key_stage] = new_stage
