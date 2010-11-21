from gamestate import GameState
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

def game(request):
    if "gamestate" not in request.session:
        return HTTPFound(location="/")

    gamestate = request.session["gamestate"]
    return { "gamestate": gamestate }

def welcome(request):
    return { "countdown": GameState.initial_countdown }

def enter_game(request):
    try:
        username = request.params["username"]
    except:
        return HTTPBadRequest()

    gamestate = GameState(username)
    request.session["gamestate"] = gamestate
    request.session.save()

    return HTTPFound(location="/game")

def add_grid(request):
    return { "status": "much_success" }
