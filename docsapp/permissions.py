from rest_framework import permissions
from docsapp.models.editable import Editable
from docsapp.models.tag import Tag
from docsapp.utils import getUserArray, isReader, isWriter, isReadPermsChange, isWritePermsChange

class IsCreatorPermission(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj):
        return obj.creator.prof_username == request.user.username
    
class TagEditPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.creator.prof_username == request.user.username

class DocMutatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #handling put requests to change readers and writers
        username = request.user.username
        # checks if the read permissions are being changed
        if request.method == "PUT" and isReadPermsChange(request.data.get('read_tags'), obj):
            return isReader(username, obj.read_tags)
        if request.method == "PUT" and isWritePermsChange(request.data.get('write_tags'), obj):
            return isWriter(username, obj.write_tags)
        if request.method == "DELETE":
            return isWriter(username, obj.write_tags)
        return True
    
            
    
class IsEditorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        username = request.user.username
        for write_tag in obj.write_tags:
            usernames = getUserArray(write_tag)
            if username in usernames:
                return username in usernames
        return False    

class IsReaderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        username = request.user.username
        for read_tag in obj.read_tags:
            usernames = getUserArray(read_tag)
            if username in usernames:
                return username in usernames
        return False    


