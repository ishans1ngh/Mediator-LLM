"""add_ai_metadata

Revision ID: 20240827_add_ai_metadata
Revises: 
Create Date: 2024-08-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20240827_add_ai_metadata'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add AI metadata columns to patient_profile_attributes
    op.add_column('patient_profile_attributes', sa.Column('normalized_value', sa.Text(), nullable=True))
    op.add_column('patient_profile_attributes', sa.Column('unit', sa.String(length=64), nullable=True))
    op.add_column('patient_profile_attributes', sa.Column('source_text', sa.Text(), nullable=True))
    op.add_column('patient_profile_attributes', sa.Column('status', sa.String(length=32), nullable=False, server_default='UNKNOWN'))
    op.add_column('patient_profile_attributes', sa.Column('agent_version', sa.String(length=64), nullable=True))
    op.add_column('patient_profile_attributes', sa.Column('prompt_version', sa.String(length=64), nullable=True))
    op.add_column('patient_profile_attributes', sa.Column('model_name', sa.String(length=128), nullable=True))
    
    # Make attribute_value nullable (was NOT NULL before)
    op.alter_column('patient_profile_attributes', 'attribute_value', nullable=True)
    
    # Add AI metadata columns to trial_criteria
    op.add_column('trial_criteria', sa.Column('normalized_value', sa.Text(), nullable=True))
    op.add_column('trial_criteria', sa.Column('source_text', sa.Text(), nullable=True))
    op.add_column('trial_criteria', sa.Column('agent_version', sa.String(length=64), nullable=True))
    op.add_column('trial_criteria', sa.Column('prompt_version', sa.String(length=64), nullable=True))
    op.add_column('trial_criteria', sa.Column('model_name', sa.String(length=128), nullable=True))
    
    # Change value column from String(255) to Text to support complex values like JSON
    op.alter_column('trial_criteria', 'value', type_=sa.Text(), existing_type=sa.String(length=255))
    
    # Change confidence to Numeric(5,4) for better precision
    op.alter_column('trial_criteria', 'confidence', type_=sa.Numeric(5, 4), existing_type=sa.Float())


def downgrade() -> None:
    # Revert trial_criteria changes
    op.alter_column('trial_criteria', 'confidence', type_=sa.Float(), existing_type=sa.Numeric(5, 4))
    op.alter_column('trial_criteria', 'value', type_=sa.String(length=255), existing_type=sa.Text())
    op.drop_column('trial_criteria', 'model_name')
    op.drop_column('trial_criteria', 'prompt_version')
    op.drop_column('trial_criteria', 'agent_version')
    op.drop_column('trial_criteria', 'source_text')
    op.drop_column('trial_criteria', 'normalized_value')
    
    # Revert patient_profile_attributes changes
    op.alter_column('patient_profile_attributes', 'attribute_value', nullable=False)
    op.drop_column('patient_profile_attributes', 'model_name')
    op.drop_column('patient_profile_attributes', 'prompt_version')
    op.drop_column('patient_profile_attributes', 'agent_version')
    op.drop_column('patient_profile_attributes', 'status')
    op.drop_column('patient_profile_attributes', 'source_text')
    op.drop_column('patient_profile_attributes', 'unit')
    op.drop_column('patient_profile_attributes', 'normalized_value')
