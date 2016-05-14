
from sqlalchemy import MetaData, Table, Column, ForeignKey, Index
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import Integer, INTEGER, Text, TEXT, TIMESTAMP, Date, DATE, BOOLEAN, LargeBinary, CHAR
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, INET, INTERVAL, CIDR
from sqlalchemy import text, DDL, join, select, event


metadata = MetaData()

#
# Define tables below
#
##########################################################################


t_user = Table('user', metadata,
	Column('id', Integer, primary_key=True, key=u'id', doc=''),
	Column('email', Text, nullable=False, unique=True, key=u'email', doc=''),
	Column('family_name', Text, key=u'familyName', doc=''),
	Column('given_name', Text, key=u'givenName', doc=''),
)


t_address = Table('address', metadata,
	Column('id', Integer, primary_key=True, key=u'id', doc=''),
	Column('street0', Text, nullable=False, key=u'street0', doc=''),
	Column('street1', Text, nullable=False, key=u'street1', doc=''),
	Column('street2', Text, key=u'street2', doc=''),
	Column('city', Text, nullable=False, key=u'city', doc=''),
	Column('province', Text, nullable=False, key=u'province', doc=''),
)


t_user_address = Table('user_address', metadata,
	Column('user_id', Integer, ForeignKey('user.id'),
		primary_key=True, autoincrement=False, key='userId', doc=''),
	Column('address_id', Integer, ForeignKey('address.id'),
		primary_key=True, autoincrement=False, key='addressId', doc=''),
)


##########################################################################
#
# Define tables above
#

__all__ = [name for name in locals().keys()
		if name.startswith('t_') or name.startswith('j_')]
__all__.insert(0, 'metadata')
