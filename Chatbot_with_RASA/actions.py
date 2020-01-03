from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from rasa_core.events import AllSlotsReset
from rasa_core.events import Restarted

import zomatopy
import json
import smtplib

from string import Template
# Import the email modules we'll need
from email.message import EmailMessage

import warnings
warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

MY_ADDRESS = 'rheadasgupta5@gmail.com' 					#Google account username for sending out emails
PASSWORD = 'Salesforce5'               					#Google account username for sending out emails

list_of_restaurants = "" 		        				#variable that stores the list of restaurants to be emailed to user

config={ "user_key":"b07f75f5777dc589d7261785d56a8faf"} #Zomato config

valid_tier_cities = ["Bangalore","Chennai", "Delhi", "Hyderabad","Kolkata", "Mumbai","Lucknow",
					"Agra","Ajmer","Aligarh","Amravati","Amritsar","Asansol","Aurangabad", "Ahmedabad","Allahabad",
					"Bareilly","Belgaum","Bhavnagar","Bhiwandi","Bhopal","Bhubaneswar",
					"Bikaner","Bokaro Steel City","Chandigarh","Coimbatore","Nagpur","Cuttack","Dehradun",
					"Dhanbad","Durg-Bhilai Nagar","Durgapur","Erode","Faridabad","Firozabad","Ghaziabad",
					"Gorakhpur","Gulbarga","Gwalior","Guntur","Gurgaon","Guwahati","Hubli-Dharwad",
					"Indore","Jabalpur","Jaipur","Jalandhar","Jammu","Jamnagar","Jamshedpur","Jhansi","Jodhpur",
					"Kannur","Kanpur","Kakinada","Kochi","Kottayam","Kolhapur","Kollam","Kota","Kozhikode","Kurnool","Ludhiana",
					"Madurai","Malappuram","Mathura","Goa","Mangalore","Meerut","Moradabad","Mysore",
					"Nanded","Nashik","Nellore","Noida","Palakkad","Patna","Pondicherry","Raipur","Rajkot",
					"Rajahmundry","Ranchi","Rourkela","Salem","Sangli","Siliguri","Solapur","Srinagar",
					"Sultanpur","Surat","Thiruvananthapuram","Thrissur","Tiruchirappalli","Tirunelveli","Tiruppur",
					"Ujjain","Vijayapura","Vadodara","Varanasi","Pune",
					"Vasai-Virar City","Vijayawada","Visakhapatnam","Warangal"]



valid_tier_cities = [x.lower() for x in valid_tier_cities]

# Check if the city specified is within the area of operation (tier1 and tier 2 cities only)
class ActionValidateLocation(Action):
	def name(self):
		return 'action_check_city_tier'

	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('location')
		city = str(loc)
		#print(city)
		try:
			
			
			if city.lower() in valid_tier_cities:
				return [SlotSet('valid_location',"yes")]

			else:
				zomato = zomatopy.initialize_app(config)
				results = zomato.get_city_ID(city)
				#print('---Location not covered-----')
				dispatcher.utter_template("utter_location_not_operable", tracker)
				
				#dispatcher.utter_template("utter_did_not_understand", tracker)
				#tracker.trigger_follow_up_action(self.try_again)

				#return [SlotSet('valid_location',"no")]
				return[Restarted()] 
				
		# For invalid city names, the code will fall in this exception block
		except:
				
				#dispatcher.utter_template("utter_did_not_understand", tracker)
				('***** Exception ******')
				dispatcher.utter_message("Sorry, didn’t find any such location. Can you please try again?")
				#tracker.trigger_follow_up_action(ActionListen)
	
				
				return[Restarted()] 
	

# Search restaurants as per user location, cuisine and price preference
class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'

	# Retrieve restaurants that match user budget range 
	def searchRestaurantsByUserFilters(self, user_price_range, restaurants):
		try:
			#print("Filter restaurants")
			price_min = 0
			price_max = 10000
			response = ""
			global list_of_restaurants
			count = 0
		

			#Check user budget
			if user_price_range.isdigit():
				#print('--User entered choice in digit---')
				choice = int(user_price_range)
				#print(choice)
				if choice == 1:
					price_max = 300

				elif choice == 2:
					price_min = 300
					price_max = 700

				else:
					price_min = 700
			else:
				#print('--cuisine range given')
				#print(user_price_range)
				if user_price_range == "<300":
					price_max = 300
					
				elif user_price_range == "300-700":
						price_min = 300
						price_max = 700
				else:
					price_min = 700

			#print(price_min)
			#print(price_max)

			for restaurant in restaurants:
				
				res = restaurant['restaurant']['name'] + " in " + restaurant['restaurant']['location']['address'] + " has been rated : " +  restaurant['restaurant']['user_rating']['aggregate_rating'] + "/5" +"\n"
				res = res + "Average price for two: " + restaurant['restaurant']['currency'] + str(restaurant['restaurant']['average_cost_for_two'])
			
				average_cost_for_two = restaurant['restaurant']['average_cost_for_two']
				
				#Filter restaurants by user sepcified price range
				if average_cost_for_two >= price_min and average_cost_for_two <= price_max:
					
					# Top 5 restaurants to be shown to the user
					if(count < 5):
						response += res + "\n"
					
					# Top 10 restaurants to be emailed to the user (if user wishes)
					if(count < 10):
						list_of_restaurants += res + "\n"

					count += 1 
					
			if response == "":
				response = "Sorry, I could not find any restaurants matching your search criteria :( \n"
			
			#print(response)
			return response
		except:
			#print('Exception!!!!!')
			return[Restarted()]
		
	def run(self, dispatcher, tracker, domain):
		try:
			zomato = zomatopy.initialize_app(config)
			loc = tracker.get_slot('location')
			cuisine = tracker.get_slot('cuisine')
			price = tracker.get_slot('price')

			#print(loc)
			#print(cuisine)
			#print(price)

			# If price not entered by user, set it to moderate range (300-700)
			if price==None:
				price="300-700"

			#print(price)

			cuisines_dict={
				'chinese':25,
				'mexican':73,
				'italian':55,
				'american':1,
				'south indian':85,
				'north indian':50	
			}

			location_detail=zomato.get_location(loc, 1)
			d1 = json.loads(location_detail)
			lat=d1["location_suggestions"][0]["latitude"]
			lon=d1["location_suggestions"][0]["longitude"]

			
			results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 30)
			d = json.loads(results)
			response=""
			#print(d)
			#print(d['results_found'])
			
			if d['results_found'] == 0:
				
				response = "Sorry, I could not find any restaurants matching your search criteria :( " +"\n" + "Want to give it another try?\n"
				dispatcher.utter_message(str(response))
				dispatcher.utter_template("utter_goodbye", tracker)
				#return [AllSlotsReset()]
				
				return[Restarted()] 
			else:
				restaurants = d['restaurants'];
				response = self.searchRestaurantsByUserFilters(price, d['restaurants'])
				dispatcher.utter_message("Searching top rated restaurants in your budget... \n")
				dispatcher.utter_message("******************************************************\n")
				dispatcher.utter_message(str(response))
				dispatcher.utter_message("******************************************************\n")
				return [SlotSet('location',loc)]
		
		except:
			#print('----Exception in run--')
			dispatcher.utter_message("Oops, looks like there is some error in fetching details. Sorry!")
			dispatcher.utter_template("utter_goodbye", tracker)
			return[Restarted()] 
		
		#return [SlotSet('location',loc)]

# Send email to user with top 10 restaurants matching his/her search criteria
class ActionSendEmail(Action):
	def name(self):
		return 'action_sendemail'
		
	def run(self, dispatcher, tracker, domain):
		global list_of_restaurants
		
		
		try:
			
			email = tracker.get_slot('emailid')
			#print(email)
			if list_of_restaurants!="":
				
				email_text = 'Please find the requested restaurant details: \n'
				email_text += '------------------------------------------------\n'
				email_text += list_of_restaurants
			else:
				email_text = 'Sorry, I could not find any restaurants matching your search criteria :( \n'

			
			msg = EmailMessage()
			
			msg['Subject'] = 'Restaurant Details by Foodie!'
			msg['From'] = MY_ADDRESS
	
			msg['To'] = email;
			msg.set_content(email_text)

			# set up the SMTP server
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(MY_ADDRESS, PASSWORD)
			server.send_message(msg)
			server.close()

			#print('Email sent!')
			list_of_restaurants = ""
			dispatcher.utter_template("utter_emailsent", tracker)
		except:
			#print('Exception!!!')
			list_of_restaurants = ""
			dispatcher.utter_message("Oops, looks like the email couldn't go through. Sorry!")
			dispatcher.utter_template("utter_goodbye", tracker)
			return[Restarted()] 
			
		
		
		return [AllSlotsReset()]


		
class ActionRestarted(Action): 	
	def name(self):
		return 'action_restarted'
	def run(self, dispatcher, tracker, domain):
		
		return[Restarted()] 

class ActionSlotReset(Action): 
	def name(self): 
		return 'action_slot_reset' 
	def run(self, dispatcher, tracker, domain): 
		return[AllSlotsReset()]
