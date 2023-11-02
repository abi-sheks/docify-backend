from rest_framework import permissions
from docsapp.models.editable import Editable
from docsapp.models.tag import Tag

class IsCreatorPermission(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj):
        return obj.creator.prof_username == request.user.username
    
class TagEditPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.creator.prof_username == request.user.username
    
class IsEditorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        mail = request.user.email
        for write_tag in obj.write_tags:
            emails = getEmailArray(write_tag)
            if mail in emails:
                return mail in emails
        return False    

class IsReaderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        mail = request.user.email
        for read_tag in obj.read_tags:
            emails = getEmailArray(read_tag)
            if mail in emails:
                return mail in emails
        return False    

def getEmailArray(tag):
    emailArray = []
    for user in tag.users:
        emailArray.append(user.user.email)
    return emailArray
