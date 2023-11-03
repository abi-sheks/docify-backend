from rest_framework import permissions
from docsapp.utils import getUserArray, isReader, isWriter, isReadPermsChange, isWritePermsChange, isAdmin, isAccessible, isCreator, isRestrictionChange

class IsCreatorPermission(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj) -> bool:
        return isCreator(request.user.username, obj)
    
class TagEditPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return isAdmin(request.user.username, obj)

class DocMutatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        #handling put requests to change readers and writers
        username : str = request.user.username
        # checks if the read permissions are being changed
        if request.method == "PUT" and isReadPermsChange(request.data.get('read_tags'), obj):
            return isReader(username, obj.read_tags) and isAccessible(request.user.username, obj)
        if request.method == "PUT" and isWritePermsChange(request.data.get('write_tags'), obj):
            return isWriter(username, obj.write_tags) and isAccessible(request.user.username, obj)
        if request.method == "PUT" and isRestrictionChange(request.data.get('restricted'), obj):
            return isCreator(request.user.username, obj)
        if request.method == "DELETE":
            return isWriter(username, obj.write_tags) or isCreator(request.user.username, obj)
        return True

