from flask import Flask, request, render_template, redirect
import telepot
import urllib3
#from nltk.chat.eliza import eliza_chatbot
#from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os, pyqrcode, base64
from cairosvg import svg2png

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

password = '[YOUR CUSTOM PASSWORD]'
addr = '[YOUR SITE ADDRESS]'
secret = "[UUID CODE]"
bot = telepot.Bot('[YOUR BOT CODE]')
bot.setWebhook("{}/{}".format(addr,secret), max_connections=1)

app = Flask(__name__)

app.config['MAX_CONTENT_PATH'] = 400000000

def makeqr(text):
    url1 = pyqrcode.create(text)
    url1.svg('qr.svg', scale=4)
    svg_code = open("qr.svg", 'rt').read()
    svg2png(bytestring=svg_code,write_to='/home/epfsbot/qr.png')
    return "OK"

@app.route('/')
def index():
    return redirect('/upload')

@app.route('/upload')
def dir_listing():
    abs_path = '/home/epfsbot/upload'
    files = os.listdir(abs_path)
    return render_template('index.html', files=files)

@app.route('/uploader' , methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save('/home/epfsbot/upload/' + f.filename)
        makeqr(f'{addr}/upload/{f.filename}')
        imgfile=base64.b64encode(open("/home/epfsbot/qr.png","rb").read()).decode('ascii')
        return "<!DOCTYPE htm><html><head><title>epfsbot file link</title><meta name='viewport' content='width=device-width, initial-scale=1.0' ></head><body><center><img src='data:image/svg+xml;base64,{}' /></center></body></html>".format(imgfile)


@app.route('/del/<paswd>')
def deleteFolder(paswd):
    abs_path = '/home/epfsbot/upload'
    files = os.listdir(abs_path)
    if paswd == password :
        for file in files:
            os.remove('/home/epfsbot/upload/' + file)
    return render_template('index.html')

@app.route('/qr/<text>')
def showqr(text):
    makeqr(f'{addr}/upload/{text}')
    imgfile=base64.b64encode(open("/home/epfsbot/qr.png","rb").read()).decode('ascii')
    return "<!DOCTYPE htm><html><head><title>epfsbot file link</title><meta name='viewport' content='width=device-width, initial-scale=1.0' ></head><body><center><img src='data:image/svg+xml;base64,{}' /></center></body></html>".format(imgfile)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        file_name = update["message"]["date"]
        #bot.sendMessage(chat_id, update )

        if "text" in update["message"]:
            text = update["message"]["text"]
            if text == "/start":
                #keyboard=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="First Button",callback_data="yes")]])
                keyboard = {'keyboard': [['/start']]}
                bot.sendMessage(chat_id, f'<a href="{addr}/upload">Open shared file site</a>', reply_markup = keyboard, parse_mode = 'html')
                #bot.sendPhoto(chat_id, open("/home/epfsbot/upload//qr.png","rb"))

            else:
                #if "caption" in update["message"]:
                #    file_name = update["message"]["caption"]
                f=open('/home/epfsbot/upload/{}.txt'.format(file_name),'w')
                f.write(update["message"]["text"])
                f.close()
                bot.sendMessage(chat_id,'{}/upload/{}.txt'.format(addr , file_name))
                makeqr('{}/upload/{}.txt'.format(addr, file_name))
                bot.sendPhoto(chat_id, open("/home/epfsbot/qr.png","rb"))
                #bot.sendMessage(chat_id, eliza_chatbot.respond(text))

        if "photo" in update["message"]:
            bot.download_file(update["message"]['photo'][-1]['file_id'], 'upload/{}'.format(update["message"]['photo'][-1]['file_unique_id']))
            bot.sendMessage(chat_id, '<a href="{}/upload/{}">photo uploaded!</a>'.format(addr , update["message"]['photo'][-1]['file_unique_id']), parse_mode = 'html')
            makeqr('{}/upload/{}'.format(addr, update["message"]['photo'][-1]['file_unique_id']))
            bot.sendPhoto(chat_id, open("/home/epfsbot/qr.png","rb"))

        if "document" in update["message"]:
            bot.download_file(update["message"]['document']['file_id'], 'upload/{}'.format(update["message"]['document']['file_name']))
            bot.sendMessage(chat_id, '<a href="{}/upload/{}">document uploaded!</a>'.format(addr, update["message"]['document']['file_name']), parse_mode = 'html')
            makeqr('{}/upload/{}'.format(addr, update["message"]['document']['file_name']))
            bot.sendPhoto(chat_id, open("/home/epfsbot/qr.png","rb"))

        if "video" in update["message"]:
            bot.download_file(update["message"]['video']['file_id'], 'upload/{}'.format(update["message"]['video']['file_unique_id']))
            bot.sendMessage(chat_id, '<a href="{}/upload/{}">video uploaded!</a>'.format(addr, update["message"]['video']['file_unique_id']), parse_mode = 'html')
            makeqr('{}/upload/{}'.format(addr, update["message"]['video']['file_unique_id']))
            bot.sendPhoto(chat_id, open("/home/epfsbot/qr.png","rb"))

        if "audio" in update["message"]:
            bot.download_file(update["message"]['audio']['file_id'], 'upload/{}'.format(update["message"]['audio']['file_unique_id']))
            bot.sendMessage(chat_id, '<a href="{}/upload/{}">audio uploaded!</a>'.format(addr, update["message"]['audio']['file_unique_id']), parse_mode = 'html')
            makeqr('{}/upload/{}'.format(addr, update["message"]['audio']['file_unique_id']))
            bot.sendPhoto(chat_id, open("/home/epfsbot/qr.png","rb"))

        if "voice" in update["message"]:
            bot.download_file(update["message"]['voice']['file_id'], 'upload/{}'.format(update["message"]['voice']['file_unique_id']))
            bot.sendMessage(chat_id, '<a href="{}/upload/{}">voice uploaded!</a>'.format(addr, update["message"]['voice']['file_unique_id']), parse_mode = 'html')
            makeqr('{}/upload/{}'.format(addr, update["message"]['voice']['file_unique_id']))
            bot.sendPhoto(chat_id, open("/home/epfsbot/qr.png","rb"))

        if "video_note" in update["message"]:
            bot.download_file(update["message"]['video_note']['file_id'], 'upload/{}'.format(update["message"]['video_note']['file_unique_id']))
            bot.sendMessage(chat_id, '<a href="{}/upload/{}">video_note uploaded!</a>'.format(addr, update["message"]['video_note']['file_unique_id']), parse_mode = 'html')
            makeqr('{}/upload/{}'.format(addr, update["message"]['video_note']['file_unique_id']))
            bot.sendPhoto(chat_id, open("/home/epfsbot/qr.png","rb"))

        if "location" in update["message"]:
            f=open('/home/epfsbot/upload/{}.loc'.format(update["message"]["date"]),'w')
            f.write(str(update["message"]["location"]))
            f.close()
            bot.sendMessage(chat_id,'<a href="{}/upload/{}.loc">location uploaded!</a>'.format(addr, update["message"]["date"]), parse_mode = 'html')
            makeqr('{}/upload/{}.loc'.format(addr, update["message"]["date"]))
            bot.sendPhoto(chat_id, open("/home/epfsbot/qr.png","rb"))

        if "contact" in update["message"]:
            f=open('/home/epfsbot/upload/{}.vcard'.format(update["message"]["date"]),'w')
            f.write(str(update["message"]["contact"]))
            f.close()
            bot.sendMessage(chat_id,'<a href="{}/upload/{}.vcard">contact uploaded!</a>'.format(addr, update["message"]["date"]), parse_mode = 'html')
            makeqr('{}/upload/{}.vcard'.format(addr, update["message"]["date"]))
            bot.sendPhoto(chat_id, open("/home/epfsbot/qr.png","rb"))

    return "OK"
