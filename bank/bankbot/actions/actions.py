



import json
from pathlib import Path
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import os

class ActionBank(Action):
    
    acc = ""
    print("hello1")
    u = "anon"
    li = list()
    
    def checkuser(self,user):
        global acc
        
        global li

        
        print("hello")
        self.u = user.username
        print(self.u)
        path = f"../bank/bankbot/data/{self.u}.txt"
        my_file = open(path, "r")
        content = my_file.read()
        c_l = content.split(",")
        my_file.close()
        print(c_l)
        f = open("../bank/bankbot/data/data.txt", 'w')
        for c in c_l:
            f.write(c+'\n')
            

    
    def name(self) -> Text:
        return "action_bank"
    

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global acc
        
        lie = []
        print(f'run-> {self.u}')
        acc1 = open("data/data.txt", 'r+')
        print(f'acc->{acc1}')
        for line in acc1.readlines():
            lie.append(line)
            
        
        for blob in tracker.latest_message['entities']:
            print(tracker.latest_message)
            if blob['entity'] == 'account':
                n = blob['value']
            if n == "number":
                msg = lie[0]
            if n == "crn":
                msg = lie[1]
            if n == "balance":
                msg = lie[2]

        dispatcher.utter_message(text=f"Here, {msg}")

        return []

import asyncio
import inspect
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Dict, Any, Optional, Callable, Awaitable, NoReturn

import rasa.utils.endpoints
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)

