# type: ignore
"""Initial revision

Revision ID: a22cc7704d14
Revises:
Create Date: 2024-01-14 14:59:07.826121

"""
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from advanced_alchemy.types import EncryptedString, EncryptedText, GUID, ORA_JSONB, DateTimeUTC
from sqlalchemy import Text  # noqa: F401

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = ["downgrade", "upgrade", "schema_upgrades", "schema_downgrades", "data_upgrades", "data_downgrades"]

sa.GUID = GUID
sa.DateTimeUTC = DateTimeUTC
sa.ORA_JSONB = ORA_JSONB
sa.EncryptedString = EncryptedString
sa.EncryptedText = EncryptedText

# revision identifiers, used by Alembic.
revision = 'a22cc7704d14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            schema_upgrades()
            data_upgrades()

def downgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            data_downgrades()
            schema_downgrades()

def schema_upgrades() -> None:
    """schema upgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.GUID(length=16), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_role')),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name', name=op.f('uq_role_name')),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('slug', name=op.f('uq_role_slug'))
    )
    op.create_table('tag',
    sa.Column('id', sa.GUID(length=16), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tag')),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('slug', name=op.f('uq_tag_slug'))
    )
    op.create_table('team',
    sa.Column('id', sa.GUID(length=16), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_team')),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('slug', name=op.f('uq_team_slug'))
    )
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_team_name'), ['name'], unique=False)

    op.create_table('user_account',
    sa.Column('id', sa.GUID(length=16), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(length=255), nullable=True),
    sa.Column('avatar_url', sa.String(length=500), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('verified_at', sa.Date(), nullable=True),
    sa.Column('joined_at', sa.Date(), nullable=False),
    sa.Column('login_count', sa.Integer(), nullable=False),
    sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_account'))
    )
    with op.batch_alter_table('user_account', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_account_email'), ['email'], unique=True)

    op.create_table('team_invitation',
    sa.Column('id', sa.GUID(length=16), nullable=False),
    sa.Column('team_id', sa.GUID(length=16), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('is_accepted', sa.Boolean(), nullable=False),
    sa.Column('invited_by_id', sa.GUID(length=16), nullable=True),
    sa.Column('invited_by_email', sa.String(), nullable=False),
    sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['invited_by_id'], ['user_account.id'], name=op.f('fk_team_invitation_invited_by_id_user_account'), ondelete='set null'),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], name=op.f('fk_team_invitation_team_id_team'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_team_invitation'))
    )
    with op.batch_alter_table('team_invitation', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_team_invitation_email'), ['email'], unique=False)

    op.create_table('team_member',
    sa.Column('id', sa.GUID(length=16), nullable=False),
    sa.Column('user_id', sa.GUID(length=16), nullable=False),
    sa.Column('team_id', sa.GUID(length=16), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('is_owner', sa.Boolean(), nullable=False),
    sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], name=op.f('fk_team_member_team_id_team'), ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user_account.id'], name=op.f('fk_team_member_user_id_user_account'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_team_member')),
    sa.UniqueConstraint('user_id', 'team_id', name=op.f('uq_team_member_user_id'))
    )
    with op.batch_alter_table('team_member', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_team_member_role'), ['role'], unique=False)

    op.create_table('team_tag',
    sa.Column('team_id', sa.GUID(length=16), nullable=False),
    sa.Column('tag_id', sa.GUID(length=16), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], name=op.f('fk_team_tag_tag_id_tag'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], name=op.f('fk_team_tag_team_id_team'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('team_id', 'tag_id', name=op.f('pk_team_tag'))
    )
    op.create_table('user_account_oauth',
    sa.Column('id', sa.GUID(length=16), nullable=False),
    sa.Column('user_id', sa.GUID(length=16), nullable=False),
    sa.Column('oauth_name', sa.String(length=100), nullable=False),
    sa.Column('access_token', sa.String(length=1024), nullable=False),
    sa.Column('expires_at', sa.Integer(), nullable=True),
    sa.Column('refresh_token', sa.String(length=1024), nullable=True),
    sa.Column('account_id', sa.String(length=320), nullable=False),
    sa.Column('account_email', sa.String(length=320), nullable=False),
    sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_account.id'], name=op.f('fk_user_account_oauth_user_id_user_account'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_account_oauth'))
    )
    with op.batch_alter_table('user_account_oauth', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_account_oauth_account_id'), ['account_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_account_oauth_oauth_name'), ['oauth_name'], unique=False)

    op.create_table('user_account_role',
    sa.Column('id', sa.GUID(length=16), nullable=False),
    sa.Column('user_id', sa.GUID(length=16), nullable=False),
    sa.Column('role_id', sa.GUID(length=16), nullable=False),
    sa.Column('assigned_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTimeUTC(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name=op.f('fk_user_account_role_role_id_role'), ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user_account.id'], name=op.f('fk_user_account_role_user_id_user_account'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_account_role'))
    )
    # ### end Alembic commands ###

def schema_downgrades() -> None:
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_account_role')
    with op.batch_alter_table('user_account_oauth', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_account_oauth_oauth_name'))
        batch_op.drop_index(batch_op.f('ix_user_account_oauth_account_id'))

    op.drop_table('user_account_oauth')
    op.drop_table('team_tag')
    with op.batch_alter_table('team_member', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_team_member_role'))

    op.drop_table('team_member')
    with op.batch_alter_table('team_invitation', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_team_invitation_email'))

    op.drop_table('team_invitation')
    with op.batch_alter_table('user_account', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_account_email'))

    op.drop_table('user_account')
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_team_name'))

    op.drop_table('team')
    op.drop_table('tag')
    op.drop_table('role')
    # ### end Alembic commands ###

def data_upgrades() -> None:
    """Add any optional data upgrade migrations here!"""

def data_downgrades() -> None:
    """Add any optional data downgrade migrations here!"""
