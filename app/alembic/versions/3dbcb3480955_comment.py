"""comment

Revision ID: 3dbcb3480955
Revises: ccd7f4396301
Create Date: 2023-02-27 11:12:41.352611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dbcb3480955'
down_revision = 'ccd7f4396301'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('employement_rewards_employement_id_fkey', 'employement_rewards', type_='foreignkey')
    op.drop_constraint('employement_rewards_reward_id_fkey', 'employement_rewards', type_='foreignkey')
    op.create_foreign_key(None, 'employement_rewards', 'employements', ['employement_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.create_foreign_key(None, 'employement_rewards', 'rewards', ['reward_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.drop_constraint('images_image_url_key', 'images', type_='unique')
    op.drop_column('images', 'image_url')
    op.drop_constraint('rewards_employement_id_fkey', 'rewards', type_='foreignkey')
    op.create_foreign_key(None, 'rewards', 'employements', ['employement_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.drop_constraint('user_rewards_user_id_fkey', 'user_rewards', type_='foreignkey')
    op.drop_constraint('user_rewards_reward_id_fkey', 'user_rewards', type_='foreignkey')
    op.drop_constraint('user_rewards_citation_id_fkey', 'user_rewards', type_='foreignkey')
    op.create_foreign_key(None, 'user_rewards', 'rewards', ['reward_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.create_foreign_key(None, 'user_rewards', 'users', ['user_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.create_foreign_key(None, 'user_rewards', 'users', ['citation_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.drop_constraint('users_group_id_fkey', 'users', type_='foreignkey')
    op.drop_constraint('users_employement_id_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'employements', ['employement_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.create_foreign_key(None, 'users', 'groups', ['group_id'], ['id'], source_schema='dev', referent_schema='dev')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', schema='dev', type_='foreignkey')
    op.drop_constraint(None, 'users', schema='dev', type_='foreignkey')
    op.create_foreign_key('users_employement_id_fkey', 'users', 'employements', ['employement_id'], ['id'])
    op.create_foreign_key('users_group_id_fkey', 'users', 'groups', ['group_id'], ['id'])
    op.drop_constraint(None, 'user_rewards', schema='dev', type_='foreignkey')
    op.drop_constraint(None, 'user_rewards', schema='dev', type_='foreignkey')
    op.drop_constraint(None, 'user_rewards', schema='dev', type_='foreignkey')
    op.create_foreign_key('user_rewards_citation_id_fkey', 'user_rewards', 'users', ['citation_id'], ['id'])
    op.create_foreign_key('user_rewards_reward_id_fkey', 'user_rewards', 'rewards', ['reward_id'], ['id'])
    op.create_foreign_key('user_rewards_user_id_fkey', 'user_rewards', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'rewards', schema='dev', type_='foreignkey')
    op.create_foreign_key('rewards_employement_id_fkey', 'rewards', 'employements', ['employement_id'], ['id'])
    op.add_column('images', sa.Column('image_url', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_unique_constraint('images_image_url_key', 'images', ['image_url'])
    op.drop_constraint(None, 'employement_rewards', schema='dev', type_='foreignkey')
    op.drop_constraint(None, 'employement_rewards', schema='dev', type_='foreignkey')
    op.create_foreign_key('employement_rewards_reward_id_fkey', 'employement_rewards', 'rewards', ['reward_id'], ['id'])
    op.create_foreign_key('employement_rewards_employement_id_fkey', 'employement_rewards', 'employements', ['employement_id'], ['id'])
    # ### end Alembic commands ###
