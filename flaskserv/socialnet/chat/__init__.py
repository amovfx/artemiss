from flask import Blueprint

chat_bp = Blueprint('chat',
                      __name__,
                      template_folder='templates',
                      static_url_path='/chat/static',
                      static_folder='static')

from . import routes, events