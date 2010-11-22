from pyramid.configuration import Configurator
from pyramid_beaker import session_factory_from_settings
from tictactroll.models import get_root

def app(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    config = Configurator(root_factory=get_root, settings=settings)
    config.begin()
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    config.add_view("tictactroll.views.game", name="game",
                    renderer="tictactroll:templates/game.mako")
    config.add_view("tictactroll.views.about", name="about",
                    renderer="tictactroll:templates/about.mako")
    config.add_view("tictactroll.views.welcome",
                    renderer="tictactroll:templates/welcome.mako")
    config.add_view("tictactroll.views.enter_game", name="enter_game")
    config.add_view("tictactroll.views.new_game", name="new_game")

    config.add_view("tictactroll.views.add_grid", name="add_grid",
                    renderer="json")

    config.add_view("tictactroll.views.next_troll_grid",
                    name="next_troll_grid", renderer="json")

    config.add_view("tictactroll.views.gameover_html", name="gameover",
                    renderer="tictactroll:templates/gameover.mako")

    config.add_static_view("static", "tictactroll:static")
    config.end()
    return config.make_wsgi_app()

