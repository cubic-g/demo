
from sqlalchemy import MetaData, Table, Column, ForeignKey, Index
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import Integer, INTEGER, Text, TEXT, TIMESTAMP, Date, DATE, BOOLEAN, LargeBinary, CHAR
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, INET, INTERVAL, CIDR
from sqlalchemy import text, DDL, join, select, event


metadata = MetaData()


t_user = Table('user', metadata,
	Column('id', Integer, primary_key=True, key=u'id', doc=''),
	Column('email', Text, nullable=False, unique=True, key=u'email', doc=''),
	Column('family_name', Text, key=u'familyName', doc=''),
	Column('given_name', Text, key=u'givenName', doc=''),
)


__all__ = [name for name in locals().keys()
		if name.startswith('t_') or name.startswith('j_')]
__all__.insert(0, 'metadata')
