from flask import current_app
from flask import render_template, request, redirect, url_for, make_response, send_from_directory, Blueprint
from flask_login import LoginManager, login_required, login_user, logout_user, confirm_login, current_user
from database import db_session
from models import User, Game
from settings import DEBUG, VERSION, HEX_CLIP_PATH
import re
import json

gameplay_blueprint = Blueprint('gameplay', __name__, template_folder='templates')


@gameplay_blueprint.route("/newgame", methods=["GET"])
@login_required
def new_game():
    return make_response(render_template("gamesetup.html", version=VERSION, hex_clip_path=HEX_CLIP_PATH))


@gameplay_blueprint.route("/creategame", methods=["POST"])
@login_required
def create_game():
    data = json.loads(request.form['data'])
    return make_response(render_template("debug_template.html", message=json.dumps(data, indent=4, sort_keys=True)))


@gameplay_blueprint.route("/game/<game_id>", methods=['GET'])
def load_game(game_id):
    response = make_response(render_template("game.html", game_id=game_id, version=VERSION, hex_clip_path=HEX_CLIP_PATH,
                                             playercolors={1: "FF0000", 2: "30ff30", 3: "0000ff"}, me=2))
    return response


@gameplay_blueprint.route("/icon/<icon>/<color>.svg")
def get_icon(icon, color):
    if icon not in ['city', 'settlement', 'road']:
        return make_response("Icon not found", 404)
    elif re.fullmatch("^[a-f0-9]{6}$", color, re.IGNORECASE) is None:
        return make_response("Invalid color", 400)

    current_app.logger.debug("Returning icon %s with primary %s", icon, color)

    response = make_response(render_template("icons/{}.svg".format(icon), primary=color))
    response.mimetype = "image/svg+xml"
    return response
