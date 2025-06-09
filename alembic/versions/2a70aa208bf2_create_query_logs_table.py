"""create_query_logs_table

Revision ID: 2a70aa208bf2
Revises: b458b21a7920
Create Date: 2025-06-08 13:35:19.430473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '2a70aa208bf2'
down_revision: Union[str, None] = 'b458b21a7920'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'query_logs',
        Column('id', Integer, primary_key=True),
        Column('query', Text),
        Column('results_count', Integer),
        Column('created_at', DateTime, default=datetime.utcnow)
    )

def downgrade() -> None:
    op.drop_table('query_logs')
