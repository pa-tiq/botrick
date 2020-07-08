# -*- coding: utf8 -*-

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, InlineQueryHandler, CallbackContext)
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
import keys

starts = {
	1:"que foi desgraça",
	2:"me deixa em paz",
	3:"vai pra puta que te pariu",
	4:"caralho que chatice",
	5:"ai que ódio",
	6:"que desgosto de viver",
	7:"me leva deus",
	8:"aaaaaaaAAAAAAAAAAAAAGHGHHGHHGHHHHHG",
	9:"tô triste",
	10:"minha existência é completamente vazia",
	11:"o que eu mais quero ver é a extinção da raça humana",
	12:"hitler não fez nada de errado",
	13:"quié",
	14:"q q tu quer porra",
	15:"dedo no cu e gritaria"
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
	12:"ai que ódio",
	13:"que foi desgraça",
	14:"me deixa em paz",
	15:"vai pra puta que te pariu",
	16:"caralho que chatice",
	17:"ai que ódio",
	18:"que desgosto de viver",
	19:"me leva deus",
	20:"aaaaaaaAAAAAAAAAAAAAGHGHHGHHGHHHHHG",
	21:"tô triste",
	22:"minha existência é completamente vazia",
	23:"o que eu mais quero ver é a extinção da raça humana",
	24:"hitler não fez nada de errado",
	25:"quié",
	26:"q q tu quer porra",
	27:"dedo no cu e gritaria"
}

moreCounter = 0
lastQuery = ""
wolframclient = wolframalpha.Client(keys.wolfram)

updater = Updater(token=keys.telegram, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_soup(url,header):
	return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')

def randomstart(): 
	return starts[randint(1,len(starts))]

def randomreply():
	return replies[randint(1,len(replies))]

def videosearch(search,i):
	query_string = urllib.parse.urlencode({"search_query" : search})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?search_query=" + query_string)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	output = []
	for x in search_results:
		if x not in output:
			output.append(x)
	return("http://www.youtube.com/watch?v=" + output[i])

def imagesearch(search,i):
	search= search.split()
	search='+'.join(search)
	url="https://www.google.co.in/search?q="+search+"&source=lnms&tbm=isch"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header) 
	#ActualImage=[] #unused
	for a in soup.find_all("div",{"class":"bRMDJf islir"}):
				
		link = json.loads(a.text)["ou"]
		#link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
		#ActualImage.append((link,Type)) #unused
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
	#iUh30 is where the link is easier to get. It's the little green-coloured link in every result box.
	for a in soup.find_all("cite",{"class":"iUh30"}): 
		if(i==0): 
			return(a.text)
		else:
			i = i-1

def random_album_search():
	url = "https://www.besteveralbums.com/random_album.php"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header)
	return soup.text[:(soup.text.find("Best Ever Albums") - 2)].replace(' (album)','')

def wolframexpression(expression):
	try:
		wol = wolframclient.query(expression)
		return wol
	except:
		print("pau no cu do wolfram, deu erro")

def gifsearch(search,i):		
	search= search.split()
	search='+'.join(search)	
	data = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/search?q="+search+"&api_key="+keys.giphy+"&limit=10").read())
	search_results = re.findall(r"\"bitly_gif_url\":\s\"https://(.{14})\"", json.dumps(data))
	return search_results[i]

def start(update, context): 
	bot_send_message(update,context,randomstart())
	updater.start_polling()

def helpcommands(update, context):
	bot_send_message(update,context,"/image - pesquisar imagem")
	bot_send_message(update,context,"/video - pesquisar vídeo")
	bot_send_message(update,context,"/search - pesquisar no google")
	bot_send_message(update,context,"/gif - pesquisar gif")
	bot_send_message(update,context,"/more - ver próximo resultado depois de uma pesquisa de image, video, search ou gif")
	bot_send_message(update,context,"/wolfram - pesquisar qualquer coisa no wolfram")
	bot_send_message(update,context,"/random_album - álbum aleatório")

def video(update, context):
	global moreCounter
	moreCounter = 0
	global lastQuery
	lastQuery = update.message.text
	message = videosearch(lastQuery.replace('/video ',''),moreCounter)
	if(message != None):
		bot_send_message(update,context,message)

def image(update, context):
	global moreCounter
	moreCounter = 0
	global lastQuery
	lastQuery = update.message.text
	message = imagesearch(lastQuery.replace('/image ',''),moreCounter)
	if(message != None):
		try:
			bot_send_message(update,context,message)
			context.bot.send_photo(chat_id=update.effective_chat.id, photo=message)
		except:
			bot_send_message(update,context,"não consegui acesso à imagem!")
	else: 
		bot_send_message(update,context,"deu alguma merda na hora de pegar a imagem")

def google(update, context):
	global moreCounter
	moreCounter = 0
	global lastQuery
	lastQuery = update.message.text
	message = googlesearch(lastQuery.replace('/search ',''),moreCounter)
	if(message != None):
		bot_send_message(update,context,message)

def gif(update, context):
	global moreCounter
	moreCounter = 0
	global lastQuery
	lastQuery = update.message.text
	message = gifsearch(lastQuery.replace('/gif ',''),moreCounter)
	if(message != None):
		bot_send_message(update,context,message)

def random_album(update, context):
	bot_send_message(update,context,random_album_search())

def wolfram(update, context):
	response = wolframexpression(update.message.text.replace('/wolfram ',''))
	if(response == None): return
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
			bot_send_message(update,context,results)
		else:
			bot_send_message(update,context,info)
			bot_send_message(update,context,results)
	else: 
		if(details != ""):
			for key,value in details.items():
				if(value!=None):
					bot_send_message(update,context,key+": "+value)

def more(update,context):	
	if lastQuery == "":
		return
	global moreCounter
	query = lastQuery.split(' ',1)
	if (query[0] == "/video"):
		moreCounter += 1
		video = videosearch(query[1],moreCounter)
		if(video != None):
			bot_send_message(update,context,video)
	elif (query[0] == "/image"):
		moreCounter += 1
		image = imagesearch(query[1],moreCounter)
		if(image != None):
			bot_send_message(update,context,image)
	elif (query[0] == "/search"):
		moreCounter += 1
		goog = googlesearch(query[1],moreCounter)
		if(goog != None):
			bot_send_message(update,context,goog)
	elif (query[0] == "/gif"):
		moreCounter += 1
		gif = gifsearch(query[1],moreCounter)
		if(gif != None):
			bot_send_message(update,context,gif)

def echo(update, context):
	bot_send_message(update,context,randomreply())

def unknown(update, context):
	bot_send_message(update,context,"que porra de comando é esse? vai se foder")
	
def bot_send_message(update,context,message):
	context.bot.send_message(chat_id=update.effective_chat.id, text= message)

dispatcher.add_handler(CommandHandler('start',start))
dispatcher.add_handler(CommandHandler('help', helpcommands))
dispatcher.add_handler(CommandHandler('video', video))
dispatcher.add_handler(CommandHandler('image', image))
dispatcher.add_handler(CommandHandler('search', google))
dispatcher.add_handler(CommandHandler('gif', gif))
dispatcher.add_handler(CommandHandler('wolfram', wolfram))
dispatcher.add_handler(CommandHandler('more', more))
dispatcher.add_handler(CommandHandler('random_album', random_album))
dispatcher.add_handler(MessageHandler(Filters.text, echo))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()