### FOODIE RESTAURANT BOT 

An Indian startup named 'Foodie' wants to build a conversational bot (chatbot) which can help users discover restaurants across several Indian cities. You have been hired as the lead data scientist for creating this product.

The main purpose of the bot is to help users discover restaurants quickly and efficiently and to provide a good restaurant discovery experience.


### DEPENDENCIES

- Python 3.6.5
- rasa-core 0.10.1
- rasa-nlu 0.12.3
(All depenedencies are listed in requirements.txt file)

### RUNNING THE BOT

### Train Rasa NLU
    $ python nlu_model.py

### Train Rasa Core
    $ python train_init.py

### Run Dialogue management model (Run bot from commandline)
    $ python dialogue_management_model.py


### SAMPLE CONVERSATION

* Hi
** hey there! How may i help you
* I’m hungry. Looking out for some good chinese restaurants in chandigarh
** Whats the average budget for two people?
1: Lesser than Rs. 300 (<300)
2: Rs. 300 to 700 (300-700)
3: More than 700 (>700)
* >700
** Searching top rated restaurants in your budget... 

******************************************************

The Great Bear in SCO 32, Madhya Marg, Sector 26, Chandigarh has been rated : 4.9/5
Average price for two: Rs.1600
Baithak in Chandigarh Haveli, Kalagram, Manimajra, Chandigarh has been rated : 4.8/5
Average price for two: Rs.1200
Beach N Brew in SCO 61, Sector 26, Chandigarh has been rated : 4.7/5
Average price for two: Rs.1800
Sector 7 Social in SCO 37, Madhya Marg, Sector 7, Chandigarh has been rated : 4.6/5
Average price for two: Rs.1400
Hops n Grains in SCO 358, Sector 9, Panchkula has been rated : 4.6/5
Average price for two: Rs.2100

******************************************************

Should I send you details of all the restaurants on email?
* yes please
To what email id should I send it to?
* rheasdaddycool@gmail.com
Sent. Thank you
* hey there!
Hey, How is it going. How May I help you Today
...
..
.


### INTEGRATION WITH SLACK

- Download ngrok (https://ngrok.com/download)

- Start the app locally
    $python run_app.py  

- Use ngrok to get a public url
    $ path_to_ngrok http <APP_PORT>

- Create a custom bot in slack 

- Provide the slackbot credentials in run_app.py file.

- Go to the bot in Slack and start conversing!


### AUTHORS

**- Arunima Dasgupta **
**- Lakshmi J **
**- Seema Gopalakrishnan **
**- Sumit Pandey ** 