#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

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
    now = datetime.now()
    
    ordinals = ['ith', 'pierwszy', 'drugi', 'trzeci', 'czwarty', 'piąty', 'szósty', 'siódmy', 'ósmy', 'dziewiąty', 'dziesiąty', 'jedenasty', 'dwunasty', 'trzynasty', 'czternasty', 'piętnasty', 'szasnasty', 'siedemnasty', 'osiemnasty', 'dziewiętnasty']
    tens = ['dwudzisty-', 'trzydziesty-']
    
    day = now.day
    dayTens = day // 10
    dayOnes = day % 10
    
    if day < 20:
    	dateStr = ordinals[int(day)]
    else:
    	dateStr = tens[int(dayTens) - 2]
    	dateStr += ordinals[int(dayOnes)]
    
    result_sentence = now.strftime("Dziś jest %d.%m.%Y")
#    result_sentence += str(day)
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    
    


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("kblachowicz:getCurrentDate", subscribe_intent_callback) \
         .start()
