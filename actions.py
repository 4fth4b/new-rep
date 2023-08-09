# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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


from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
import requests
import pandas as pd


class ActionSlotResetting(Action):

    def name(self) -> Text:
        return "action_slot_value_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Have a nice Time")

        return [SlotSet("battery", None),SlotSet("Internal Memory", None),SlotSet("brand_name", None),SlotSet("RAM", None),SlotSet("camera", None),SlotSet("Adapter_brand", None),SlotSet("Earphone_brand", None),SlotSet("Mobile_Holder_brand", None),SlotSet("CAR_CHARGERS_brand", None),SlotSet("Power_Bank_brand", None)]


# ==============================================================================================================================================
class ActionSeeDetails(Action):

    def name(self) -> Text:
        return "action_see_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        battery = tracker.get_slot("battery")
        InternalMemory = tracker.get_slot("Internal Memory")
        brand_name = tracker.get_slot("brand_name")
        RAM = tracker.get_slot("RAM")
        camera = tracker.get_slot("camera")
        
        response=None

        mobile_data=pd.read_csv("smartPhone.csv")
        mobile_data=mobile_data[["id","name","image1","brand_name","battery","Internal Memory","Primary Camera","RAM"]]
        data1=mobile_data[(mobile_data["RAM"]==RAM) & (mobile_data["battery"]==battery) & (mobile_data["brand_name"]==brand_name) & (mobile_data["Internal Memory"]==InternalMemory) & (mobile_data["Primary Camera"]==camera)]
        data2=mobile_data[(mobile_data["RAM"]==RAM) & (mobile_data["battery"]==battery) & (mobile_data["brand_name"]==brand_name) & (mobile_data["Internal Memory"]==InternalMemory)]
        data3=mobile_data[(mobile_data["RAM"]==RAM) & (mobile_data["battery"]==battery) & (mobile_data["brand_name"]==brand_name)]
        data4=mobile_data[(mobile_data["battery"]==battery) & (mobile_data["brand_name"]==brand_name)]
        data5=mobile_data[(mobile_data["brand_name"]==brand_name)]

        data = data1.append([data2, data3, data4, data5, mobile_data], ignore_index=True)
        data=data.drop_duplicates()
        data=data.set_index('id')
        json = data.to_json(orient ='index') 
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ==========================================================================================================================================
       
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
            {"title": "3279 mAh", "payload": '/battery{"battery":"3279 mAh"}'},
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
    def name(self) -> Text:
        return "action_ask_RAM"
    
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "4 GB", "payload": '/RAM{"RAM":" 4 GB"}'},
            {"title": "6 GB", "payload": '/RAM{"RAM":" 6 GB"}'},
            {"title": "2 GB", "payload": '/RAM{"RAM":" 2 GB"}'},
            {"title": "STOP", "payload": '/stop please'}
        ]
        dispatcher.utter_message(
            text=f"What ram you want?Please confirm",
            buttons=buttons
        )
       
        return []

class AskForInternalMemoryAction(Action):
    def name(self) -> Text:
        return "action_ask_Internal Memory"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "128 GB", "payload": '/Internal Memory{"Internal Memory":" 128 GB"}'},
            {"title": "256 GB", "payload": '/Internal Memory{"Internal Memory":" 256 GB"}'},
            {"title": "32 GB", "payload": '/Internal Memory{"Internal Memory":" 32 GB"}'},
            {"title": "64 GB", "payload": '/Internal Memory{"Internal Memory":" 64 GB"}'},
            {"title": "STOP", "payload": '/stop please'}
        ]
        dispatcher.utter_message(
            text=f"What Internal Memory you want?Please confirm",
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


# ==============================================================================================

class ActionSeeAdapterDetails(Action):

    def name(self) -> Text:
        return "action_see_Adapter_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        Adapter_brand = tracker.get_slot("Adapter_brand")
 
        response=None

        data=pd.read_csv("life_style_full.csv")
        data=data[data["material_name"]=="ADAPTER"]
        data=data[["id","name","image1","brand_name"]]
        data=data[data["brand_name"]==Adapter_brand]
    
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

class AskForAdapter_brandAction(Action):
    def name(self) -> Text:
        return "action_ask_Adapter_brand"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "NYORK", "payload": '/Adapter_info{"Adapter_brand":"NYORK"}'},
            {"title": "SOUNDTECH", "payload": '/Adapter_info{"Adapter_brand":"SOUNDTECH"}'},
            {"title": "PORODO", "payload": '/Adapter_info{"Adapter_brand":"PORODO"}'},
            {"title": "STOP", "payload": '/stop please'}
        ]
        dispatcher.utter_message(
            text=f"Your Preffered brand?",
            buttons=buttons
        )
       
        return []

# ==================================================


class ActionSeeEarphoneDetails(Action):

    def name(self) -> Text:
        return "action_see_Earphone_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        Earphone_brand = tracker.get_slot("Earphone_brand")
 
        response=None

        data=pd.read_csv("life_style_full.csv")
        data=data[data["material_name"]=="EAR PHONE"]
        data=data[["id","name","image1","brand_name"]]
        data=data[data["brand_name"]==Earphone_brand]
    
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

class AskForEarphone_brandAction(Action):
    def name(self) -> Text:
        return "action_ask_Earphone_brand"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "NYORK", "payload": '/Earphones_info{"Earphone_brand":"NYORK"}'},
            {"title": "PORODO", "payload": '/Earphones_info{"Earphone_brand":"PORODO"}'},
            {"title": "STOP", "payload": '/stop please'}
        ]
        dispatcher.utter_message(
            text=f"Your Preffered brand?",
            buttons=buttons
        )
       
        return []

# =====================================================

class ActionSeeMobile_HolderDetails(Action):

    def name(self) -> Text:
        return "action_see_Mobile_Holder_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        Mobile_Holder_brand = tracker.get_slot("Mobile_Holder_brand")
 
        response=None


        data=pd.read_csv("life_style_full.csv")
        data=data[data["material_name"]=="MOBILE HOLDER"]
        data=data[["id","name","image1","brand_name"]]
        data=data[data["brand_name"]==Mobile_Holder_brand]
    
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)


class AskForMobile_Holder_brandAction(Action):
    def name(self) -> Text:
        return "action_ask_Mobile_Holder_brand"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "NYORK", "payload": '/Mobile_Holder_info{"Mobile_Holder_brand":"NYORK"}'},
            {"title": "PORODO", "payload": '/Mobile_Holder_info{"Mobile_Holder_brand":"PORODO"}'},
            {"title": "STOP", "payload": '/stop please'}
        ]
        dispatcher.utter_message(
            text=f"Your Preffered brand?",
            buttons=buttons
        )
       
        return []

# ======================================================


class ActionSeeCAR_CHARGERSDetails(Action):

    def name(self) -> Text:
        return "action_see_CAR_CHARGERS_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        CAR_CHARGERS_brand = tracker.get_slot("CAR_CHARGERS_brand")
 
        response=None


        data=pd.read_csv("life_style_full.csv")
        data=data[data["material_name"]=="CAR CHARGERS"]
        data=data[["id","name","image1","brand_name"]]
        data=data[data["brand_name"]==CAR_CHARGERS_brand]
    
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)



class AskForCAR_CHARGERS_brandAction(Action):
    def name(self) -> Text:
        return "action_ask_CAR_CHARGERS_brand"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "NYORK", "payload": '/CAR_CHARGERS_info{"CAR_CHARGERS_brand":"NYORK"}'},
            {"title": "PORODO", "payload": '/CAR_CHARGERS_info{"CAR_CHARGERS_brand":"PORODO"}'},
            {"title": "STOP", "payload": '/stop please'}
        ]
        dispatcher.utter_message(
            text=f"Your Preffered brand?",
            buttons=buttons
        )
       
        return []

# ========================================================


class ActionSeePower_BankSDetails(Action):

    def name(self) -> Text:
        return "action_see_Power_Bank_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        Power_Bank_brand = tracker.get_slot("Power_Bank_brand")
 
        response=None

        data=pd.read_csv("life_style_full.csv")
        data=data[data["material_name"]=="POWER BANK"]
        data=data[["id","name","image1","brand_name"]]
        data=data[data["brand_name"]==Power_Bank_brand]
    
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

class AskForPower_BankAction(Action):
    def name(self) -> Text:
        return "action_ask_Power_Bank_brand"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        buttons=[
            {"title": "PORODO", "payload": '/Power_Bank{"Power_Bank_brand":"PORODO"}'},
            {"title": "STOP", "payload": '/stop please'}
        ]
        dispatcher.utter_message(
            text=f"Your Preffered brand?",
            buttons=buttons
        )
       
        return []

# ==========================================================================
# ==========================================================================

class ActionSeeHOT_BEVERAGESSDetails(Action):

    def name(self) -> Text:
        return "action_see_HOT_BEVERAGES_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        Hot_beverages=df[df["category_name"]=="HOT BEVERAGES"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ==========================================================================

class ActionSeeCOLD_BEVERAGESDetails(Action):

    def name(self) -> Text:
        return "action_see_COLD_BEVERAGES_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        COLD_beverages=df[df["category_name"]=="COLD BEVERAGES"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ==========================================================================

class ActionSeeHOME_BAKING_AND_COOKINGDetails(Action):

    def name(self) -> Text:
        return "action_see_HOME_BAKING_AND_COOKING_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        HOME_BAKING_AND_COOKING=df[df["category_name"]=="HOME BAKING AND COOKING"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ===========================================================================

class ActionSeeBOTTLED_CANNED_AND_POUCHDetails(Action):

    def name(self) -> Text:
        return "action_see_BOTTLED_CANNED_AND_POUCH_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        data=df[df["category_name"]=="BOTTLED CANNED AND POUCH"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ===========================================================================

class ActionSeeFROZEN_FOODDetails(Action):

    def name(self) -> Text:
        return "action_see_FROZEN_FOOD_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        data=df[df["category_name"]=="FROZEN FOOD"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ===========================================================================

class ActionSee_CONFECTIONERY_Details(Action):

    def name(self) -> Text:
        return "action_see_CONFECTIONERY_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        data=df[df["category_name"]=="CONFECTIONERY"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)
# ===========================================================================

class ActionSeePASTA_NOODLES_AND_RICEDetails(Action):

    def name(self) -> Text:
        return "action_see_PASTA_NOODLES_AND_RICE_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        data=df[df["category_name"]=="PASTA NOODLES AND RICE"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ===========================================================================

class ActionSeeNUTS_DATES_DRIED_FRUITSDetails(Action):

    def name(self) -> Text:
        return "action_see_NUTS_DATES_DRIED_FRUITS_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        data=df[df["category_name"]=="NUTS, DATES & DRIED FRUITS"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ===========================================================================

class ActionSee_CHILLERS_AND_DAIRY_Details(Action):

    def name(self) -> Text:
        return "action_see_CHILLERS_AND_DAIRY_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        data=df[df["category_name"]=="CHILLERS AND DAIRY"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ===========================================================================

class ActionSee_HOME_CLEANING_Details(Action):

    def name(self) -> Text:
        return "action_see_HOME_CLEANING_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        data=df[df["category_name"]=="HOME CLEANING"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ===========================================================================

class ActionSeeHEALTH_AND_BEAUTYDetails(Action):

    def name(self) -> Text:
        return "action_see_HEALTH_AND_BEAUTY_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        data=df[df["category_name"]=="HEALTH AND BEAUTY"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)

# ===========================================================================

class ActionSeeBABY_AND_KIDSDetails(Action):

    def name(self) -> Text:
        return "action_see_BABY_AND_KIDS_details"

    global response
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response=None

        df=pd.read_csv("Full_Bulk.csv")
        data=df[df["category_name"]=="BABY AND KIDS"]
        data=data[["id","name","image1"]]
        data=data.set_index('id')
        json = data.to_json(orient ='index')
    
    
        dispatcher.utter_message(text = 'These are the Products available', json_message =   json)


