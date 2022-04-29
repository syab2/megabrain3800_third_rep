import flask

from . import db_session
from .games import Game

blueprint = flask.Blueprint('games_api', __name__, template_folder='templates')


@blueprint.route('/api/games')
def get_all_games():
    db_sess = db_session.create_session()
    games = db_sess.query(Game).all()
    
    return flask.jsonify({
        'games': [game.to_dict(only=('title', 'description', 'created_date', 'user_id')) for game in games]
    })


@blueprint.route('/api/games/<int:id>')
def get_single_game(id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == id).first()
    
    return flask.jsonify(game.to_dict(only=('title', 'description', 'created_date', 'user_id')))


