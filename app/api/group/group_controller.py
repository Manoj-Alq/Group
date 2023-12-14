from .group_service import *
from utils.validations import Validations

validation = Validations()

def getGroupController(db,group_id):
    if group_id:
        db_Group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted == False).first()
        if db_Group == None:
            errorhandler(404, "Group not found")

    service = getGroupService(db, group_id)

    return service

def createGroupController(db, group, Auth_head):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    validation.None_validation(group.group_name,group.description, group.is_private,group.members)
    validation.empty_key_validation(group)
    if len(group.members) > 9:
        errorhandler(400, "members size shouldn't exceed above 9")
    if len(group.members) <= 0:
        errorhandler(400,"Group needs member")
    
    members = []
    for member in group.members:
            db_user = db.query(User).filter(User.user_id == member, User.is_deleted == False).first()
            if db_user == None:
                errorhandler(404, f"{member} is not found")
            members.append(db_user)
    
    service = createGroupService(db, group, user_id, members)

    return service

def updateGroupController(db,group, group_id, Auth_head):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted == False).first()
    errorhandler(403, "You're not authorize") if db_group.creator != user_id else None
    service = updateGroupService(db, db_group, group )

    return service

def deleteGroupController(db, Auth_head, group_id):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted == False).first()
    validation.GroupNotFound(db_group)
    errorhandler(403,"You can't delete the group") if db_group.creator != user_id else None
    service = deleteGroupService(db, db_group)

    return service

def addMemberController(db, Auth_head, group_id, id):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_user = db.query(User).filter(User.user_id == id).first()
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted == False).first()
    validation.GroupNotFound(db_group)
    
    if db_group != None:
        validation.admin_check(db,user_id, Members,db_group) if db_group.is_private == True else None
    validation.member_check(db,group_id, Members, user_id,False,id)
    db_member = db.query(Members).filter(Members.group_id == db_group.group_id, Members.user_id == id).first()
    if db_member != None:
        errorhandler(403,"You can't add this user") if db_member.deleted_by == db_group.creator else None
    errorhandler(404, "user not found") if db_user == None else None
    
    service = addMemberService(db,db_user, group_id,user_id,db_member)

    return service

def deleteMemberController(db, Auth_head, group_id, member_id):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_member = db.query(Members).filter(Members.member_id == member_id, Members.is_deleted == False).first()
    errorhandler(404,"Member not found") if db_member == None else None
    db_group = db.query(Group).filter(Group.group_id == group_id,Group.is_deleted == False).first()
    validation.GroupNotFound(db_group)
    validation.member_check(db,group_id, Members,user_id,False)
    if db_group != None:
        validation.admin_check(db,user_id, Members,db_group) if db_group.is_private == True else None
        errorhandler(403,"Creator can't be deleted") if db_group.creator == db_member.user_id else None
    service = deleteMemberService(db,db_member,user_id)

    return service

def leaveFromGroupController(db, Auth_head, group_id, member_id):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_member = db.query(Members).filter(Members.member_id == member_id, Members.is_deleted == False).first()
    errorhandler(404,"Member not found") if db_member == None else None
    db_group = db.query(Group).filter(Group.group_id == group_id).first()
    validation.GroupNotFound(db_group)
    errorhandler(403,"You can't leave another member") if db_member.user_id != user_id else None
    errorhandler(403,"Creator can't leave from group") if db_group.creator == db_member.user_id else None
    validation.member_check(db,group_id, Members,user_id,False,member_id)
    
    service = leaveFromGroupService(db,db_member)

    return service


def reportGroupController(db, Auth_head, group_id,report, report_type):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_group = db.query(Group).filter(Group.group_id == group_id).first()
    validation.member_check(db,group_id, Members, user_id)
    if db_group == None:
        errorhandler(404,"group not found")

    service = reportGroupService(db, user_id, db_group, report_type, report)
    
    return service

def promoteAdminController(db, Auth_head, group_id,id):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted==False).first()
    validation.GroupNotFound(db_group)
    db_member = db.query(Members).filter(Members.member_id == id, Members.is_deleted == False).first()
    validation.memberNotFound(db_member)
    validation.member_check(db,group_id, Members, user_id,True, id)
    validation.admin_check(db,user_id, Members,db_group)
    errorhandler(403, "Already member is a admin") if db_member.is_admin == True else None


    service = promoteAdminService(db,db_group,db_member)

    return service

def depromoteAdminController(db, Auth_head, group_id,member_id):
    user_id = decode_token_id(Auth_head,model=Tokens, db=db)
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted==False).first()
    validation.GroupNotFound(db_group)
    errorhandler(403, "you can't depromote") if db_group.creator != user_id else None
    validation.member_check(db,group_id, Members, user_id,False)
    db_admin = db.query(GroupAdmin).filter(GroupAdmin.member_id == member_id, GroupAdmin.is_deleted == False).first()
    print(db_admin)
    errorhandler(404,"Admin not found") if db_admin == None else None
        
    service = depromoteAdminService(db,db_group,db_admin)

    return service