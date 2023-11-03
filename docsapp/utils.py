
def getUserArray(tag) -> list:
    user_array : list = []
    for user in tag.users.all():
        user_array.append(user.user.username)
    return user_array

def isWriter(uname : str, write_tags) -> bool:
    for write_tag in write_tags.all():
            usernames = getUserArray(write_tag)
            if uname in usernames:
                return uname in usernames
    return False    
    
def isReader(uname : str, read_tags) -> bool:
    for read_tag in read_tags.all():
        usernames = getUserArray(read_tag)
        if uname in usernames:
            return uname in usernames
    return False   

def isReadPermsChange(incoming_readers : list, doc) -> bool:
    print(f"The received doc is {doc}")
    print(f"It has tags like {doc.read_tags.all()}")
    current_readers = []
    for tag in doc.read_tags.all():
        current_readers.append(tag.name)
    return incoming_readers == current_readers

def isWritePermsChange(incoming_writers : list, doc) -> bool:
    current_writers = []
    for tag in doc.write_tags.all():
        current_writers.append(tag.name)
    return incoming_writers == current_writers

def isRestrictionChange(incoming_restriction : bool, doc) -> bool:
    return incoming_restriction != doc.restricted
def isAdmin(uname : str ,tag) -> bool:
    for admin in tag.admins.all():
        if(uname == admin.prof_username):
            return True 
    return False 

def isCreator(uname : str , obj) -> bool:
    return uname == obj.creator.prof_username

def isAccessible(uname : str, doc) -> bool:
    is_restricted_and_creator : bool = doc.restricted and uname == doc.creator.prof_username
    return (not doc.restricted) or is_restricted_and_creator
