# -*- coding: utf8 -*-

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, InlineQueryHandler)
from telegram import InlineQueryResultArticle, InputTextMessageContent
from random import randint
from bs4 import BeautifulSoup
import logging
import urllib.request
import urllib.parse
import re
import sys
import simplejson
import requests
import json
import wolframalpha

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
	5:"quero morrer",
	6:"quié",
	7:"q q tu quer porra",
	8:"que foi desgraça",
	9:"me deixa em paz",
	10:"vai pra puta que te pariu",
	11:"caralho que chatice",
	12:"ai que ódio"
}

moreCounter = 0
lastQuery = ""
wolframclient = wolframalpha.Client('V6HL75-H6WJWKPYEQ')

def get_soup(url,header):
	return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')
def randomstart(): 
	return starts[randint(1,len(starts))]
def randomreply():
	return replies[randint(1,len(replies))]
def videosearch(search,i):
	query_string = urllib.parse.urlencode({"search_query" : search})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	return("http://www.youtube.com/watch?v=" + search_results[i])
def imagesearch(search,i):
	search= search.split()
	search='+'.join(search)
	url="https://www.google.co.in/search?q="+search+"&source=lnms&tbm=isch"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header) 
	ActualImage=[] #unused
	for a in soup.find_all("div",{"class":"rg_meta"}):
		link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
		ActualImage.append((link,Type)) #unused
		if(i==0): 
			return(link)
		else:
			i = i-1
def googlesearch(search,i):
	search= search.split()
	search='+'.join(search)
	url="https://www.google.co.in/search?q="+search+"&source=lnms"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header) 
	#_Rm is where the link is easier to get. It's the little green-coloured link in every result box.
	for a in soup.find_all("cite",{"class":"_Rm"}): 
		if(i==0): 
			return(a.text)
		else:
			i = i-1
def wolframexpression(expression):
	return wolframclient.query(expression)
def gifsearch(search,i):
	return

updater = Updater(token='547982491:AAH9dUGZatOuFHiOsI9fg1rU1oSIJHxP-cw')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text= randomstart())
	updater.start_polling()

dispatcher.add_handler(CommandHandler('start',start))

def kill(bot, update): 	
	bot.send_message(chat_id=update.message.chat_id, text= "infelizmente não sei como faz pra matar alguém")
	bot.send_message(chat_id=update.message.chat_id, text= "também não consigo nem me matar")
	bot.send_message(chat_id=update.message.chat_id, text= "que monstro criaria um ser que não consegue tirar a própria vida?")

dispatcher.add_handler(CommandHandler('kill',kill))

def help(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text="/kill - matar")
	bot.send_message(chat_id=update.message.chat_id, text="/image - pesquisar imagem")
	bot.send_message(chat_id=update.message.chat_id, text="/video - pesquisar vídeo")
	bot.send_message(chat_id=update.message.chat_id, text="/search - pesquisar no google")
	bot.send_message(chat_id=update.message.chat_id, text="/gif - pesquisar gif")
	bot.send_message(chat_id=update.message.chat_id, text="/more - ver próximo resultado depois de uma pesquisa de image, video, search ou gif")
	bot.send_message(chat_id=update.message.chat_id, text="/wolfram - pesquisar qualquer coisa no wolfram")

dispatcher.add_handler(CommandHandler('help', help))

def video(bot, update):
	global moreCounter
	moreCounter = 0
	global lastQuery
	lastQuery = update.message.text
	bot.send_message(chat_id=update.message.chat_id, text=videosearch(lastQuery.replace('/video ',''),moreCounter))

dispatcher.add_handler(CommandHandler('video', video))

def image(bot, update):
	global moreCounter
	moreCounter = 0
	global lastQuery
	lastQuery = update.message.text
	bot.send_photo(chat_id=update.message.chat_id, photo=imagesearch(lastQuery.replace('/image ',''),moreCounter))

dispatcher.add_handler(CommandHandler('image', image))

def google(bot, update):
	global moreCounter
	moreCounter = 0
	global lastQuery
	lastQuery = update.message.text
	bot.send_message(chat_id=update.message.chat_id, text=googlesearch(lastQuery.replace('/search ',''),moreCounter))

dispatcher.add_handler(CommandHandler('search', google))

def gif(bot, update):
	global moreCounter
	moreCounter = 0
	global lastQuery
	lastQuery = update.message.text
	bot.send_message(chat_id=update.message.chat_id, text=gifsearch(lastQuery.replace('/gif ',''),moreCounter))

dispatcher.add_handler(CommandHandler('gif', gif))

def wolfram(bot, update):
	response = wolframexpression(lastQuery.replace('/wolfram ',''))
	try:
		info = next(response.info).text
	except:
		info = ""
	try:
		results = next(response.results).text
	except:
		results = ""
	try:
		details = response.details
	except:
		details = ""
	
	if(info!="" and results!=""):
		if(info == results):
			bot.send_message(chat_id=update.message.chat_id, text= results)
		else:
			bot.send_message(chat_id=update.message.chat_id, text= info)   
			bot.send_message(chat_id=update.message.chat_id, text= results)
	else: 
		if(details != ""):
			for key,value in details.items():
				if(value!=None): 
					bot.send_message(chat_id=update.message.chat_id, text= key+": "+value)

dispatcher.add_handler(CommandHandler('wolfram', wolfram))

def more(bot,update):	
	if lastQuery == "":
		return
	global moreCounter
	query = lastQuery.split(' ',1)
	if (query[0] == "/video"):
		moreCounter += 1
		bot.send_message(chat_id=update.message.chat_id, text=videosearch(query[1],moreCounter))
	elif (query[0] == "/image"):
		moreCounter += 1
		bot.send_message(chat_id=update.message.chat_id, text=imagesearch(query[1],moreCounter))
	elif (query[0] == "/search"):
		moreCounter += 1
		bot.send_message(chat_id=update.message.chat_id, text=googlesearch(query[1],moreCounter))
	elif (query[0] == "/gif"):
		return

dispatcher.add_handler(CommandHandler('more', more))

def echo(bot,update): 
	bot.send_message(chat_id=update.message.chat_id, text= randomreply())

dispatcher.add_handler(MessageHandler(Filters.text, echo))

def unknown(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text="que porra de comando é esse? vai se foder")	

dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()