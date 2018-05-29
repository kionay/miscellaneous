# requires: python3
#           discord.py
#               requires the 'rewrite' branch on github here:
#                   https://github.com/Rapptz/discord.py/tree/rewrite
#                   recommended installation: download as zip, unpack to selected folder, cd to directory with setup.py
#                       sudo -H pip3 install -e . --upgrade
#
#           aiohttp     (pip3 install aiohttp)
#               if aiohttp is already installed make sure it's up to date (pip3 install aiohttp --upgrade)
#

from discord import Webhook, AsyncWebhookAdapter
from aiohttp import web

webhook_url = "{webhook URL as provided by Discord}"

routes = web.RouteTableDef()

@routes.get('/')
@routes.get('/{SDSUpdate}')
async def SDSUpdate(request):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session)) 
        if not request.match_info:
            return web.Response(status=400)
        await webhook.send(request.match_info['SDSUpdate'])
        return web.Response(text="sent successfully")


app = web.Application()
app.router.add_routes(routes)
web.run_app(app,port=8082)
