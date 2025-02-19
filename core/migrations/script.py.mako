<%
import os

COUNTER_FILE = "migrations/migration_counter.txt"

def get_next_revision_id():
    with open(COUNTER_FILE, "r+") as f:
        current_val_str = f.read().strip()
    return current_val_str

my_up_revision = get_next_revision_id()
%>
"""
${message}

Revision ID: ${my_up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(my_up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
