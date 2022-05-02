import flask

from . import db_session
from .games import Game

blueprint = flask.Blueprint(
    'games_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/games', methods=['GET'])
def get_all_games():
    db_sess = db_session.create_session()
    games = db_sess.query(Game).all()
    
    return flask.jsonify({
        'games': [game.to_dict(only=('title', 'description', 'created_date', 'user_id')) for game in games]
    })


@blueprint.route('/api/games/<title>', methods=['GET'])
def get_single_game(title):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.title.like(f'%{title}%')).first()
    if game:
        return flask.jsonify(game.to_dict(only=('title', 'description', 'created_date', 'user_id')))
    else:
        return flask.jsonify({'error': 'Bad request'})

    
@blueprint.route('/api/help', methods=['GET'])
def api_help():
    return jsonify({'/api/games': 'спесок всех игр по базе данных', '/api/games/<title>': 'получить одну игру'})
