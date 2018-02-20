# -*- coding: utf8 -*-

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from random import randint
from bs4 import BeautifulSoup
import logging
import urllib.request
import urllib.parse
import re
import simplejson
import requests
import re
import json
import math
import wolframalpha

wolframclient = wolframalpha.Client('V6HL75-H6WJWKPYEQ')

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')

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
    return starts[randint(1,len(starts))]
def randomreply():
    return replies[randint(1,len(replies))]
def videosearch(search):
	query_string = urllib.parse.urlencode({"search_query" : search})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	return("http://www.youtube.com/watch?v=" + search_results[0])
def imagesearch(search):
    search= search.split()
    search='+'.join(search)
    url="https://www.google.co.in/search?q="+search+"&source=lnms&tbm=isch"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header) 
    ActualImage=[]# contains the link for Large original image, type of image
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        ActualImage.append((link,Type))
        return(link)
def wolframexpression(expression):
	return wolframclient.query(expression)

updater = Updater(token='547982491:AAH9dUGZatOuFHiOsI9fg1rU1oSIJHxP-cw')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text= ramdomstart())
	updater.start_polling()

start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)

def kill(bot, update): 	
	bot.send_message(chat_id=update.message.chat_id, text= "infelizmente não sei como faz pra matar alguém")
	bot.send_message(chat_id=update.message.chat_id, text= "também não consigo nem me matar")
	bot.send_message(chat_id=update.message.chat_id, text= "que monstro criaria um ser que não consegue tirar a própria vida?")

kill_handler = CommandHandler('kill',kill)
dispatcher.add_handler(kill_handler)

def help(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text="/kill - matar")
	bot.send_message(chat_id=update.message.chat_id, text="/image - pesquisar imagem")
	bot.send_message(chat_id=update.message.chat_id, text="/video- pesquisar vídeo")
	bot.send_message(chat_id=update.message.chat_id, text="/wolfram - pesquisar qualquer coisa no wolfram")

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

def video(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text=videosearch((update.message.text).replace('/video ','')))

video_handler = CommandHandler('video', video)
dispatcher.add_handler(video_handler)

def image(bot, update): 
	bot.send_photo(chat_id=update.message.chat_id, photo=imagesearch((update.message.text).replace('/image ','')))

image_handler = CommandHandler('image', image)
dispatcher.add_handler(image_handler)

def wolfram(bot, update): 
    bot.send_message(chat_id=update.message.chat_id, text= next((wolframexpression((update.message.text).replace('/wolfram ',''))).results).text)

wolfram_handler = CommandHandler('wolfram', wolfram)
dispatcher.add_handler(wolfram_handler)

def echo(bot,update): 
	bot.send_message(chat_id=update.message.chat_id, text= randomreply())

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def unknown(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text="que porra de comando é esse? vai se foder")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)



updater.start_polling()