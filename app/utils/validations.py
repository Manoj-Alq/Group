import re
from utils.handlers import errorhandler

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
                