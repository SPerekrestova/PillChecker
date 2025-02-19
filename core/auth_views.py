import logging

from fastapi import Request, Depends, Form, status, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from postgrest import APIError
from starlette.templating import Jinja2Templates

from auth_service import sign_up_user, sign_in_user
from core.supabase_client import get_supabase_client
from decorators import supabase_login_required
from forms import ProfileUpdateForm


class SupabaseAuthRoutes:
    def __init__(self, app: FastAPI, templates: Jinja2Templates):
        logger = logging.getLogger(__name__)

        @app.post("/signup", name="signup", response_class=HTMLResponse)
        def supabase_signup_view(request):
            email = request.POST.get("email")
            password = request.POST.get("password")
            username = request.POST.get("username", email)
            try:
                result = sign_up_user(email, password)
                if result and hasattr(result, "user"):
                    request.session["supabase_user"] = result.user.id
                    request.user = result.user

                    # Create profile using Supabase
                    get_supabase_client().from_("profiles").insert(
                        {"user_id": result.user.id, "display_name": username}
                    ).execute()

                    logger.success(request, "Signed up successfully. Please log in.")
                    return RedirectResponse(url="/login", status_code=status.HTTP_200_OK)
                else:
                    logger.error(request, "Sign-up failed. Check your email/password.")
                    return RedirectResponse(
                        url="/signup?error=Sign-up failed. Check your email/password.",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
            except APIError as e:
                logger.error(request, f"Database error: {str(e)}")
                return RedirectResponse(
                    url="/signup?error=Database error occurred",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            except Exception as e:
                logger.error(request, f"Sign-up error: {str(e)}")
                return RedirectResponse(
                    url="/signup?error=Sign-up error occurred",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        @app.get("/signup", name="signup", response_class=HTMLResponse)
        def supabase_signup_view():
            return RedirectResponse(url="/signup", status_code=status.HTTP_200_OK)

        @app.post("/login", name="login", response_class=HTMLResponse)
        async def supabase_login_view(
            request: Request,
            email: str = Form(...),
            password: str = Form(...),
        ):
            logger.info(f"Login attempt for user: {email}")
            try:
                result = sign_in_user(email, password)
                if result and hasattr(result, "user"):
                    # Set session data
                    request.session["supabase_user"] = result.user.id
                    request.session["user"] = {
                        "id": result.user.id,
                        "email": result.user.email,
                    }

                    logger.info(f"User {email} logged in successfully, redirecting to dashboard")
                    response = RedirectResponse(
                        url="/dashboard", status_code=status.HTTP_303_SEE_OTHER
                    )
                    # The session middleware will automatically handle saving the session
                    response.headers["Location"] = "/dashboard"
                    return response
                else:
                    logger.error("Invalid credentials or login failed.")
                    response = RedirectResponse(
                        url="/login?error=Invalid credentials",
                        status_code=status.HTTP_303_SEE_OTHER,
                    )
                    response.headers["Location"] = "/login?error=Invalid credentials"
                    return response
            except Exception:
                logger.exception(f"Login error for user {email}")
                response = RedirectResponse(
                    url="/login?error=Login error occurred", status_code=status.HTTP_303_SEE_OTHER
                )
                response.headers["Location"] = "/login?error=Login error occurred"
                return response

        @app.get("/login", name="login", response_class=HTMLResponse)
        def get_supabase_login_view(request: Request):
            return templates.TemplateResponse("login.html", {"request": request})

        @app.post("/logout", name="logout", response_class=HTMLResponse)
        def supabase_logout_view(request: Request):
            response = get_supabase_client().auth.sign_out()
            return RedirectResponse(url="/logout", status_code=status.HTTP_200_OK)

        @app.get("/logout", name="logout", response_class=HTMLResponse)
        def supabase_logout_view(request: Request):
            return templates.TemplateResponse("logout.html", {"request": request})

        @app.post("/profile/update", name="update_profile", response_class=HTMLResponse)
        async def update_profile(
            profile_updates: ProfileUpdateForm, user=Depends(supabase_login_required)
        ):
            try:
                # Check if profile exists
                profile = (
                    get_supabase_client()
                    .from_("profiles")
                    .select("*")
                    .eq("user_id", user.id)
                    .single()
                )
                if not profile:
                    return RedirectResponse(
                        url="/profile/update?error=Profile does not exist.",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )

                # Update profile using Supabase
                get_supabase_client().from_("profiles").update(
                    {"display_name": profile_updates.display_name, "bio": profile_updates.bio}
                ).eq("user_id", user.id).execute()

            except APIError as e:
                logger.error(f"Database error: {str(e)}")
                return RedirectResponse(
                    url="/profile/update?error=Database error occurred",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            except Exception:
                logger.exception("Profile update error:")
                return RedirectResponse(
                    url="/profile/update?error=Profile update error occurred",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            return RedirectResponse(url="/dashboard", status_code=status.HTTP_200_OK)
