from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/templates", tags=["templates"])
templates = Jinja2Templates(directory="templates")

@router.get("/{role}", response_class=HTMLResponse)
async def get_role_template(request: Request, role: str):
    mapping = {
        "ssk": "form_ssk.html",
        "iko": "form_iko.html",
        "prorab": "form_prorab.html",
        "foreman": "form_prorab.html"
    }
    template_name = mapping.get(role, "form_prorab.html" if role in ("prorab", "foreman") else "form_ssk.html")
    email = request.query_params.get("email", "")
    return templates.TemplateResponse(template_name, {"request": request, "role": role, "email": email})
