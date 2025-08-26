"""
Functions to call while starting the fastapi server.
"""
from pymongo import ASCENDING
from database import database

def init_indexes():
    """
    Initialize database indexes.
    """
    SIX_MONTHS_IN_SECONDS = 6 * 30 * 24 * 60 * 60  # Approximation of six months
    database["users"].create_index(
        [("id", ASCENDING)],
        unique=True,
        name="unique_id_idx"
    )
    database["users"].create_index(
        [("email", ASCENDING)],
        unique=True,
        name="unique_email_idx"
    )
    database["users"].create_index(
        [("username", ASCENDING)],
        unique=True,
        name="unique_username_idx"
    )
    database["blacklisted_tokens"].create_index(
        [("token", ASCENDING)],
        unique=True,
        name="unique_token_idx"
    )
    database["blacklisted_tokens"].create_index(
        [("created_at", ASCENDING)],
        expireAfterSeconds=SIX_MONTHS_IN_SECONDS,
        name="token_ttl_idx"
    )