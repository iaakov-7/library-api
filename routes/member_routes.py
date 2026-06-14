from fastapi import APIRouter,HTTPException
import mysql.connector
from database.member_db import db_member
from logs.logger_config import logger
from utils.models import Member, UpdateMember

router = APIRouter(tags=["Members"])

@router.get("")
def gat_all_members():
    members = db_member.get_all_members()
    if len(members) == 0:
        logger.warning("There are no members")
    return members

@router.get("/{id}") 
def get_member_by_id(id:int):
    member = db_member.get_member_by_id(id)
    if not member:
        raise HTTPException(404,f"Member with id {id} not found") 
    return member

@router.post("")
def create_member(new_member:Member):
    member = new_member.model_dump()
    try:
        new_id = db_member.create_member(member)
    except mysql.connector.errors.IntegrityError:
          raise HTTPException(400,"This email is already exist")            
    return {"Success":f"Created new member with id {new_id}"} 

@router.patch("/{id}")
def update_member(id:int,to_update:Member):
    if not db_member.get_member_by_id(id):
        raise HTTPException(404,f'Member with id {id} not found')
    member_to_update = to_update.model_dump(exclude_unset=True)
    updated = db_member.update_member(id,member_to_update)
    if not updated:
        raise HTTPException(400,"Bad request")
    return {"Success":"Member updated successfully"}

@router.patch("/{id}/deactivate")
def deactivate_member(id:int):
    if not db_member.get_member_by_id(id):
        raise HTTPException(404,f'Member with id {id} not found')
    db_member.deactivate_member(id)
    return {"Success":"Member deactivate successfully"}

@router.patch("/{id}/activate")
def deactivate_member(id:int):
    if not db_member.get_member_by_id(id):
        raise HTTPException(404,f'Member with id {id} not found')
    db_member.activate_member(id)
    return {"Success":"Member activate successfully"}
