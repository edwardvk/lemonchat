# -*- coding: utf-8 -*-
import telegram
import sys
import setpath
import settings

bot = None

# Groups
alexgeneral = -208181084
nitrictest = -217625579
papervideo = -239300120
nitriccalls = -249242528
dramafactory = -267176353
securebooking = -286958904
papervideo = -313764144
lemongroup = -244798008

def connect():
    global bot
    try:
        bot = telegram.Bot(token=settings.doyatelegram)
    except:
        bot = None
connect()

def send(channel, text):
    if channel == "alexgeneral": channel = alexgeneral
    if channel == "papervideo": channel = papervideo
    if channel == "nitriccalls": channel = nitriccalls
    if channel == "dramafactory": channel = dramafactory
    if channel == "papervideo": channel = papervideo
    if channel == "lemongroup": channel = lemongroup
    if settings.testmode: channel = nitrictest
    global bot
    if not bot: connect()
    try:
        response = bot.sendMessage(channel, text, timeout=3)
    except:
        # Try resetting the connection...
        bot = telegram.Bot(token=settings.doyatelegram)
        response = bot.sendMessage(channel, text=text)
    return response['message_id']

def edit(channel, message_id, text):
    if channel == "alexgeneral": channel = alexgeneral
    if channel == "papervideo": channel = papervideo
    if channel == "nitriccalls": channel = nitriccalls    
    if channel == "dramafactory": channel = dramafactory   
    if channel == "papervideo": channel = papervideo   
    if channel == "lemongroup": channel = lemongroup      
    if settings.testmode: channel = nitrictest
    bot.editMessageText(chat_id=channel, message_id=message_id, text=text)

def append(channel, message_id, oldmessage, text):
    if channel == "alexgeneral": channel = alexgeneral
    if channel == "papervideo": channel = papervideo
    if channel == "nitriccalls": channel = nitriccalls    
    if channel == "dramafactory": channel = dramafactory  
    if channel == "papervideo": channel = papervideo
    if channel == "lemongroup": channel = lemongroup                  
    if settings.testmode: channel = nitrictest
    try:
        edit(channel, message_id, oldmessage+text)
        return message_id
    except:
        return send(channel, text)


if __name__ == '__main__':
    try:
        message_id = send(sys.argv[1], sys.stdin.read())
        exit()
    except:
        message = u'Test from Master Penné. Click here to respond. http://lemonchat.nitric.co.za/?user_id=Craig&agent=1\n'
        message_id = send('lemongroup', message)

    # for x in range(1000):
    #     appendtext = 'Added Text %s\n' % (x,) + ("X"*1000)
    #     print "last message:",message
    #     print "appendtext",appendtext
    #     new_message_id = append('@nitricincomingcalls', message_id, message, appendtext)
    #     print "new_message_id:",new_message_id
    #     if new_message_id == message_id:
    #         message += appendtext
    #     else:
    #         print "New because %s != %s" % (new_message_id, message_id)
    #         message_id = new_message_id
    #         message = appendtext
    #     print "message_id", message_id
