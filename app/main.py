import bottle
import os
import random


taunts = ['Cumin for you', 'Catch me if you cayenne', 'Youre outta thyme']
lastMove = 'up'

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
    board_width = data.get('width')
    board_height = data.get('height')
    board = [[0 for x in range(board_width)] for y in range(board_height)]
    for a in data.get('food').get('data'):
        x = a.get('x')
        y = a.get('y')
        board[x][y] = 'F'

    for snake in data.get('snakes').get('data'):
        if snake.get('name') == 'spicerack-snake':
            iteration = 1

            for point in snake.get('body').get('data'):
                if iteration == 1:
                    headX = point.get('x')
                    headY = point.get('y')
                    board[headX][headY] = 'H'
                else:
                    ourSnakeX = point.get('x')
                    ourSnakeY = point.get('y')
                    board[ourSnakeX][ourSnakeY] = 'X'
                iteration = iteration+1
        else:
            for point in snake.get('body').get('data'):
                snakeX = point.get('x')
                snakeY = point.get('y')
                board[snakeX][snakeY] = 'X'

    moveOptions = {'spacesDown': 0, 'spacesUp': 0, 'spacesLeft': 0, 'spacesRight':0}
    global lastMove
    if lastMove == 'up':
        #dont go down
    for down in range(headY+1, board_height):
        if board[headX][down] == 0 or board[headX][down] == 'F':
            moveOptions['spacesDown'] = moveOptions['spacesDown']+1
        else:
            break
    for right in range(headX+1, board_width):
        if board[right][headY] == 0 or board[right][headY] == 'F':
            moveOptions['spacesRight'] = moveOptions['spacesRight']+1
        else:
            break
    for up in range(headY-1, 0, -1):
        if board[headX][up] == 0 or board[headX][up] == 'F':
            moveOptions['spacesUp'] = moveOptions['spacesUp']+1
        else:
            break
    for left in range(headX-1, 0, -1):
        if board[left][headY] == 0 or board[left][headY] == 'F':
            moveOptions['spacesLeft'] = moveOptions['spacesLeft']+1
        else:
            break
    most = max(moveOptions, key=lambda i: moveOptions[i])

    move = lastMove
    if most == 'spacesUp':
        move = 'up'
    elif most == 'spacesDown':
        move = 'down'
    elif most == 'spacesLeft':
        move = 'left'
    elif most == 'spacesRight':
        movw = 'right'
    #taunt = taunts[random.randint(0,2)]
    taunt = "Head: ", headX,", "headY
    lastMove = move
    return {
        'move': move,
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
