from .user_model import *
from utils.handlers import *
from utils.auth_handlers import *
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.orm import defer

expiry_del = ACCESS_TOKEN_EXPIRY_MINUTES

def getUserService(db, id):
    try:
        if id != None:
            db_user = db.query(User).filter(User.user_id == id, User.is_deleted == False).options(defer(User.password)).first()
            return  db_user
        else:
            db_users = db.query(User).filter(User.is_deleted == False).options(defer(User.password)).all()
            return db_users
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def signupuserService(db, user):
    try:
        db_user = User(
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
            phonenumber = user.phonenumber,
            username = user.username,
            bio = user.bio,
            password = hash_password(user.password),
            is_active = False,
            is_deleted = False,
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return JSONResponse({
            "message": "user created successfully"
        })
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def logInuserService(db, db_user):
    try:
        db_user.is_active = True 
        access_token = create_access_token(data={"sub": str(db_user.user_id),"role": "user"}, expires_delta=expiry_del)
        db_token = Tokens(user_id=db_user.user_id, token=access_token)
        db.add(db_token)
        db.commit()
        return JSONResponse({
            "message":"User loggedin successfully",
            "user":{
                "username":db_user.username,
                "access_token": access_token, 
                "token_type": "bearer"}
            })
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def getMyProfileService(db, db_user):
    try:
        return db_user
    except Exception as e:
        db.rollback()
        errorhandler(400,f"{e}")

def updateUserService(db, user, db_user):
    try:
        update_handler(user, db_user)
        db.commit()
        return JSONResponse({
            "message": "author updated successfully"
        })
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def logoutUserService(db, db_user):
    try:
        db_user.is_active = False
        db_token = db.query(Tokens).filter(
            Tokens.user_id == db_user.user_id).first()
        if db_token != None:
            db.delete(db_token)
        db.commit()
        return JSONResponse({
            "message": "logged out successfully"
        })
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def  deleteUserService(db, db_user):
    try:
        db_user.is_deleted = True
        db.commit()
        return JSONResponse({
            "message": "author deleted successfully"
        })
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")