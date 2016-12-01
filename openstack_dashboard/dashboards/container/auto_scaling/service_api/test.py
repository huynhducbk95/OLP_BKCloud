# import django
from openstack_dashboard import api
import logging

LOG = logging.getLogger(__name__)
def get(self):
        try:
            instances = api.nova.server_list(
                self.request)
        except Exception:
            print ('error')

get()