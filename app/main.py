import bottle
import os
import random


taunts = ['Cumin for you', 'Catch me if you cayenne', 'Youre outta thyme']

@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    taunt = taunts[random.randit(0,3)]
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'head_url': 'fang',
        'taunt': taunt
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data

    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    print direction
    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
