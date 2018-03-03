import bottle
import os
import random


taunts = ['Cumin for you', 'Catch me if you cayenne', 'Youre outta thyme']
board_width = 20
board_height = 20

@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    taunt = taunts[random.randint(0,2)]
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')


    head_url = '%s://%s/static/spicerack.jpeg' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )
    # TODO: Do things with data

    return {
        'color': '#3B87AF',
        'head_url': head_url,
        'head_type': 'fang',
        'tail_type': 'curled',
        'taunt': taunt
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    board = [[0 for x in range(data.get('width'))] for y in range(data.get('height'))]
    for a in data.get('food').get('data'):
        x = a.get('x')
        y = a.get('y')
        board[x][y] = 'F'

    for snake in data.get('snakes').get('data'):
        if snake.get('name') == 'spicerack-snake':
            for point in snake.get('body').get('data'):
                snakeX = point.get('x')
                snakeY = point.get('y')
                board[snakeX][snakeY] = 'L'
        else:
            for point in snake.get('body').get('data'):
                snakeX = point.get('x')
                snakeY = point.get('y')
                board[snakeX][snakeY] = 'X'
    # TODO: Do things with data
    #print(board)
    taunt = taunts[random.randint(0,2)]
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    print direction
    return {
        'move': direction,
        'taunt': taunt
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
