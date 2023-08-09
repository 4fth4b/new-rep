# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
import requests
import pandas as pd
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionSeeDetails(Action):

    def name(self) -> Text:
        return "action_see_details"
    global response
    def run(self,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        battery= tracker.get_slot("battery")
        brand_name= tracker.get_slot("brand_name")
        RAM= tracker.get_slot("RAM")
        InternalMemory = tracker.get_slot("Internal Memory")
        camera = tracker.get_slot("camera")

        response=None
        mobile_data=pd.read_csv("smartPhone.csv")
        mobile_data= mobile_data[["id","name","image1","brand_name","battery","Internal Memory","Primary Camera", "RAM"]]
        data1=mobile_data[(mobile_data["RAM"]==RAM) & (mobile_data["battery"]==battery) & (mobile_data["brand_name"]==brand_name) & (mobile_data["Internal Memory"]==InternalMemory) & (mobile_data["Primary Camera"]==camera)]
        data2=mobile_data[(mobile_data["RAM"]==RAM) & (mobile_data["battery"]==battery) & (mobile_data["brand_name"]==brand_name) & (mobile_data["Internal Memory"]==InternalMemory)]
        data3=mobile_data[(mobile_data["RAM"]==RAM) & (mobile_data["battery"]==battery) & (mobile_data["brand_name"]==brand_name)]
        data4=mobile_data[(mobile_data["battery"]==battery) & (mobile_data["brand_name"]==brand_name)]
        data5=mobile_data[(mobile_data["brand_name"]==brand_name)]

        data= pd.concat([data1,data2, data3, data4, data5, mobile_data], ignore_index=True)
        data=data.drop_duplicates()
        data=data.set_index('id')
        json = data.to_json(orient='index')

        dispatcher.utter_message(text = 'These are the Products available', json_message = json)

class AskFormobile_batteryAction(Action):
    def name(self) -> Text:
        return "action_ask_battery"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "5000 mAh", "payload": '/battery{"battery":" 5000 mAh"}'},
            {"title": "3240 mAh", "payload": '/battery{"battery":" 3240 mAh"}'},
            {"title": "3125 mAh", "payload": '/battery{"battery":" 3125 mAh"}'},
            {"title": "3200 mAh", "payload": '/battery{"battery":" 3200 mAh"}'},
            {"title": "3279 mAh", "payload": '/battery{"battery":" 3279 mAh"}'},
            {"title": "4373 mAh", "payload": '/battery{"battery":" 4373 mAh"}'},
            {"title": "4323 mAh", "payload": '/battery{"battery":" 4323 mAh"}'},
            {"title": "3110 mAh", "payload": '/battery{"battery":" 3110 mAh"}'},
            {"title": "STOP", "payload": '/stop please'}
        ]
        dispatcher.utter_message(
            text=f"How much Battery you are looking for?Please confirm",
            buttons=buttons
        )
       
        return []
    
class AskForbrand_nameAction(Action):
    def name(self) -> Text:
        return "action_ask_brand_name"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "SAMSUNG", "payload": '/brand_name{"brand_name":"SAMSUNG"}'},
            {"title": "APPLE", "payload": '/brand_name{"brand_name":"APPLE"}'},
            {"title": "STOP", "payload": '/stop please'}
        ]
        dispatcher.utter_message(
            text=f"What brand you want?Please confirm",
            buttons=buttons
        )
       
        return []
class AskForRamAction(Action):
    def name(self)-> Text:
        return "action_ask_RAM"
    
    def run(
            self,dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "4 GB", "payload": '/RAM{"RAM":" 4 GB"}'},
            {"title": "6 GB", "payload": '/RAM{"RAM":" 6 GB"}'},
            {"title": "2 GB", "payload": '/RAM{"RAM":" 2 GB"}'},
            {"title": "STOP", "payload": '/stop please'},
        ]
        dispatcher.utter_message(
            text=f"What ram you want?",
            buttons=buttons
        )

        return []

class AskForInternalMemoryAction(Action):
    def name(self) -> Text:
        return "action_ask_Internal Memory"
    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict       
    ) -> List[EventType]:
        
        buttons =[
            {"title": "128 GB", "payload": '/Internal Memory{"Internal Memory":" 128 GB"}'},
            {"title": "256 GB", "payload": '/Internal Memory{"Internal Memory":" 256 GB"}'},
            {"title": "32 GB", "payload": '/Internal Memory{"Internal Memory":" 32 GB"}'},
            {"title": "64 GB", "payload": '/Internal Memory{"Internal Memory":" 64 GB"}'},
            {"title": "STOP", "payload": '/stop please'}
        ]
        dispatcher.utter_message(
            text=f"What Internal Memory do you need? Please confirm",
            buttons=buttons
        )
        return []

class AskForcameraAction(Action):
    def name(self) -> Text:
        return "action_ask_camera"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "48+12+12 MP", "payload": '/camera{"camera":" 48+12+12 MP"}'},
            {"title": "12+12 MP", "payload": '/camera{"camera":" 12+12 MP"}'},
            {"title": "50+5+5+2 MP", "payload": '/camera{"camera":" 50+5+5+2"}'},
            {"title": "64+8+5+5 MP", "payload": '/camera{"camera":" 64+8+5+5"}'},
            {"title": "48+8+5+2 MP", "payload": '/camera{"camera":" 48+8+5+2"}'},
            {"title": "48MP + 2 MP", "payload": '/camera{"camera":" 48MP + 2MP"}'},
            {"title": "8 MP", "payload": '/camera{"camera":" 8"}'},
            {"title": "STOP", "payload": '/stop please'}
      
        ]
        dispatcher.utter_message(
            text=f"Your Preffered Camera?",
            buttons=buttons
        )
       
        return []
    
class ActionSlotResetting(Action):

    def name(self) -> Text:
        return "action_slot_value_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Have a nice Time")

        return [SlotSet("battery", None),SlotSet("Internal Memory", None),SlotSet("brand_name", None),SlotSet("RAM", None),SlotSet("camera", None)]

