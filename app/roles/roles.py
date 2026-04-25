from fastapi import APIRouter, Depends
from app.dependencies import require_role

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/admin-only")
def admin_route(user = Depends(require_role("admin"))):
    return {"message": "Welcome Admin"}


@router.get("/user-only")
def user_route(user = Depends(require_role("user"))):
    return {"message": "Welcome User"}