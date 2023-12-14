from api.group.group_model import *
from .chat_model import *
from api.user.user_model import *
from utils.auth_handlers import *
import os

def getChatService(db,db_chat):
    try:
        return db_chat
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def getGroupsSharedChatService(db,db_chats):
    group_data = [
                {
                    "group_id": group.group_id, 
                    "group_name":group.group_name,
                    "description": group.description,
                    "Joined_at":group.created_at.isoformat()
                } for chat, group in db_chats
            ]
    response_data = {"Groups": group_data}
    return JSONResponse(content=response_data)

def createChatService(db,file, description,db_member,db_group):
    try:
        # file_path = os.path.join("uploads", file.filename)
        # # if not os.path.exists(file_path):
        # #     os.makedirs(file_path)
        # print(file_path)
        with open(f"D:/practice/projects/Group/uploads/{datetime.now().date()}_{db_member.member_id}_{file.filename}", "wb") as f:
            f.write(file.file.read())
        db_chat = Chat(
            member_id = db_member.member_id,
            group_id = db_group.group_id,
            image = f"D:/practice/projects/Group/uploads/{file.filename}",
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            created_by = db_member.member_id
        )
        db.add(db_chat)
        db.commit()
        db.refresh(db_chat)

        return "Image sent successfully"
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")

def shareChatService(db,db_chat, db_member, db_group):
    try:
        db_share = Chat(
            member_id = db_member.member_id,
            group_id = db_group.group_id,
            image = db_chat.image,
            is_shared = True,
            shared_chat_id = db_chat.chat_id,
        )
        db_chat.shared_count += 1
        db.add(db_share)
        db.commit()
        db.refresh(db_share)

        return "shared successfully"
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")
    

def deleteChatService(db,db_chat):
    try:
        db_chat.is_deleted = True
        db.commit()
    except Exception as e:
        db.rollback()
        errorhandler(400, f"{e}")