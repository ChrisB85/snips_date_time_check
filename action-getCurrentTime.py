#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import mqtt_client

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    from datetime import datetime
    import random
    now = datetime.now()
    hour = now.hour
    min = now.minute
    
    hours = ['twelve', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven']
    ones = [' ', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tens = ['oh ', ' ', 'twenty-', 'thirty-', 'fourty-', 'fifty-']
    
    suffix = " AM"
    if hour > 11:
    	hour -= 12
    	suffix = " PM"
    
    minTens = min // 10
    minOnes = min % 10
    
    if min == 0:
    	minutes = ""
    elif min >= 10 and min < 20:
    	minutes = ones[int(min)]
    else:
    	minutes = tens[int(minTens)]
    	minutes += ones[int(minOnes)]
    
    intro = random.randint(0, 2)
    if intro == 0:
      result_sentence = "Jest "
    elif intro == 1:
      result_sentence = "Obecnie jest "
    elif intro == 2:
      result_sentence = " "
    
    result_sentence += datetime.now().strftime("%-H:%M")
#    result_sentence += hours[int(hour)]
#    result_sentence += " "
    
#    result_sentence += minutes
    
#    result_sentence += suffix 
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    


if __name__ == "__main__":
    with Hermes(mqtt_options = mqtt_client.get_mqtt_options()) as h:
        h.subscribe_intent("kblachowicz:getCurrentTime", subscribe_intent_callback) \
         .start()
