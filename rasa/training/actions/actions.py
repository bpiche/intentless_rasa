import os
import logging
import requests
from typing import Any, Text, Dict, List

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.actions import Action


class ActionIntentlessFAQ(Action):
    """
    """
    def name(self) -> Text:
        """
        """
        return "call_intentless"


    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        """
        host = os.getenv("AI_UTIL_HOST", "util")
        port = os.getenv("AI_UTIL_PORT", 5006)
        query = tracker.latest_message['text']
        headers = {"accept": "application/json",
                   "content-type": "application/json"}
        response = requests.post(f'http://{host}:{port}/similarity',
                                 json={'text': query})
        dispatcher.utter_message(text=response.json().get('answer'))
        return []
 