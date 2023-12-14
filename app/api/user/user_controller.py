from .user_service import *
from utils.validations import *

validation = Validations()

#getUser
def getUserController(db, id):
    if id:
        db_user = db.query(User).filter(User.user_id == id, User.is_deleted == False).first()
        if db_user == None:
            errorhandler(404, "user not found")

    return getUserService(db, id)

#CreatUser
def createUserController(db,user):
    validation.None_validation(user.first_name,user.last_name,user.email,user.bio,user.phonenumber,user.username,user.password,user.profile_pic)
    validation.empty_key_validation(user)
    validation.duplication_username_validate(db,User,user.username)
    validation.email_validations(user.email)
    validation.duplication_email_validate(db,User,user.email)
    validation.phoneNumber_validation(user.phonenumber)
    validation.password_validation(user.password)

    service = signupuserService(db, user)

    return service

#loginUser
def logInuserController(db,user):
    validation.None_validation(user.username,user.password)
    validation.empty_key_validation(user)
    db_user = authenticate_user(db,user.username, user.password,User)
    validation.User_delete_validation(db_user)
    validation.login_validation(db_user)

    service = logInuserService(db,db_user)

    return service

#myprofile
def getMyProfileController(db,Auth_head):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_user = db.query(User).filter(User.user_id == user_id).first()
    validation.User_delete_validation(db_user)

    service = getMyProfileService(db, db_user)

    return  service

#updateUser
def updateUserController(db,user,Auth_head,id):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_user = db.query(User).filter(User.user_id == id).first()

    validation.User_delete_validation(db_user)
    validation.duplication_username_validate(db,User,user.username)
    validation.email_validations(user.email)
    validation.duplication_email_validate(db,User,user.email)
    validation.phoneNumber_validation(user.phonenumber)
    validation.password_validation(user.password)


    # service = updateUserService(db, user, db_user )

    return "  "

#logoutUser
def logoutuserController(db,Auth_head,id):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_user = db.query(User).filter(User.user_id == id).first()
    validation.User_delete_validation(db_user)

    if db_user.is_active == False:
            errorhandler(400, f"{id} is not loggedin yet")

    service = logoutUserService(db, db_user)

    return service

#deleteUser
def deleteUserController(db,Auth_head,id):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_user = db.query(User).filter(User.user_id == id, User.is_deleted == False).first()
    if db_user == None:
        errorhandler(404,"user not found")

    service = deleteUserService(db, db_user)

    return service