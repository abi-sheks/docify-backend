
def getUserArray(tag) -> list:
    user_array : list = []
    for user in tag.users.all():
        user_array.append(user.user.username)
    return user_array

def isWriter(uname : str, doc) -> bool:
    if(isCreator(uname, doc)):
        return True
    for write_tag in doc.write_tags.all():
            usernames = getUserArray(write_tag)
            if uname in usernames:
                return uname in usernames
    return False    
    
def isReader(uname : str, doc) -> bool:
    if(isCreator(uname, doc)):
        return True
    for read_tag in doc.read_tags.all():
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

def isAccessor(uname : str, doc) -> bool:
    accessor_names = [accessor.prof_username for accessor in doc.accessors.all()]
    return uname in accessor_names

def isAccessible(uname : str, doc) -> bool:
    is_restricted_and_accessor : bool = doc.restricted and (isCreator(uname, doc) or isAccessor(uname, doc))
    return (not doc.restricted) or is_restricted_and_accessor
