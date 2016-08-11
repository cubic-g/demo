
from flask import jsonify

import db.model as m
from . import api_1_0 as bp
from .. import InvalidUsage

@bp.route('addresses')
def get_addresses():
	return jsonify(addresses=m.Address.dump(m.Address.query.all()))
