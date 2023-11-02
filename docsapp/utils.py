
def getUserArray(tag):
    userArray = []
    for user in tag.users:
        userArray.append(user.user.username)
    return userArray

def isWriter(uname, write_tags):
    for write_tag in write_tags:
            usernames = getUserArray(write_tag)
            if uname in usernames:
                return uname in usernames
    return False    
    
def isReader(uname, read_tags):
    for read_tag in read_tags:
        usernames = getUserArray(read_tag)
        if uname in usernames:
            return uname in usernames
    return False   

def isReadPermsChange(incoming_readers, doc):
    current_readers = []
    for tag in doc.read_tags:
        current_readers.append(tag.name)
    return incoming_readers == current_readers

def isWritePermsChange(incoming_writers, doc):
    current_writers = []
    for tag in doc.write_tags:
        current_writers.append(tag.name)
    return incoming_writers == current_writers
     
