"""comment

Revision ID: ccd7f4396301
Revises: cfc928d1a5ad
Create Date: 2023-02-13 11:19:49.787754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccd7f4396301'
down_revision = 'cfc928d1a5ad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('employement_rewards_reward_id_fkey', 'employement_rewards', type_='foreignkey')
    op.drop_constraint('employement_rewards_employement_id_fkey', 'employement_rewards', type_='foreignkey')
    op.create_foreign_key(None, 'employement_rewards', 'employements', ['employement_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.create_foreign_key(None, 'employement_rewards', 'rewards', ['reward_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.add_column('images', sa.Column('image_url', sa.String(), nullable=False))
    op.drop_constraint('images_image_key', 'images', type_='unique')
    op.create_unique_constraint(None, 'images', ['image_url'], schema='dev')
    op.drop_column('images', 'image')
    op.drop_constraint('rewards_employement_id_fkey', 'rewards', type_='foreignkey')
    op.create_foreign_key(None, 'rewards', 'employements', ['employement_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.drop_constraint('user_rewards_user_id_fkey', 'user_rewards', type_='foreignkey')
    op.drop_constraint('user_rewards_reward_id_fkey', 'user_rewards', type_='foreignkey')
    op.drop_constraint('user_rewards_citation_id_fkey', 'user_rewards', type_='foreignkey')
    op.create_foreign_key(None, 'user_rewards', 'users', ['citation_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.create_foreign_key(None, 'user_rewards', 'users', ['user_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.create_foreign_key(None, 'user_rewards', 'rewards', ['reward_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.drop_constraint('users_employement_id_fkey', 'users', type_='foreignkey')
    op.drop_constraint('users_group_id_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'employements', ['employement_id'], ['id'], source_schema='dev', referent_schema='dev')
    op.create_foreign_key(None, 'users', 'groups', ['group_id'], ['id'], source_schema='dev', referent_schema='dev')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', schema='dev', type_='foreignkey')
    op.drop_constraint(None, 'users', schema='dev', type_='foreignkey')
    op.create_foreign_key('users_group_id_fkey', 'users', 'groups', ['group_id'], ['id'])
    op.create_foreign_key('users_employement_id_fkey', 'users', 'employements', ['employement_id'], ['id'])
    op.drop_constraint(None, 'user_rewards', schema='dev', type_='foreignkey')
    op.drop_constraint(None, 'user_rewards', schema='dev', type_='foreignkey')
    op.drop_constraint(None, 'user_rewards', schema='dev', type_='foreignkey')
    op.create_foreign_key('user_rewards_citation_id_fkey', 'user_rewards', 'users', ['citation_id'], ['id'])
    op.create_foreign_key('user_rewards_reward_id_fkey', 'user_rewards', 'rewards', ['reward_id'], ['id'])
    op.create_foreign_key('user_rewards_user_id_fkey', 'user_rewards', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'rewards', schema='dev', type_='foreignkey')
    op.create_foreign_key('rewards_employement_id_fkey', 'rewards', 'employements', ['employement_id'], ['id'])
    op.add_column('images', sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'images', schema='dev', type_='unique')
    op.create_unique_constraint('images_image_key', 'images', ['image'])
    op.drop_column('images', 'image_url')
    op.drop_constraint(None, 'employement_rewards', schema='dev', type_='foreignkey')
    op.drop_constraint(None, 'employement_rewards', schema='dev', type_='foreignkey')
    op.create_foreign_key('employement_rewards_employement_id_fkey', 'employement_rewards', 'employements', ['employement_id'], ['id'])
    op.create_foreign_key('employement_rewards_reward_id_fkey', 'employement_rewards', 'rewards', ['reward_id'], ['id'])
    # ### end Alembic commands ###