"""Initial migration - Create all tables.

Revision ID: 001_initial_schema
Revises: None
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum types
    user_role_enum = postgresql.ENUM('admin', 'agronomist', 'sales_representative', 'farmer', name='userrole')
    user_role_enum.create(op.get_bind(), checkfirst=True)

    diagnosis_status_enum = postgresql.ENUM('pending', 'processing', 'completed', 'failed', name='diagnosisstatus')
    diagnosis_status_enum.create(op.get_bind(), checkfirst=True)

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', user_role_enum, nullable=False, server_default='farmer'),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('region', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index('idx_user_email', 'users', ['email'])
    op.create_index('idx_user_created_at', 'users', ['created_at'])

    # Create crops table
    op.create_table(
        'crops',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('name_ar', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('scientific_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_index('idx_crop_name', 'crops', ['name'])

    # Create diseases table
    op.create_table(
        'diseases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('crop_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('name_ar', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('symptoms', sa.JSON(), nullable=False),
        sa.Column('causes', sa.JSON(), nullable=False),
        sa.Column('severity_level', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['crop_id'], ['crops.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_disease_crop_id', 'diseases', ['crop_id'])
    op.create_index('idx_disease_name', 'diseases', ['name'])

    # Create growth_stages table
    op.create_table(
        'growth_stages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('crop_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('name_ar', sa.String(), nullable=True),
        sa.Column('days_from_planting', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['crop_id'], ['crops.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_growth_stage_crop_id', 'growth_stages', ['crop_id'])

    # Create products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('name_ar', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('active_ingredient', sa.String(), nullable=False),
        sa.Column('concentration', sa.String(), nullable=False),
        sa.Column('dosage', sa.String(), nullable=False),
        sa.Column('safety_info', sa.Text(), nullable=False),
        sa.Column('pre_harvest_interval', sa.Integer(), nullable=True),
        sa.Column('brochure_url', sa.String(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('stock_available', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_index('idx_product_category', 'products', ['category'])
    op.create_index('idx_product_active_ingredient', 'products', ['active_ingredient'])

    # Create diagnoses table
    op.create_table(
        'diagnoses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('disease_id', sa.Integer(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('crop_type', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('region', sa.String(), nullable=False),
        sa.Column('plant_age_days', sa.Integer(), nullable=True),
        sa.Column('growth_stage', sa.String(), nullable=True),
        sa.Column('irrigation_method', sa.String(), nullable=True),
        sa.Column('greenhouse', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('status', diagnosis_status_enum, nullable=False, server_default='pending'),
        sa.Column('detected_problem', sa.String(), nullable=False),
        sa.Column('symptoms_observed', sa.JSON(), nullable=False),
        sa.Column('possible_causes', sa.JSON(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('diagnosis_notes', sa.Text(), nullable=True),
        sa.Column('ai_response', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['disease_id'], ['diseases.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_diagnosis_user_id', 'diagnoses', ['user_id'])
    op.create_index('idx_diagnosis_created_at', 'diagnoses', ['created_at'])
    op.create_index('idx_diagnosis_status', 'diagnoses', ['status'])

    # Create recommendations table
    op.create_table(
        'recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('diagnosis_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('recommendation_type', sa.String(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('application_program', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['diagnosis_id'], ['diagnoses.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_recommendation_diagnosis_id', 'recommendations', ['diagnosis_id'])

    # Create chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('diagnosis_id', sa.Integer(), nullable=True),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('ai_response', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_chat_message_user_id', 'chat_messages', ['user_id'])
    op.create_index('idx_chat_message_created_at', 'chat_messages', ['created_at'])

    # Create quotation_requests table
    op.create_table(
        'quotation_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('sales_rep_assigned', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_quotation_request_user_id', 'quotation_requests', ['user_id'])
    op.create_index('idx_quotation_request_created_at', 'quotation_requests', ['created_at'])

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('resource_type', sa.String(), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_audit_log_user_id', 'audit_logs', ['user_id'])
    op.create_index('idx_audit_log_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_log_created_at', 'audit_logs', ['created_at'])

    # Create association tables
    op.create_table(
        'crop_product',
        sa.Column('crop_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['crop_id'], ['crops.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('crop_id', 'product_id'),
    )

    op.create_table(
        'disease_product',
        sa.Column('disease_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['disease_id'], ['diseases.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('disease_id', 'product_id'),
    )


def downgrade() -> None:
    op.drop_table('disease_product')
    op.drop_table('crop_product')
    op.drop_index('idx_audit_log_created_at', table_name='audit_logs')
    op.drop_index('idx_audit_log_action', table_name='audit_logs')
    op.drop_index('idx_audit_log_user_id', table_name='audit_logs')
    op.drop_table('audit_logs')
    op.drop_index('idx_quotation_request_created_at', table_name='quotation_requests')
    op.drop_index('idx_quotation_request_user_id', table_name='quotation_requests')
    op.drop_table('quotation_requests')
    op.drop_index('idx_chat_message_created_at', table_name='chat_messages')
    op.drop_index('idx_chat_message_user_id', table_name='chat_messages')
    op.drop_table('chat_messages')
    op.drop_index('idx_recommendation_diagnosis_id', table_name='recommendations')
    op.drop_table('recommendations')
    op.drop_index('idx_diagnosis_status', table_name='diagnoses')
    op.drop_index('idx_diagnosis_created_at', table_name='diagnoses')
    op.drop_index('idx_diagnosis_user_id', table_name='diagnoses')
    op.drop_table('diagnoses')
    op.drop_index('idx_product_active_ingredient', table_name='products')
    op.drop_index('idx_product_category', table_name='products')
    op.drop_table('products')
    op.drop_index('idx_growth_stage_crop_id', table_name='growth_stages')
    op.drop_table('growth_stages')
    op.drop_index('idx_disease_name', table_name='diseases')
    op.drop_index('idx_disease_crop_id', table_name='diseases')
    op.drop_table('diseases')
    op.drop_index('idx_crop_name', table_name='crops')
    op.drop_table('crops')
    op.drop_index('idx_user_created_at', table_name='users')
    op.drop_index('idx_user_email', table_name='users')
    op.drop_table('users')
