
from flask import jsonify

import db.model as m
from . import api_1_0 as bp
from .. import InvalidUsage

@bp.route('users')
def get_users():
	return jsonify(users=m.User.dump(m.User.query.all()))
