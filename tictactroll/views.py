"""
This is where the views are defined, from my Pylons experience, they are
very similar to controllers and if they are not, I'm using them this way
in this application ;)
"""

from gamestate import *
from utils import format_number
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

def game(request):
    """Show the board, let the player play!"""
    if "gamestate" not in request.session:
        return HTTPFound(location="/")
    gamestate = request.session["gamestate"]
    if gamestate.is_expired():
        gamestate.reset()

    return { "gamestate": gamestate }

def welcome(request):
    """Hello, what's your name?"""
    return { "countdown": GameState.initial_countdown }

def about(request):
    """Plain page."""
    return {}

def enter_game(request):
    """Redirector which sets up the session with the initial gamestate."""
    try:
        username = request.params["username"]
    except:
        return HTTPBadRequest()

    gamestate = GameState(username)
    request.session["gamestate"] = gamestate
    request.session.save()

    return HTTPFound(location="/game")

def next_troll_grid(request):
    """Get the next grid positioned by le troll"""
    if "gamestate" not in request.session:
        return { "status": "no_session" }

    gamestate = request.session["gamestate"]
    if gamestate.is_expired():
        return { "status": "gameover", "reason": "timeout" }

    matches, grid = gamestate.next_troll_grid()

    if not matches:
        return { "status": "thats_all_folks" }

    return {
        "status": "great_scott",
        "grids": [
            (grid.x, grid.y),
        ],
        "pieces": matches,
        "p1": gamestate.get_p1_stats(),
        "p2": gamestate.get_p2_stats(),
    }

def add_grid(request):
    """The human player adds a grid, check if we can first, return a missed
    shot via Exceptions.
    """
    
    if "gamestate" not in request.session:
        return { "status": "no_session" }

    gamestate = request.session["gamestate"]
    if gamestate.is_expired():
        return { "status": "gameover", "reason": "timeout" }

    try:
        x = int(request.params["x"])
        y = int(request.params["y"])
    except:
        return HTTPBadRequest()

    status = { }

    try:
        good_pieces = gamestate.add_grid(x, y, "green")
        status.update({ "status": "much_success", "pieces": good_pieces })
    except GridOverlaps:
        status.update({ "status": "overlap" })
    except BadSpot:
        status.update({ "status": "badspot" })
    except OutOfLife:
        status.update({ "status": "gameover" })

    status.update({
        "life": gamestate.life,
        "p1": gamestate.get_p1_stats(),
        "p2": gamestate.get_p2_stats(),
    })

    return status

def new_game(request):
    """Reset the current game state if any and play again!"""
    if "gamestate" not in request.session:
        return HTTPFound(location="/")
    gamestate = request.session["gamestate"]
    gamestate.reset()
    return HTTPFound(location="/game")

def gameover_html(request):
    """Dump the game over HTML with the high scores."""
    if "gamestate" not in request.session:
        return HTTPBadRequest()

    gamestate = request.session["gamestate"]
    gamestate.record()
    return {
        "gamestate": gamestate,
        "fmt": format_number,
        "stats": gamestate.get_p1_stats()
    }

