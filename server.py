from sqlalchemy import MetaData, Table, Column, Integer, String, UniqueConstraint


metadata = MetaData()

users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(50), nullable=False),
    UniqueConstraint('name', name='uq_users_name')
)
