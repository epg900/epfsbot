from flask import Flask, request, render_template, redirect
import telepot
import urllib3
#from nltk.chat.eliza import eliza_chatbot
#from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os, pyqrcode
from cairosvg import svg2png

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "[any UUID]"
bot = telepot.Bot('[Your telegram Bot code]')
bot.setWebhook("[your python flask supported site address]/{}".format(secret), max_connections=1)

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/upload')

@app.route('/upload')
def dir_listing():
    abs_path = '/home/epfsbot/upload'
    files = os.listdir(abs_path)
    return render_template('index.html', files=files)

@app.route('/qr/<text>')
def getqr(text):
    url1 = pyqrcode.create('{your site address]upload/{}'.format(text))
    url1.svg('qr.svg', scale=8)
    svg_code = open("qr.svg", 'rt').read()
    svg2png(bytestring=svg_code,write_to='/home/epfsbot/upload/qr.png')
    return redirect('{your site address]upload/qr.png')


@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        #bot.sendMessage(chat_id, update )

        if "text" in update["message"]:
            text = update["message"]["text"]
            if text == "/start":
                bot.sendMessage(chat_id, "touch below link to view uploaded file:\n{your site address]upload" )
            else:
                f=open('/home/epfsbot/upload/{}.txt'.format(update["message"]["date"]),'w')
                f.write(update["message"]["text"])
                f.close()
                bot.sendMessage(chat_id,'{your site address]upload/{}.txt'.format(update["message"]["date"]))
                #bot.sendMessage(chat_id, eliza_chatbot.respond(text))

        if "photo" in update["message"]:
            bot.download_file(update["message"]['photo'][-1]['file_id'], 'upload/{}'.format(update["message"]['photo'][-1]['file_unique_id']))
            bot.sendMessage(chat_id, "photo uploaded! \n{your site address]upload/{}".format(update["message"]['photo'][-1]['file_unique_id']) )

        if "document" in update["message"]:
            bot.download_file(update["message"]['document']['file_id'], 'upload/{}'.format(update["message"]['document']['file_name']))
            bot.sendMessage(chat_id, "file uploaded! \n{your site address]upload/{}".format(update["message"]['document']['file_name']) )

        if "video" in update["message"]:
            bot.download_file(update["message"]['video']['file_id'], 'upload/{}'.format(update["message"]['video']['file_unique_id']))
            bot.sendMessage(chat_id, "video uploaded! \n{your site address]upload/{}".format(update["message"]['video']['file_unique_id']) )

        if "audio" in update["message"]:
            bot.download_file(update["message"]['audio']['file_id'], 'upload/{}'.format(update["message"]['audio']['file_unique_id']))
            bot.sendMessage(chat_id, "audio uploaded! \n{your site address]upload/{}".format(update["message"]['audio']['file_unique_id']) )

        if "voice" in update["message"]:
            bot.download_file(update["message"]['voice']['file_id'], 'upload/{}'.format(update["message"]['voice']['file_unique_id']))
            bot.sendMessage(chat_id, "voice uploaded! \n{your site address]upload/{}".format(update["message"]['voice']['file_unique_id']) )

        if "video_note" in update["message"]:
            bot.download_file(update["message"]['video_note']['file_id'], 'upload/{}'.format(update["message"]['video_note']['file_unique_id']))
            bot.sendMessage(chat_id, "video_note uploaded! \n{your site address]upload/{}".format(update["message"]['video_note']['file_unique_id']) )

        if "location" in update["message"]:
            f=open('/home/epfsbot/upload/{}.loc'.format(update["message"]["date"]),'w')
            f.write(str(update["message"]["location"]))
            f.close()
            bot.sendMessage(chat_id,'{your site address]upload/{}.loc'.format(update["message"]["date"]))

        if "contact" in update["message"]:
            f=open('/home/epfsbot/upload/{}.vcard'.format(update["message"]["date"]),'w')
            f.write(str(update["message"]["contact"]))
            f.close()
            bot.sendMessage(chat_id,'{your site address]upload/{}.vcard'.format(update["message"]["date"]))


    return "OK"
