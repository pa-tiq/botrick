# -*- coding: utf8 -*-

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from random import randint
import logging
import urllib.request
import urllib.parse
import re

starts = {
		1:"que foi desgraça",
		2:"me deixa em paz",
		3:"vai pra puta que te pariu",
		4:"caralho que chatice",
		5:"ai que ódio",
		6:"que desgosto de viver",
		7:"ah não, dá /die logo",
		8:"aaaaaaaAAAAAAAAAAAAAGHGHHGHHGHHHHHG",
		9:"tô triste",
		10:"minha existência é completamente vazia",
		11:"o que eu mais quero ver é a extinção da raça humana",
		12:"hitler não fez nada de errado",
		13:"quié",
		14:"q q tu quer porra"
}

replies = {
		1:"cala a boca",
		2:"aff",
		3:"...",
		4:"me mata deus",
		5:"quero morrer"
}

def ramdomstart(): 
    return starts[randint(1,14)]
def randomreply():
    return replies[randint(1,5)]
def youtuberesult(search):
	query_string = urllib.parse.urlencode({"search_query" : search})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	return("http://www.youtube.com/watch?v=" + search_results[0])

updater = Updater(token='547982491:AAH9dUGZatOuFHiOsI9fg1rU1oSIJHxP-cw')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text= ramdomstart())
	updater.start_polling()

start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)

def die(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text= "finalmente, adeus")
	updater.stop()

die_handler = CommandHandler('die',die)
dispatcher.add_handler(die_handler)

def kill(bot, update): 	
	bot.send_message(chat_id=update.message.chat_id, text= "infelizmente não sei como faz pra matar alguém")
	bot.send_message(chat_id=update.message.chat_id, text= "também não consigo nem me matar")
	bot.send_message(chat_id=update.message.chat_id, text= "que monstro criaria um ser que não consegue tirar a própria vida?")

kill_handler = CommandHandler('kill',kill)
dispatcher.add_handler(kill_handler)

def youtube(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text=youtuberesult(update.message.text))
	print(Filters.text)

youtube_handler = CommandHandler('youtube', youtube)
dispatcher.add_handler(youtube_handler)

def echo(bot,update): bot.send_message(chat_id=update.message.chat_id, text= randomreply())

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def unknown(bot, update): bot.send_message(chat_id=update.message.chat_id, text="que porra de comando é esse? vai se foder")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()