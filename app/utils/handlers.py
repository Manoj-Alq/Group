from fastapi import HTTPException

def errorhandler(status_code, message):
    raise HTTPException(status_code=status_code, detail=message)

def update_handler(obj, dbObj):

    for key , val in obj:
        if val != "" and val != None:
            setattr(dbObj,f"{key}", f"{val}")
    return