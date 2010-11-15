from pyramid.configuration import Configurator
from tictactroll.models import get_root

def app(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    config = Configurator(root_factory=get_root, settings=settings)
    config.begin()
    config.add_view('tictactroll.views.my_view',
                    context='tictactroll.models.MyModel',
                    renderer='tictactroll:templates/base.mako')
    config.add_static_view('static', 'tictactroll:static')
    config.end()
    return config.make_wsgi_app()

