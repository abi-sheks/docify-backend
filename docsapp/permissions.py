from rest_framework import permissions
from docsapp.utils import getUserArray, isReader, isWriter, isReadPermsChange, isWritePermsChange, isAdmin, isAccessible, isCreator, isRestrictionChange
from docsapp.models.editable import Editable

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
            return isReader(username, obj) and isAccessible(request.user.username, obj)
        if request.method == "PUT" and isWritePermsChange(request.data.get('write_tags'), obj):
            return isWriter(username, obj) and isAccessible(request.user.username, obj)
        if request.method == "PUT" and isRestrictionChange(request.data.get('restricted'), obj):
            return isCreator(request.user.username, obj)
        if request.method == "DELETE":
            return isWriter(username, obj) or isCreator(request.user.username, obj)
        return True

class CommentsAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if(request.method == 'POST'):
            docId : str = request.data.get('parent_doc')
            print(docId)
            for doc in Editable.objects.all():
                print(f"Id is {doc.id}")
            doc = Editable.objects.get(id=docId)
            return isAccessible(request.user.username , doc) or isReader(request.user.username, doc)
        return True


