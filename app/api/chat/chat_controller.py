from .chat_service import *
from utils.validations import Validations

validation = Validations()

def getChatController(db,Auth_head,group_id):
    user_id = decode_token_id(Auth_head,model=Tokens,db=db)
    db_member_id = db.query(Members).filter(Members.group_id == group_id, Members.user_id == user_id, Members.is_deleted == False).first()
    errorhandler(403,"You can't get chats of this group") if db_member_id == None else None
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted == False).first()
    validation.GroupNotFound(db_group)
    db_chat = db.query(Chat).filter(Chat.group_id == group_id, Chat.is_deleted == False).order_by(Chat.chat_id.desc()).limit(10).all()
    if db_chat == []:
        return "chats are empty" 
    
    service = getChatService(db,db_chat)

    return service

def createChatController(db, Auth_head,group_id, file, description):
    user_id = decode_token_id(Auth_head,model=Tokens,db=db)
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted == False).first()
    validation.GroupNotFound(db_group)
    validation.member_check(db,db_group.group_id,Members,user_id)
    db_member = db.query(Members).filter(Members.user_id == user_id,group_id==group_id, Members.is_deleted == False).first()
    validation.memberNotFound(db_member)

    validation.validate_image(file)

    service = createChatService(db,file, description, db_member, db_group)
    return service

def shareChatController(db, Auth_head,group_id,chat_id):
    user_id = decode_token_id(Auth_head,model=Tokens,db=db)
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted == False).first()
    validation.GroupNotFound(db_group)
    validation.member_check(db,db_group.group_id,Members,user_id)
    db_member = db.query(Members).filter(Members.user_id == user_id,group_id==group_id, Members.is_deleted == False).first()
    validation.memberNotFound(db_member)
    db_chat = db.query(Chat).filter(Chat.chat_id == chat_id,Chat.is_deleted == False).first()
    errorhandler(404,"Chat not found") if db_chat == None else None
    validation.member_check(db,db_chat.group_id,Members,user_id)
    service = shareChatService(db,db_chat, db_member, db_group,user_id)

    return service

def getGroupsSharedChatController(db,chat_id):
    db_chats = db.query(Chat, Group).join(Group, Chat.group_id == Group.group_id).filter(Chat.shared_chat_id == chat_id,Chat.is_deleted == False).all()
    print(db_chats)

    service = getGroupsSharedChatService(db,db_chats)

    return service

def deleteChatController(db, Auth_head,chat_id,group_id):
    user_id = decode_token_id(Auth_head,model=Tokens,db=db)
    db_member_id = db.query(Members).filter(Members.group_id == group_id, Members.user_id == user_id, Members.is_deleted == False).first()
    errorhandler("Member not found") if db_member_id == None else None
    print(db_member_id.member_id)
    result = db.query(Chat,Members,Group).join(Members, Chat.member_id == Members.member_id).join(Group, Chat.group_id == Group.group_id).filter(Chat.chat_id == chat_id,Group.is_deleted == False, Chat.is_deleted == False).first()
    if result is not None:
        db_chat, db_member, db_group = result
    else:
        db_chat, db_member, db_group = None, None, None
        raise HTTPException(status_code=404, detail="cChat not found")
    print("member_id",db_member.member_id)
    if db_member_id.is_admin != True:
        errorhandler(403,"You can't delete others chat") if db_chat.member_id != db_member_id.member_id else None
        errorhandler(403,"You're Not authorize") if db_member.user_id != user_id else None
        errorhandler(403,"you're not a member") if db_member_id.group_id != group_id else None
    

    
    service = deleteChatService(db,db_chat,user_id)

    return service
