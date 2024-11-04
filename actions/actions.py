# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient, errors

# MongoDB client connection
client = MongoClient("mongodb://localhost:27017/")
db = client.dummy_db

class ActionContactDoctors(Action):
    def name(self) -> Text:
        return "action_contact_doctors"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Query MongoDB to get the doctors collection
            doctors_count = db.doctors.count_documents({})  # Replaced the deprecated .count() method

            if doctors_count == 0:
                dispatcher.utter_message(text="No doctors found.")
            else:
                # Fetching all doctors and building the response string
                doctors = db.doctors.find()
                response = ""
                for doctor in doctors:
                    response += f"Name: {doctor['name']}, Specialization: {doctor['specialization']}, Phone: {doctor['phone_number']}\n"
                dispatcher.utter_message(text=response)
        except errors.PyMongoError as e:
            # Handle any MongoDB errors gracefully
            dispatcher.utter_message(text="Sorry, something went wrong while fetching the doctors.")
            print(f"MongoDB error: {e}")  # Log the error for debugging

        return []

class ActionStoreProductDetails(Action):
    def name(self) -> Text:
        return "action_store_product_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Retrieve product type and user message
            product_type = tracker.get_slot("product_type")
            user_message = tracker.latest_message.get('text')

            # Insert product details into the appropriate MongoDB collection
            db[product_type].insert_one({"details": user_message})
            dispatcher.utter_message(text=f"Your {product_type} details have been stored.")
        except errors.PyMongoError as e:
            # Handle any MongoDB errors gracefully
            dispatcher.utter_message(text="Sorry, something went wrong while storing your product details.")
            print(f"MongoDB error: {e}")  # Log the error for debugging

        return []

class ActionStoreUpdateDetails(Action):
    def name(self) -> Text:
        return "action_store_update_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get the user's update message
            user_message = tracker.latest_message.get('text')

            # Insert the update request into MongoDB
            db.updates.insert_one({"update": user_message})
            dispatcher.utter_message(text="Your update request has been stored.")
        except errors.PyMongoError as e:
            # Handle any MongoDB errors gracefully
            dispatcher.utter_message(text="Sorry, something went wrong while storing your update request.")
            print(f"MongoDB error: {e}")  # Log the error for debugging

        return []

class ActionStoreFeedback(Action):
    def name(self) -> Text:
        return "action_store_feedback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get the user's feedback message
            user_message = tracker.latest_message.get('text')

            # Insert the feedback into MongoDB
            db.feedback.insert_one({"feedback": user_message})
            dispatcher.utter_message(text="Your message has been stored.")
        except errors.PyMongoError as e:
            # Handle any MongoDB errors gracefully
            dispatcher.utter_message(text="Sorry, something went wrong while storing your feedback.")
            print(f"MongoDB error: {e}")  # Log the error for debugging

        return []




'''from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.dummy_db

class ActionContactDoctors(Action):
    def name(self) -> Text:
        return "action_contact_doctors"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        doctors = db.doctors.find()
        if doctors.count() == 0:
            dispatcher.utter_message(text="No doctors found.")
        else:
            response = ""
            for doctor in doctors:
                response += f"Name: {doctor['name']}, Specialization: {doctor['specialization']}, Phone: {doctor['phone']}\n"
            dispatcher.utter_message(text=response)
        return []

class ActionStoreProductDetails(Action):
    def name(self) -> Text:
        return "action_store_product_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_type = tracker.get_slot("product_type")
        user_message = tracker.latest_message.get('text')
        db[product_type].insert_one({"details": user_message})
        dispatcher.utter_message(text=f"Your {product_type} details have been stored.")
        return []

class ActionStoreUpdateDetails(Action):
    def name(self) -> Text:
        return "action_store_update_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get('text')
        db.updates.insert_one({"update": user_message})
        dispatcher.utter_message(text="Your update request has been stored.")
        return []

class ActionStoreFeedback(Action):
    def name(self) -> Text:
        return "action_store_feedback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get('text')
        db.feedback.insert_one({"feedback": user_message})
        dispatcher.utter_message(text="Your message has been stored.")
        return []'''

