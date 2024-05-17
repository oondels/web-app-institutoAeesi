"""empty message

Revision ID: 1c3927bd7aef
Revises: b27de8bd1a81
Create Date: 2024-05-17 09:50:19.444682

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1c3927bd7aef'
down_revision = 'b27de8bd1a81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('aluno', schema=None) as batch_op:
        batch_op.alter_column('cpf',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.alter_column('telefone',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=25),
               existing_nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_confirmed', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('confirmed_on', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('confirmed_on')
        batch_op.drop_column('is_confirmed')

    with op.batch_alter_table('aluno', schema=None) as batch_op:
        batch_op.alter_column('telefone',
               existing_type=sa.String(length=25),
               type_=mysql.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('cpf',
               existing_type=sa.String(length=200),
               type_=mysql.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###