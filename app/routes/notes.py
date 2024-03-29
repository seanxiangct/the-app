from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import crud.notes as crud
from auth.jwthandler import get_current_user
from schemas.notes import NoteOutSchema, NoteInSchema, UpdateNote
from schemas.token import Status
from schemas.users import UserOutSchema


router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.get(
    "/",
    response_model=List[NoteOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_notes(status: str = None):
    if status:
        return await crud.get_notes(status=status)
    else: 
        return await crud.get_notes()


@router.get(
    "/{note_id}",
    response_model=NoteOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_note(note_id: int) -> NoteOutSchema:
    try:
        return await crud.get_note(note_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Note does not exist",
        )


@router.post(
    "/", response_model=NoteOutSchema, dependencies=[Depends(get_current_user)]
)
async def create_note(
    note: NoteInSchema, current_user: UserOutSchema = Depends(get_current_user)
) -> NoteOutSchema:
    return await crud.create_note(note, current_user)


@router.patch(
    "/{note_id}",
    dependencies=[Depends(get_current_user)],
    response_model=NoteOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_note(
    note_id: int,
    note: UpdateNote,
    current_user: UserOutSchema = Depends(get_current_user),
) -> NoteOutSchema:
    return await crud.update_note(note_id, note, current_user)

@router.patch(
    "/{note_id}/complete",
    dependencies=[Depends(get_current_user)],
    response_model=NoteOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def complete_note(
    note_id: int,
    current_user: UserOutSchema = Depends(get_current_user),
) -> NoteOutSchema:
    return await crud.update_note(note_id, UpdateNote(status="complete"), current_user)

@router.delete(
    "/{note_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_note(
    note_id: int, current_user: UserOutSchema = Depends(get_current_user)
):
    return await crud.delete_note(note_id, current_user)