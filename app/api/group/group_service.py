from .group_model import *
from utils.auth_handlers import errorhandler
from api.user.user_model import *
from utils.auth_handlers import *

def getGroupService(db, id):
    try:
        if id != None:
            db_Group = db.query(Group, Members, User).join(Members, Group.group_id == Members.group_id).join(User, Members.user_id == User.user_id).filter(Group.group_id == id,Members.is_deleted==False, Group.is_deleted == False, User.is_deleted == False).all()
            print(db_Group)
            if db_Group == None:
                return
            group_data = {
            "group_id": db_Group[0][0].group_id,
            "group_name": db_Group[0][0].group_name,
            "group_description": db_Group[0][0].description,
            "creator":db_Group[0][0].creator
            }

            member_data = [
                {
                    "member_id": member.member_id, 
                    "user_id": member.user_id,
                    "user_name":user.username,
                    "group_id":member.group_id,
                    "is_admin":member.is_admin,
                    "Joined_at":member.created_at.isoformat()
                } for group, member, user in db_Group
            ]

            response_data = {"group": group_data, "members": member_data}
            return JSONResponse(content=response_data)
        else:
            db_Groups = db.query(Group).filter(Group.is_deleted == False).all()
            return db_Groups
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def createGroupService(db, group, user_id, members):
    # try:
        db_group = Group(
            group_name = group.group_name,
            description = group.description,
            creator = user_id,
            is_private = group.is_private,
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            created_by = user_id
        )
        db.add(db_group)
        db.flush()
        for member in members:
            db_member = Members(
                user_id = member.user_id,
                group_id = db_group.group_id,
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                created_by = db_group.creator
            )
            db.add(db_member)
        db_member = Members(
                user_id = user_id,
                group_id = db_group.group_id,
                is_admin = True,
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                created_by = db_group.creator
            )
        db.add(db_member)
        db.commit()
        db.refresh(db_group)

        return db_group
    # except Exception as e:
    #     db.rollback()
    #     errorhandler(400, f"{e}")

def  updateGroupService(db, db_group, group ):
    try:
        update_handler(group, db_group)
        db.commit()
        return "updated succesfully"
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def deleteGroupService(db, db_group):
    try:
        db_group.is_deleted = True
        db.commit()
        return JSONResponse({
            "message": "Group deleted successfully"
        })
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def addMemberService(db,db_user,group_id,user_id,db_member):
    try:
        if db_member:
            db_member.is_deleted = False
            db_member.deleted_by = None
            db.commit()
        else:
            db_member = Members(
                user_id = db_user.user_id,
                group_id = group_id,
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                created_by = user_id
            )
            db.add(db_member)
            db.commit()
            db.refresh(db_member)
        return "successfully addedd member"
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def deleteMemberService(db,db_member, user_id):
    try:
        db_member.is_deleted = True
        db_member.deleted_by = user_id
        db.commit()
        return "Member deleted successfully"
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def leaveFromGroupService(db,db_member):
    try:
        db_member.is_deleted = True
        db.commit()
        return "leaved successfully"
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")


def reportGroupService(db, user_id, db_group, report_type, report):
    try:
        db_report = Report(
            user_id = user_id,
            group_id = db_group.group_id,
            report_type = report_type,
            report = report.reason,
            reported_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)

    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def promoteAdminService(db,db_group,db_member):
    try:
        db_admin = GroupAdmin(
            group_id = db_group.group_id,
            member_id = db_member.member_id,
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db_member.is_admin = True
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)

        return "promoted successfully"
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def depromoteAdminService(db,db_group,db_admin):
    try:
        db_admin.is_deleted = True
        db.commit()
        return "Depromoted admin successfully"
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")