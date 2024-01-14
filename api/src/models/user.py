from __future__ import annotations

import uuid
from enum import IntEnum
from typing import Union

from sqlalchemy import Column, String, select
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy_utils.types.password import PasswordType

from database.base_class import Base

from .mixins import TimeStampMixin


class SexType(IntEnum):
    MAN = 0
    WOMAN = 1
    OTHER = 2

    @classmethod
    def from_str(cls, input_string: str) -> Union[int, None]:
        try:
            return cls[input_string.upper()]
        except KeyError:
            return None

    @classmethod
    def get_label(cls, value: int) -> Union[str, None]:
        for member in cls:
            if member.value == value:
                return member.name
        return None  # 一致するラベルが見つからない場合


class User(Base, TimeStampMixin):

    @declared_attr
    def __table_args__(self):  # noqa:U100
        args = Base.__table_args__[0]
        return (
            {**args, "comment": "ユーザー"},
        )

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    username = Column(
        String(255, collation="utf8mb4_bin"),
        unique=True,
        nullable=True
    )
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt']
    ))
    sex = Column(ChoiceType(SexType, impl=TINYINT()), nullable=True)
    age = Column(TINYINT, nullable=True)
    # is_active = Column(Boolean, default=True, nullable=False)  # noqa:E800

    def convert_output(self):
        self.id = str(self.id)
        self.password = "*****"
        return self

    @classmethod
    async def read_by_id(
        cls, db: AsyncSession, user_id: int
    ) -> 'User' | None:
        stmt = select(cls).where(cls.id == user_id)
        return await db.scalar(stmt.order_by(cls.id))
