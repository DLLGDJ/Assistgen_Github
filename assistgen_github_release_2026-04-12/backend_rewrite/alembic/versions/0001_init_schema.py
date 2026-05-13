"""init schema

Revision ID: 0001_init_schema
Revises:
Create Date: 2026-04-11 00:00:00
"""

from __future__ import annotations

from alembic import op

# revision identifiers, used by Alembic.
revision = "0001_init_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS knowledge_items (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_conversations_user_updated
        ON conversations(user_id, updated_at DESC, created_at DESC, id DESC)
        """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_messages_conversation_created
        ON messages(conversation_id, created_at ASC, id ASC)
        """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_knowledge_created
        ON knowledge_items(created_at DESC, id DESC)
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_knowledge_created")
    op.execute("DROP INDEX IF EXISTS idx_messages_conversation_created")
    op.execute("DROP INDEX IF EXISTS idx_conversations_user_updated")
    op.execute("DROP TABLE IF EXISTS knowledge_items")
    op.execute("DROP TABLE IF EXISTS messages")
    op.execute("DROP TABLE IF EXISTS conversations")

