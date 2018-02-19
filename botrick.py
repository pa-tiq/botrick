# -*- coding: utf8 -*-

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from random import randint
import logging
import urllib.request
import urllib.parse
import re
import simplejson
import io

from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')


query = raw_input("query image")# you can change the query for the image  here
image_type="ActiOn"
query= query.split()
query='+'.join(query)
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
print url
#add the directory for your image here
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url,header)


ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print  "there are total" , len(ActualImages),"images"

if not os.path.exists(DIR):
            os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
            os.mkdir(DIR)
###print images
for i , (img , Type) in enumerate( ActualImages):
    try:
        req = urllib2.Request(img, headers={'User-Agent' : header})
        raw_img = urllib2.urlopen(req).read()

        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print cntr
        if len(Type)==0:
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


        f.write(raw_img)
        f.close()
    except Exception as e:
        print "could not load : "+img
        print e


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
    fetcher = urllib.request.build_opener()
    startIndex = "0"
    searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + search + "&start=" + startIndex
    print(searchUrl)
    f = fetcher.open(searchUrl)
    deserialized_output = simplejson.load(f)
    imageUrl = deserialized_output['responseData']['results'][0]['unescapedUrl']
    file = io.StringIO(urllib.request.urlopen(imageUrl).read())
    return(file)

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

def video(bot, update): 
	bot.send_message(chat_id=update.message.chat_id, text=videosearch(update.message.text))
	print(Filters.text)

video_handler = CommandHandler('video', video)
dispatcher.add_handler(video_handler)

def image(bot, update): 
	bot.send_photo(chat_id=update.message.chat_id, file=imagesearch(update.message.text))
	print(Filters.text)

image_handler = CommandHandler('image', image)
dispatcher.add_handler(image_handler)

def echo(bot,update): bot.send_message(chat_id=update.message.chat_id, text= randomreply())

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def unknown(bot, update): bot.send_message(chat_id=update.message.chat_id, text="que porra de comando é esse? vai se foder")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()