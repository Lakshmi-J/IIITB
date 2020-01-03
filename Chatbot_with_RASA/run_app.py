from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput('xoxp-699601522772-688663128386-702269246934-b05e83301921bed96d920480e709e195', #app verification token
							'xoxb-699601522772-693780963457-JlhlxtFS7L5Vd8z8fvVLUyxy', # bot verification token
							'br1Mk8Ze6YnQCqgikfwQwSqq', # slack verification token
							True)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))



