from .chat_service import *
from utils.validations import Validations

validation = Validations()

def getChatController(db,group_id):
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted == False).first()
    if db_group == None:
        errorhandler(404,"Group not found")
    db_chat = db.query(Chat).filter(Chat.group_id == group_id, Chat.is_deleted == False).order_by(Chat.chat_id.desc()).limit(2).all()
    if db_chat == []:
        return "chats are empty"
    
    service = getChatService(db,db_chat)

    return service

def createChatController(db, Auth_head,group_id, file, description):
    user_id = decode_token_id(Auth_head,model=Tokens,db=db)
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted == False).first()
    if db_group == None:
        errorhandler(404,"Group not found")
    validation.member_check(db,db_group.group_id,Members,user_id)
    db_member = db.query(Members).filter(Members.user_id == user_id,group_id==group_id, Members.is_deleted == False).first()
    print(db_member.member_id)

    validation.validate_image(file)

    service = createChatService(db,file, description, db_member, db_group)
    return service

def shareChatController(db, Auth_head,group_id,chat_id):
    user_id = decode_token_id(Auth_head,model=Tokens,db=db)
    db_group = db.query(Group).filter(Group.group_id == group_id, Group.is_deleted == False).first()
    if db_group == None:
        errorhandler(404,"Group not found")
    validation.member_check(db,db_group.group_id,Members,user_id)
    db_member = db.query(Members).filter(Members.user_id == user_id,group_id==group_id, Members.is_deleted == False).first()
    if db_member == None:
        errorhandler(404,"member not found")
    db_chat = db.query(Chat).filter(Chat.chat_id == chat_id).first()
    validation.member_check(db,db_chat.group_id,Members,user_id)
    if db_chat == None:
        errorhandler(404,"chat not found")
    service = shareChatService(db,db_chat, db_member, db_group)
    return service

def getGroupsSharedChatController(db,chat_id):
    db_chats = db.query(Chat, Group).join(Group, Chat.group_id == Group.group_id).filter(Chat.shared_chat_id == chat_id,Chat.is_deleted == False).all()
    print(db_chats)

    service = getGroupsSharedChatService(db,db_chats)

    return service

def deleteChatController(db, Auth_head,chat_id):
    user_id = decode_token_id(Auth_head,model=Tokens,db=db)
    db_chat, db_member, db_group= db.query(Chat,Members,Group).join(Members, Chat.member_id == Members.member_id).join(Group, Chat.group_id == Group.group_id).filter(Chat.chat_id == chat_id, Chat.is_deleted == False).first()
    print(db_chat)
    if db_member.user_id != user_id:
        errorhandler(403,"You're not authorize")
    if db_member.group_id != db_group.group_id:
        errorhandler(403,"you're nt member")

    
    service = deleteChatService(db,db_chat)

    return service
