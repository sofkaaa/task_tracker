from django.core.exceptions import PermissionDenied
from .models import Task
from django.http import HttpRequest

class UserIsOwnerMixin(object):
    def dispatch(self, request:HttpRequest, *args, **kwargs):
        isnstance:Task = self.gat_object()
        if isnstance.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied