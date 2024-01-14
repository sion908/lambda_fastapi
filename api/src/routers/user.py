from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import create_user_query
from database.db import get_db
from dependencies import verify_from_api
from models import User
from schemas import user as sc_user
from schemas.user import OutputUser  # これは廃止予定
from setting import Tags

router = APIRouter()


@router.post(
    "/users/",
    response_model=sc_user.OutputUser,
    tags=[Tags.user],
)
async def create_user(
    user: sc_user.UserCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(verify_from_api),  # NOQA: U101
) -> sc_user.OutputUser:
    """
    Create a user with each the information:

    - **username**(str):
    - **password**(str):
    - **sex**(int): [男性:0,女性:1,その他2]
    - **age**(int):
    """
    user = await create_user_query(db=db, user=user)
    return OutputUser.model_validate(user.convert_output())


@router.get(
    "/users/{user_id}",
    response_model=sc_user.OutputUser,
    description="ユーザーIDを元にユーザー情報を取得する。",
    tags=[Tags.user],
)
async def read_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    _=Depends(verify_from_api),  # NOQA: U101
) -> sc_user.OutputUser:
    user = await User.read_by_id(db=db, user_id=user_id)

    if user:
        return sc_user.OutputUser.model_validate(user.convert_output())
    else:
        return JSONResponse(content={"notFound": "指定されたユーザーが存在しません"}, status_code=404)
