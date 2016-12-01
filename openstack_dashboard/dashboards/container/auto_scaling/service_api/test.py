import django
from openstack_dashboard import api

class GetInstanceList(django.views.generic.TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            instances, self._more = api.nova.server_list(
                self.request)
        except Exception:
            print ('error')
