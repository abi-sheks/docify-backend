
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
     
