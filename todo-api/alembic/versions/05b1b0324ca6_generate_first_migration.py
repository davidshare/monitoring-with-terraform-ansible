"""generate first migration

Revision ID: 05b1b0324ca6
Revises: 
Create Date: 2024-11-29 23:51:47.590649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '05b1b0324ca6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ensure `statusenum` type exists
    op.execute(
        text("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statusenum') THEN
                CREATE TYPE statusenum AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED');
            END IF;
        END $$;
        """)
    )

    # Ensure `priorityenum` type exists
    op.execute(
        text("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'priorityenum') THEN
                CREATE TYPE priorityenum AS ENUM ('LOW', 'MEDIUM', 'HIGH');
            END IF;
        END $$;
        """)
    )

    # Conditionally create 'users' table
    op.execute(
        text("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'users') THEN
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR NOT NULL UNIQUE,
                    email VARCHAR NOT NULL UNIQUE,
                    hashed_password VARCHAR NOT NULL
                );
            END IF;
        END $$;
        """)
    )

    # Conditionally create 'todo_items' table
    op.execute(
        text("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'todo_items') THEN
                CREATE TABLE todo_items (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR NOT NULL,
                    description TEXT NOT NULL,
                    start_date TIMESTAMP NULL,
                    due_date TIMESTAMP NULL,
                    priority priorityenum NOT NULL,
                    status statusenum NOT NULL,
                    tags VARCHAR NULL,
                    category VARCHAR NOT NULL,
                    created_at TIMESTAMP NULL,
                    updated_at TIMESTAMP NULL,
                    user_id INTEGER NOT NULL REFERENCES users (id)
                );
            END IF;
        END $$;
        """)
    )

    # Add indexes if they don't already exist
    op.execute(
        text("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 
                FROM pg_indexes 
                WHERE tablename = 'users' AND indexname = 'ix_users_email'
            ) THEN
                CREATE UNIQUE INDEX ix_users_email ON users (email);
            END IF;
        END $$;
        """)
    )

    op.execute(
        text("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 
                FROM pg_indexes 
                WHERE tablename = 'users' AND indexname = 'ix_users_id'
            ) THEN
                CREATE INDEX ix_users_id ON users (id);
            END IF;
        END $$;
        """)
    )

    op.execute(
        text("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 
                FROM pg_indexes 
                WHERE tablename = 'todo_items' AND indexname = 'ix_todo_items_id'
            ) THEN
                CREATE INDEX ix_todo_items_id ON todo_items (id);
            END IF;
        END $$;
        """)
    )


def downgrade() -> None:
    # Drop indexes
    op.execute("DROP INDEX IF EXISTS ix_todo_items_id;")
    op.execute("DROP INDEX IF EXISTS ix_users_id;")
    op.execute("DROP INDEX IF EXISTS ix_users_email;")

    # Drop tables
    op.execute("DROP TABLE IF EXISTS todo_items;")
    op.execute("DROP TABLE IF EXISTS users;")

    # Drop types
    op.execute("DROP TYPE IF EXISTS statusenum;")
    op.execute("DROP TYPE IF EXISTS priorityenum;")
