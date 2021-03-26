from __future__ import absolute_import
from __future__ import division
from typing import Text, Dict, Any, List, Union
from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Action, Tracker
from rasa_core_sdk.events import SlotSet
import logging
from datetime import datetime
from datetime import date
import json
import csv
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction
from rasa_core_sdk.events import UserUtteranceReverted, \
    ConversationPaused, FollowupAction, Form
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.agent import Agent
import logging
import pymongo;
from pymongo import MongoClient
from instamojo_wrapper import Instamojo

logger = logging.getLogger(__name__)



class ResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("admission_no", None), SlotSet("complaint_message", None), SlotSet("department", None), SlotSet("department_type", None), SlotSet("employee", None), SlotSet("fees_type", None), SlotSet("graduate", None), SlotSet("position", None), SlotSet("semester", None)]


class ActionChitchat(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self):
        return "action_chitchat"

    def run(self,  dispatcher,  tracker,  domain):
        intent = tracker.latest_message['intent'].get('name')

        # retrieve the correct chitchat utterance dependent on the intent
        if intent in ['greet', 'insult', 'greet_whatsup', 'user_is_angry', 'user_is_back', 'user_say_usersname', 
		              'greets_goodevening', 'greets_goodnight', 'greets_goodmorning', 'greets_nice_to_meet_you', 
					  'greets_nice_to_see_you', 'greets_nice_to_talk_to_you', 'user_is_going_to_bed', 'user_ask_about_bot', 
					  'user_says_wow', 'user_ask_bot_orgin', 'user_say_bot_is_beautiful', 'user_ask_bot_to_be_clever', 
					  'user_ask_bot_age', 'user_ask_bot_birth_date', 'user_asks_is_bot_there', 'user_will_be_back', 
					  'user_want_to_talk', 'user_ask_is_bot_sure', 'user_says_bot_is_right', 'user_asks_bot_residence', 
					  'user_ask_bot_occupation', 'user_ask_is_bot_ready', 'user_ask_is_bot_busy', 'user_ask_builder', 
					  'user_asks_bot_help', 'user_asks_bot_is_friend', 'user_say_bot_boring', 'user_ask_bot_marry_user', 
					  'user_ask_bot_hungry', 'user_ask_bot_hobby', 'user_ask_if_bot_happy', 'user_asks_how_are_you', 
					  'user_ask_bot_is_robot', 'user_laughs', 'user_is_good', 'user_says_its_wrong', 'user_asks_what_do_you_mean', 
					  'user_says_sorry', 'user_says_i_dont_care', 'user_want_hug', 'user_ask_to_wait', 'user_says_well_done', 'user_says_welcome', 'user_is_sad', 
					  'user_is_testing_bot', 'user_is_tired', 'user_want_to_see_bot_again', 'user_is_waiting', 'user_is_sleepy', 
					  'user_is_happy', 'user_has_birthday_today', 'user_is_here', 'user_is_joking', 'user_likes_bot', 'user_misses_bot', 
					  'user_is_lonely', 'user_is_bored', 'user_loves_bot', 'user_needs_advice', 'user_is_busy', 'what_user_look_like', 
					  'user_not_want_to_talk', 'user_say_thank_you', 'user_say_no_problem', 'user_say_bot_good', 'user_say_bot_funny', 
					  'user_say_bot_bad', 'user_say_bot_fired', 'user_can_not_sleep', 'user_say_bot_clever', 'user_saying_bot_crazy', 
					  'user_saying_good_answer', 'user_is_excited', 'bot_answer_my_question', 'user_find_bot_annoying', 
					  'user_saying_bad_answer', 'math', 'arts_sports', 'user_ask_languagesbot', 'user_ask_whatisusername', 
					  'user_ask_whoami', 'ask_time', 'ask_weather', 'ask_what_can_bot_do', 'user_say_bot_canthelp', 
					  'out_of_scope', 'goodbye', 'user_ask_can_bot_understand']:
            dispatcher.utter_template('utter_' + intent,  tracker)
        return []

class ActionFAQ(Action):
    """Returns the FAQ utterance dependent on the intent"""

    def name(self):
         return "action_faq"

    def run(self,  dispatcher,  tracker,  domain):
        intent = tracker.latest_message['intent'].get('name')

        # retrieve the correct chitchat utterance dependent on the intent
        if intent in ['ask_cms_info','ask_cms_contact','user_ask_exam_results',
		              'user_ask_exam_timetable','ask_cms_location','user_ask_curriculum','user_ask_where_to_pay_fees',
					  'user_ask_programs_offered','user_ask_fees_concession']:
            dispatcher.utter_template('utter_' + intent,  tracker)
        return []		

class ActionEventDetails(Action):
    """Returns the Event Details"""

    def name(self):
        return "action_event_details"

    def run(self,  dispatcher,  tracker,  domain):
        import bs4 as bs
        import urllib.request
        global responsMsg
        global msg,msg1,msg2
        responsMsg = ""
        msg1 = ""
        msg2 = ""
        msg = ""
        n = 0
        sauce=urllib.request.urlopen('http://cmscollege.ac.in/latest-events.html').read()
        html=bs.BeautifulSoup(sauce,'html.parser')
        for my_tag in html.find_all(class_=["row event_box"]):
            n = n + 1
            if n<3:
                msg1 = msg1 + my_tag.text.strip()
            else:
                msg2 = msg2 +"\n \n" + my_tag.text.strip()
            msg1 = msg1.replace('\n',' ')
            msg2 = msg2.replace('\n',' ')
        responsMsg = " - "+msg1+"\n \n - "+msg2
        dispatcher.utter_message(responsMsg)
        return [] 
	

class ActionAdmissionDetails(Action):
    """Returns the Admission Details"""

    def name(self):
        return "action_admission_details"

    def run(self,  dispatcher,  tracker,  domain):
	    
        gra = tracker.get_slot('graduate')
        if gra.strip() == "ug":
            responseMsg = "You can check out UG admission details by [click here](http://cmscollege.ac.in/online-admission.html)"		
        elif gra.strip() == "pg":    
            responseMsg = "You can check out PG admission details by [click here](http://cmscollege.ac.in/pg-admission.html)" 
        else:
            responseMsg = "You can check out UG admission details by [click here](http://cmscollege.ac.in/online-admission.html)"+"You can check out PG admission details by [click here](http://cmscollege.ac.in/pg-admission.html)"
        dispatcher.utter_message(responseMsg)
        return [] 




class ComplaintForm(FormAction):
    """Accept free text input from the user for compaliant"""

    def name(self):
        return "complaint_form"

    @staticmethod
    def required_slots(tracker):
        return ["complaint_message"]

    def slot_mappings(self):
        return {"complaint_message": self.from_text()}

    def submit(self, dispatcher, tracker, domain):
        client = MongoClient('localhost', 27017)


        complaint = tracker.get_slot('complaint_message')
        db = client.cmsbot
        complaint_table = db.complaint
        complaint_table.insert({"complaint": complaint}) 
        responseMsg2 =  """Your complaint is {} . and thank you we will look into it""".format(complaint)             
        """dispatcher.utter_template('utter_complaint_message', tracker)"""
        dispatcher.utter_message(responseMsg2)
        return []


class EmployeeSearchForm(FormAction):
    """Search employee"""

    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "employee_search_form"

    @staticmethod
    def required_slots(tracker):
       # type: () -> List[Text]
        """A list of required slots that the form has to fill"""

        if tracker.get_slot('position') == 'examination controller':
          return ["position"]
        elif tracker.get_slot('position') == 'vice principal':
          return ["position"]
        elif tracker.get_slot('position') == 'principal':
          return ["position"]
        elif tracker.get_slot('position') == 'hod':
          return ["position", "department"]
        else:
          return ["employee", "position", "department"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"position": [self.from_entity(entity="position",
                                                intent=["inform",
                                                        "user_ask_employee_details"])],
                "employee": [self.from_entity(entity="employee",
                                                intent=["inform",
                                                        "user_ask_employee_details"])],
                "department": [self.from_entity(entity="department",
                                                  intent=["inform",
                                                          "user_ask_employee_details"])]}                                                    

    def submit(self, dispatcher, tracker, domain):
        employee = tracker.get_slot('employee')
        position = tracker.get_slot('position')
        department = tracker.get_slot('department')
        
        global emp
        global pos
        global dep
        global con  
        emp = str(employee)
        pos = str(position)
        dep = str(department)
        con = ""
        client = MongoClient('localhost', 27017)

        db = client.cmsbot
        table = db.employee_info        
        if position == "vice principal":
           staff = table.find_one({"position": "vice principal"})
           emp = staff["name"]
           con = staff["contact"]
           responseMsg = """Vice principal is {} you can contact by {}.""".format(emp, con) 
        elif position == "principal":
            staff = table.find_one({"position": "principal"})  
            emp = staff["name"]
            con = staff["contact"]
            responseMsg = """principal is {} you can contact by {}.""".format(emp, con) 
        elif position == "examination controller":
            staff = table.find_one({"position": "principal"})
            emp = staff["name"]
            pos = staff["position"]
            con = staff["contact"]
            responseMsg = """Examination controller is {} you can contact by {}.""".format(emp, con) 
        elif position == "hod":
            staff = table.find_one({"department": department.strip(), "position": "hod"})
            emp = staff["name"]
            con = staff["contact"]
            responseMsg = """employee name is {} you can contact by {}.""".format(emp, con)
        else: 
            staff = table.find_one({"name": {'$regex': ".*" + employee.strip() + ".*"}, "department": department.strip()})
            no = table.find({"name": {'$regex': ".*" + employee.strip() + ".*"}, "department": department.strip()}).count()
            if no == 1: 
                emp= staff["name"]
                pos = staff["position"]
                dep = staff["department"]
                con = staff["contact"]
                responseMsg = """employee name is {} is {} of {} you can contact by {}.""".format(emp, pos, dep, con)               
            else:
                responseMsg = "the staff you are looking for is not found."
        dispatcher.utter_message(responseMsg)
        return []
            





class FeesDateForm(FormAction):
    """fees date"""

    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "fees_date_form"

    @staticmethod
    def required_slots(tracker):
       # type: () -> List[Text]
        """A list of required slots that the form has to fill"""

        return ["fees_type", "semester", "graduate", "department_type"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"fees_type": [self.from_entity(entity="fees_type",
                                                intent=["inform",
                                                        "user_ask_fees_date"])],
                "semester": [self.from_entity(entity="semester",
                                                intent=["inform",
                                                        "user_ask_fees_date"])],
                "graduate": [self.from_entity(entity="graduate",
                                                intent=["inform",
                                                        "user_ask_fees_date"])],
                "department_type": [self.from_entity(entity="department_type",
                                                  intent=["inform",
                                                          "user_ask_fees_date"])]}                                                    

    def submit(self, dispatcher, tracker, domain):
        date_ftype = tracker.get_slot('fees_type')
        date_sem = tracker.get_slot('semester')
        date_deptypee = tracker.get_slot('department_type')
        date_graduatee = tracker.get_slot('graduate')
        client = MongoClient('localhost', 27017)
        db = client.cmsbot
        table = db.fees_date_fine
        dates = table.find_one({"fees_type": date_ftype.strip(), "semester": date_sem.strip(),"department_type": date_deptypee.strip(),"graduate": date_graduatee.strip()})
        no = table.find({"fees_type": date_ftype.strip(), "semester": date_sem.strip(),"department_type": date_deptypee.strip(),"graduate": date_graduatee.strip()}).count()
        if no == 1:
            date = dates["last_date"]
            responseMsg =  """The last date for your fees submission without fine is {}.""".format(date)
        else:
            responseMsg = "i am afraid i dont have it"
        dispatcher.utter_message(responseMsg)
        return []


class FineAmountForm(FormAction):
    """fine amount"""

    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "fine_amount_form"

    @staticmethod
    def required_slots(tracker):
       # type: () -> List[Text]
        """A list of required slots that the form has to fill"""

        return ["fees_type", "semester", "graduate", "department_type"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"fees_type": [self.from_entity(entity="fees_type",
                                                intent=["inform",
                                                        "user_ask_about_fine_amount"])],
                "semester": [self.from_entity(entity="semester",
                                                intent=["inform",
                                                        "user_ask_about_fine_amount"])],
                "graduate": [self.from_entity(entity="graduate",
                                                intent=["inform",
                                                        "user_ask_about_fine_amount"])],
                "department_type": [self.from_entity(entity="department_type",
                                                  intent=["inform",
                                                          "user_ask_about_fine_amount"])]}                                                    

    def submit(self, dispatcher, tracker, domain):
        fine_ftype = tracker.get_slot('fees_type')
        fine_sem = tracker.get_slot('semester')
        fine_deptypee = tracker.get_slot('department_type')
        fine_graduatee = tracker.get_slot('graduate')
        client = MongoClient('localhost', 27017)
        db = client.cmsbot
        table = db.fees_date_fine
        fine = table.find_one({"fees_type": fine_ftype.strip(), "semester": fine_sem.strip(),"department_type": fine_deptypee.strip(),"graduate": fine_graduatee.strip()})
        no = table.find({"fees_type": fine_ftype.strip(), "semester": fine_sem.strip(),"department_type": fine_deptypee.strip(),"graduate": fine_graduatee.strip()}).count()
        if no == 1:
            fine_amount = fine["fine"]
            superfine_amount = fine["superfine"]
            responseMsg =  """Fine amount is {} and the superfine is {}.""".format(fine_amount,superfine_amount)
        else:
            responseMsg = "sorry it is available to me"    
        dispatcher.utter_message(responseMsg)
        return []


class OnlineFeesForm(FormAction):
    """Online payment"""

    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "online_fees_form"

    @staticmethod
    def required_slots(tracker):
       # type: () -> List[Text]
        return ["admission_no", "fees_type"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"admission_no": [self.from_entity(entity="admission_no",
                                                intent=["inform",
                                                        "user_want_to_pay_fees"])],
                "fees_type": [self.from_entity(entity="fees_type",
                                                intent=["inform",
                                                        "user_want_to_pay_fees"])]}   

    @staticmethod
    def fees_type_db():
        # type: () -> List[Text]
        """Database of supported fees types"""
        return ["exam",
                "semester",
                "supplementary"]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False
    

    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
            else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if not slot_values:
                # reject form action execution
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))

        # we'll check when validation failed in order
        # to add appropriate utterances
        for slot, value in slot_values.items():
            
            if slot == 'admission_no':
                if not self.is_int(value) or int(value) <= 999 or int(value) > 9999:
                    dispatcher.utter_template('utter_wrong_admission_no',
                                              tracker)
                    # validation failed, set slot to None
                    slot_values[slot] = None

        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]


    def submit(self, dispatcher, tracker, domain):
        """validate admission number 4 DIGITS"""
        global st_department
        st_department = ""
        global st_department_type
        st_department_type = ""
        global st_semester
        st_semester = ""
        global st_graduate,total_amount,req_id,response
        response = ""
        req_id = ""
        st_graduate = "" 
        total_amount = ""
        pay_admno = tracker.get_slot('admission_no') 
        api = Instamojo(api_key="test_e00bfc85a4af1fcf229cf6f1d59",auth_token="test_2842fb0ed18deb1950f61abbbeb" , endpoint="https://test.instamojo.com/api/1.1/")
        pay_feetype = tracker.get_slot('fees_type')
        client = MongoClient('localhost', 27017)
        db = client.cmsbot 
        table = db.student_info
        fees_table = db.fees_info
        fine_table = db.fees_date_fine
        payment_table = db.payment_fees
        student = table.find_one({"admission_no": pay_admno.strip()})
        no = table.find({"admission_no": pay_admno.strip()}).count()
        if no == 1:
            st_name = student["name"]
            st_graduate = student["graduate"]
            st_department = student["department"]
            st_department_type = student["department_type"]
            st_semester = student["semester"]
            fees_amount = fees_table.find_one({"fees_type": pay_feetype.strip(), "department_type": st_department_type.strip(), "semester": st_semester.strip(), "graduate": st_graduate.strip()})
            total_amount = fees_amount["fees_amount"]
            loc_fine = fine_table.find_one({"fees_type": pay_feetype.strip(), "department_type": st_department_type.strip(), "semester": st_semester.strip(), "graduate": st_graduate.strip()})
            today = date.today()
            current_date = today.strftime("%d/%m/%Y")
            current_date = datetime.strptime(current_date, '%d/%m/%Y')
            last_d = loc_fine["last_date"]
            last_date = datetime.strptime(last_d, '%d/%m/%Y')
            super_d = loc_fine["superfine_date"]
            super_date = datetime.strptime(super_d, '%d/%m/%Y')
            last_amount = loc_fine["fine"]
            super_amount = loc_fine["superfine"]
            if super_date <= current_date:
                total_amount = int(total_amount) + int(super_amount)
            elif current_date >= last_date:
                total_amount = int(total_amount) + int(last_amount)
            else:
                total_amount = int(total_amount) 
            response = api.payment_request_create(amount= total_amount, purpose=pay_feetype, send_email=True, email="foo@example.com", redirect_url= "http://localhost:3000/verify" )
            req_id =response['payment_request']['id']  
            validate = payment_table.find({"admission_no": pay_admno, "validatefees": "true", "fees_type": pay_feetype}).count()  
            responseMsg =  """Amount for payment is {} .[Make payment here]({})""".format(total_amount, response['payment_request']['longurl'])
            if validate == 1:
                responseMsg = "you have already paid your fees"
            else:
               
                payment_table.insert({"req_id": req_id, "admission_no": pay_admno, "name": st_name, "department": st_department, "department_type": st_department_type, " graduate": st_graduate, "fees_type": pay_feetype, "semester": st_semester, "amount_paid": total_amount, "validatefees": "false"})
        else:
            responseMsg = "invalid admission no" 
            
        dispatcher.utter_message(responseMsg)
        return []


class FeesAmountForm(FormAction):
    """Fees Amount Form"""

    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "fees_amount_form"

    @staticmethod
    def required_slots(tracker):
       # type: () -> List[Text]
        """A list of required slots that the form has to fill"""
        return ["fees_type", "semester", "department_type", "graduate"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"fees_type": [self.from_entity(entity="fees_type",
                                                intent=["inform",
                                                        "user_ask_fees_amount"])],
                "semester": [self.from_entity(entity="semester",
                                                intent=["inform",
                                                        "user_ask_fees_amount"])],
                "graduate": [self.from_entity(entity="graduate",
                                                intent=["inform",
                                                        "user_ask_fees_amount"])],
                "department_type": [self.from_entity(entity="department_type",
                                                  intent=["inform",
                                                          "user_ask_fees_amount"])]}                                                    

    def submit(self, dispatcher, tracker, domain):
        amount_feetype = tracker.get_slot('fees_type')
        amount_sem = tracker.get_slot('semester')
        amount_grad = tracker.get_slot('graduate')
        amount_deptype = tracker.get_slot('department_type')
        client = MongoClient('localhost', 27017)
        db = client.cmsbot 
        table = db.fees_info
        amount_fees = table.find_one({"fees_type": amount_feetype.strip(), "department_type": amount_deptype.strip(), "semester": amount_sem.strip(), "graduate": amount_grad.strip()})
        no = table.find({"fees_type": amount_feetype.strip(), "department_type": amount_deptype.strip(), "semester": amount_sem.strip(), "graduate": amount_grad.strip()}).count()
        if no == 1:
            amount = amount_fees["fees_amount"]
            responseMsg =  """The amount you need to pay is {}.""".format(amount)
        else:
            responseMsg = "sorry it is not available"
        dispatcher.utter_message(responseMsg)
        return []