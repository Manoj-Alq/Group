import re
from utils.handlers import errorhandler
from fastapi import UploadFile

class Validations:

        def email_validations(self, email):
            EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$")
            if email:
                if EMAIL_REGEX.match(email):
                    return True
                else:
                    errorhandler(400, "Invalid email")
            
        def password_validation(Self, password):
            PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
            if password:
                if PASSWORD_REGEX.match(password):
                    return True
                else:  errorhandler(400, "Password should contain 8 character, atleast 1 uppercase letter, atleast 1 lowercase letter, atleast 1 symbol")
        
        def phoneNumber_validation(self,phoneNumber):
            pattern = re.compile(r"^\d{10}$")
            if phoneNumber:
                if pattern.match(phoneNumber):
                    return True
                else: errorhandler(400,"Invalid phone number")
                
        def empty_key_validation(self, obj):
            for key, value in obj:
                if value == "":
                    errorhandler(400, f"{key} shoudn't be empty")
                
        def login_validation(Self,user):
            if user.is_active == True:
                errorhandler(400, "You're already loggedin")
            else:
                return False
            
        def User_delete_validation(self, user):
            if user == None:
                errorhandler(404, "User not found")
            if user.is_deleted == True:
                errorhandler(404, "User not found")
                return True
        
        def None_validation(self,*args):
            for i in args:
                if i == None:
                    errorhandler(400, "All fields are required")
                
        def duplication_username_validate(self,db,model,key):
                if key:
                    if len(key ) < 5:
                        errorhandler(400, "username should have more than 5 characters")
                    db_data = db.query(model).filter(model.username == key).first()
                    if db_data:
                        errorhandler(400,"username is not avaiable")
                
        def duplication_email_validate(self,db,model,key):
                db_data = db.query(model).filter(model.email == key).first()
                if db_data:
                    errorhandler(400,"email is not avaiable")
        
        def member_check(self,db,group_id, model, user_id=None,promote=None,id=None):
            db_members = db.query(model).filter(model.group_id == group_id, model.is_deleted == False).all()
            users = [i.user_id for i in db_members]
            print(users)
            members = [i.member_id for i in db_members]
            print(members)
            if user_id not in users:
                errorhandler(403,"You're not authorize")
            if id != None:
                if promote == False:
                    if id in users:
                        errorhandler(400,"member is already in the group")
                if promote == True:
                    if id not in members:
                        errorhandler(404,"member not found in the group")
        
        def admin_check(self,db, id, membermodel,db_group):
            db_member = db.query(membermodel).filter(membermodel.user_id == id, membermodel.group_id == db_group.group_id).first()
            print("member id",db_member.member_id)
            if db_member.is_admin != True:
                errorhandler(403,"you're NNot authorize")
        
        def validate_image(self,file: UploadFile):
            # Validate file type
            allowed_types = {"image/jpeg", "image/png", "image/gif"}
            if file.content_type not in allowed_types:
                errorhandler(400,"Invalid file type. Supported types: JPEG, PNG, GIF")

            # Validate file size
            # max_size = 2 * 1024 * 1024  # 2MB
            # if file.content_length > max_size:
            #     # raise HTTPException(status_code=400, detail="File size exceeds the maximum allowed size (2MB)")
            #     errorhandler(400,"File size exceeds the maximum allowed size (2MB)")
        
        def GroupNotFound(self,db_group):
            errorhandler(404, "Group not found") if db_group == None else None     
                
        def memberNotFound(self,db_member):
            errorhandler(404, "Member not found") if db_member == None else None      
        
        def AlreadyAdmin(self,db_member):
            errorhandler(403, "Already member is a admin") if db_member.is_admin == True else None
        