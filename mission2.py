from aiohttp import web
from main import API
import os

# constant to get cross-platform relational path to the file
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# create API class instance and again get games
ap = API('nazar_havryliuk')
ap.get_games_names()
data = ap.print_json()
# write data into test.html
with open(os.path.join(THIS_FOLDER, 'test.html'), 'w') as file:
    file.write(str(data))

# routes configuration for static files 
routes = web.RouteTableDef()
routes.static('/TEST', THIS_FOLDER)

@routes.get('/')
async def hello(request):
    return web.json_response(data)

# run aiohttp web server
app = web.Application()
app.add_routes(routes)
web.run_app(app)