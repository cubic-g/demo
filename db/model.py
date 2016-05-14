
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, synonym, column_property, object_session
from sqlalchemy.sql import case, text, func
from marshmallow import Schema, fields

from . import database
from .schema import *

def set_schema(cls, schema_class):
	if not issubclass(schema_class, Schema):
		raise TypeError('schema must be subclass of Schema')
	cls._schema_class = schema_class


def dump(cls, obj, extra=None, only=(), exclude=(), prefix=u'',
		strict=False, context=None, load_only=(), **kwargs):
	if cls._schema_class is None:
		raise RuntimeError('schema class not found for {0}'\
			.format(cls.__name__))
	s = cls._schema_class(extra=extra, only=only, exclude=exclude,
			prefix=prefix, strict=strict, context=context)
	if isinstance(obj, list):
		many = True
	else:
		many = False
	marshal_result = s.dump(obj, many=many, **kwargs)
	return marshal_result.data


Base = database.Model
Base._schema_class = None
Base.set_schema = classmethod(set_schema)
Base.dump = classmethod(dump)


_names = set(locals().keys()) | {'_names'}


#
# Define model class and its schema (if needed) below
#
##########################################################################


# User
class User(Base):
	__table__ = t_user
	userId = synonym('id')
	addresses = relationship('Address', secondary=t_user_address,
		order_by='Address.addressId')

class UserSchema(Schema):
	addresses = fields.Nested('AddressSchema', many=True)
	class Meta:
		fields = ('userId', 'email', 'familyName', 'givenName',
			'addresses')


# Address
class Address(Base):
	__table__ = t_address
	addressId = synonym('id')

class AddressSchema(Schema):
	class Meta:
		fields = ('addressId', 'street0', 'street1', 'street2',
			'city', 'province')


##########################################################################
#
# Define model class and its schema (if needed) above
#

__all__ = list(set(locals().keys()) - _names)

for schema_name in [i for i in __all__ if i.endswith('Schema')]:
	klass_name = schema_name[:-6]
	assert klass_name
	klass = locals()[klass_name]
	schema = locals()[schema_name]
	klass.set_schema(schema)

