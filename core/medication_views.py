import logging
from datetime import datetime

from fastapi import File, UploadFile, Depends, FastAPI
from fastapi import Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from decorators import supabase_login_required
from ocr_service import recognise
from supabase_client import get_supabase_client


class MedicationRoutes:
    def __init__(self, app: FastAPI, templates: Jinja2Templates):
        logger = logging.getLogger(__name__)

        @app.post("/upload-image", name="upload")
        async def upload_image(
            request: Request, image: UploadFile = File(...), user=Depends(supabase_login_required)
        ):
            try:
                if not image.content_type.startswith("image/"):
                    return templates.TemplateResponse(
                        "upload.html",
                        {"request": request, "messages": ["Please upload a valid image file."]},
                        status_code=400,
                    )

                # Process the image
                active_ingredients = recognise(image)

                # Store in Supabase
                profile = (
                    get_supabase_client()
                    .from_("profiles")
                    .select("*")
                    .eq("user_id", user.id)
                    .execute()
                ).data[0]

                # Save medication record
                get_supabase_client().from_("medication").insert(
                    {
                        "profile_id": profile["id"],
                        "active_ingredients": active_ingredients,
                        "scan_date": datetime.now().isoformat(),
                    }
                ).execute()

                # Store results in session for display
                request.session["active_ingredients"] = active_ingredients

                return RedirectResponse(url="/result", status_code=status.HTTP_303_SEE_OTHER)

            except Exception:
                logger.exception("Upload error:")
                return templates.TemplateResponse(
                    "upload.html",
                    {"request": request, "messages": ["Error processing image. Please try again."]},
                    status_code=500,
                )

        @app.get("/upload-image", name="upload")
        async def upload_image(request: Request):
            return templates.TemplateResponse("upload.html", {"request": request})

        @app.get("/dashboard", name="dashboard", response_class=HTMLResponse)
        async def user_dashboard(request: Request, user=Depends(supabase_login_required)):
            logger.info(f"Accessing dashboard with user: {user.id}")
            try:

                profile = (
                    get_supabase_client()
                    .from_("profiles")
                    .select("*")
                    .eq("user_id", user.id)
                    .execute()
                ).data[0]

                medications = (
                    get_supabase_client()
                    .from_("medication")
                    .select("*")
                    .eq("profile_id", profile["id"])
                    .execute()
                ).data

                response = templates.TemplateResponse(
                    "dashboard.html", {"request": request, "medications": medications, "user": user}
                )
                return response

            except Exception:
                logger.exception("Dashboard error:")
                response = RedirectResponse(
                    url="/login?error=Error loading dashboard",
                    status_code=status.HTTP_303_SEE_OTHER,
                )
                response.headers["Location"] = "/login?error=Error loading dashboard"
                return response

        @app.get("/result", name="result", response_class=HTMLResponse)
        async def show_result(request: Request):
            ingredients = request.session.get("active_ingredients", [])
            return templates.TemplateResponse(
                "result.html", {"request": request, "active_ingredients": ingredients}
            )
