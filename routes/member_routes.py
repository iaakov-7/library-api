from fastapi import APIRouter,HTTPException
import mysql.connector
from database.member_db import db_member
from logs.logger_config import logger
from utils.models import Member, UpdateMember

router = APIRouter(tags=["Members"])

@router.get("")
def gat_all_members():
    logger.info("Incoming request: get all members")
    members = db_member.get_all_members()
    if len(members) == 0:
        logger.warning("There are no members")
    logger.info("Read all members successfully")    
    return members

@router.get("/{id}") 
def get_member_by_id(id:int):
    logger.info("Incoming request: member %s",id)
    member = db_member.get_member_by_id(id)
    if not member:
        logger.error("Member %s not found",id)
        raise HTTPException(404,f"Member with id {id} not found") 
    logger.info("Read member %s successfully",id)
    return member

@router.post("",status_code=201)
def create_member(new_member:Member):
    logger.info("Incoming request: create new member")
    member = new_member.model_dump()
    try:
        new_id = db_member.create_member(member)
    except mysql.connector.errors.IntegrityError:
          logger.error("Email is already exist")
          raise HTTPException(409,"This email is already exist")
    logger.info("Created member %s successfully",new_id)            
    return {"Success":f"Created new member with id {new_id}"} 

@router.patch("/{id}")
def update_member(id:int,to_update:UpdateMember):
    logger.info("Incoming request: update member %s",id)
    if not db_member.get_member_by_id(id):
        logger.error("Member %s not found",id)
        raise HTTPException(404,f'Member with id {id} not found')
    member_to_update = to_update.model_dump(exclude_unset=True)
    updated = db_member.update_member(id,member_to_update)
    if not updated:
        raise HTTPException(400,"Bad request")
    logger.info("Update member %s successfully",id)
    return {"Success":"Member updated successfully"}

@router.patch("/{id}/deactivate")
def deactivate_member(id:int):
    logger.info("Incoming request: deactive member %s",id)
    if not db_member.get_member_by_id(id):
        logger.error("Member %s not found",id)
        raise HTTPException(404,f'Member with id {id} not found')
    db_member.deactivate_member(id)
    logger.info("Deactived successfully member %s",id)
    return {"Success":"Member deactivated successfully"}

@router.patch("/{id}/activate")
def deactivate_member(id:int):
    logger.info("Incoming request: active member %s",id)
    if not db_member.get_member_by_id(id):
        logger.error("Member %s not found",id)
        raise HTTPException(404,f'Member with id {id} not found')
    db_member.activate_member(id)
    logger.info("Actived successfully member %s",id)
    return {"Success":"Member activate successfully"}
