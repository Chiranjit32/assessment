from common.models import Users
from django.db.models import Q


class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False


    def get_user(self, user_id):
       try:
          return Users.objects.get(pk=user_id)
       except Users.DoesNotExist:
          return None


    def authenticate(self, username, password):
        try:
            users = Users.objects.prefetch_related('ipmodel_set').filter(
                Q(username=username) | Q(email=username) | Q(phone=username)
            )
        except:
            users = []
        if len(users) == 0:
            user = None
        elif len(users) > 1:
            user = users.filter(pswd_token=password).first()
        else:
            user = users[0]
        return user if user is not None and user.check_password(password) else None