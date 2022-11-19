from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    #NOTE: has_permission의 경우 apiview접근시 작용하여 boolean값 반환
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated

    #NOTE: has_object는 get_object로 db 접근할때 반환
    def has_object(self,request,view,obj):
        #GET method 일 때는 허락
        if request.method in permissions.SAFE_METHODS:
            return True
        #PATCH, POST 등의 수정을 가하는 거면 작성자 일 때만 허락
        return request.user == obj.owner