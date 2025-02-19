from fastapi import HTTPException, status, Request
from postgrest import APIError
import logging

from supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


def supabase_login_required(request: Request):
    """
    Checks if a user is in the session and returns the user data
    """
    user_id = request.session.get("supabase_user")
    if not user_id:
        logger.warning("No user_id found in session")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    try:
        profile = get_supabase_client().auth.get_user()

        if not profile.user.aud:
            logger.error(f"No profile found for user_id: {user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        return profile.user

    except APIError as e:
        logger.error(f"Database error in auth check: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )
