# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard import api
import django
from django.http import HttpResponse
import json
from horizon import forms
from horizon import tables
from openstack_dashboard.dashboards.container.auto_scaling import forms as add_rule_forms
from openstack_dashboard.dashboards.container.auto_scaling import tables as rule_tables
import docker
import requests
import datetime


class Rule:
    def __init__(self, rule_id, metric, upper_threshold, lower_threshold, node_up, node_down):
        self.id = rule_id
        self.metric = metric
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
        self.node_up = node_up
        self.node_down = node_down


class IndexView(tables.DataTableView):
    table_class = rule_tables.ScalingRuleTable
    template_name = 'container/auto_scaling/index.html'
    page_title = _("Scaling Rule")

    def get_data(self):
        rules = []
        rules.append(Rule(1, 'CPU', 90, 20, 1, 4))
        rules.append(Rule(2, 'CPU', 90, 20, 1, 4))
        rules.append(Rule(3, 'CPU', 90, 20, 1, 4))
        rules.append(Rule(4, 'CPU', 90, 20, 1, 4))
        rules.append(Rule(5, 'CPU', 90, 20, 1, 4))
        ip = 'localhost'
        port = '8080'
        url = 'http://' + ip + ":" + port + '/api/v1.2/docker/'
        data = requests.get(url=url)
        containers = data.json()
        list_key = containers.keys()
        result= {}
        container_list = []
        for container in list_key:
            container_info = {}
            container_id = containers[container]['id']
            container_name = containers[container]['aliases'][0]
            stats = containers[container]['stats']
            series = []
            index = 1
            while index< len(stats):
                cur = stats[index]
                prev = stats[index - 1]
                interval_nano = get_interval(
                    cur['timestamp'], prev['timestamp'])
                cpu_usage = (cur['cpu']['usage']['total'] -
                             prev['cpu']['usage']['total']) / interval_nano
                container_usage = {
                    'time': cur['timestamp'][:19],
                    'cpu':cpu_usage,
                }
                series.append(container_usage)
                index += 1
            container_info['container_id'] = container_id
            container_info['container_name'] =container_name
            container_info['container_data'] = series
            container_list.append(container_info)
        result['container_list'] = container_list
        return rules


class AddRuleView(forms.ModalFormView):
    form_class = add_rule_forms.AddRuleForm
    form_id = "add_rule_form"
    modal_header = _("Add Rule Host")
    submit_label = _("Add Rule Host")
    submit_url = reverse_lazy('horizon:container:auto_scaling:add_rule')
    template_name = 'container/auto_scaling/add_rule.html'
    success_url = reverse_lazy('horizon:container:auto_scaling:index')
    page_title = _("Add Rule Host")

    def get_initial(self):
        initial = {}
        return initial


class GetInstanceList(django.views.generic.TemplateView):
    def get(self):
        try:
            vm_list = {}
            vms = []
            instances = api.nova.server_list(
                self.request)
            instance_list = instances[0]
            for instance in instance_list:
                metadata = instance.metadata
                keys = metadata.keys()
                if 'olp2016' in keys:
                    vm = {}
                    vm['vm_id'] = instance.id
                    vm['vm_name'] = instance.name
                    vms.append(vm)
            vm_list['vm_list'] = vms
        except Exception:
            vm_list['vm_list'] = []
            print ('unable to retrevie instance')
        return HttpResponse(json.dumps(vm_list), content_type='application/json')


class GetVMDetail(django.views.generic.TemplateView):
    def get(self):
        instance_id = self.request.GET.get('instance_id', None)
        result = {}
        try:
            instance = api.nova.server_get(self.request, instance_id)
            instance_ip = instance.addresses['OPS1_IntNet'][0]['addr']
            full_flavor = api.nova.flavor_get(
                self.request, instance.flavor["id"])
        except Exception:
            instance = None
            print ('unable to retreive instance detail')
        return HttpResponse(json.dumps(result), content_type='application/json')

    def get_cpu_ram_usage(self, ip, port, flavor):
        ip = 'localhost'
        port = '8080'
        url = 'http://' + ip + ":" + port + '/api/v1.2/docker/'
        data = requests.get(url=url)
        containers = data.json()
        list_key = containers.keys()
        result = {}
        container_list = []
        for container in list_key:
            container_info = {}
            container_id = containers[container]['id']
            container_name = containers[container]['aliases'][0]
            stats = containers[container]['stats']
            series = []
            index = 1
            while index < len(stats):
                cur = stats[index]
                prev = stats[index - 1]
                interval_nano = get_interval(
                    cur['timestamp'], prev['timestamp'])
                cpu_usage = (cur['cpu']['usage']['total'] -
                             prev['cpu']['usage']['total']) / interval_nano
                container_usage = {
                    'time': cur['timestamp'][:19],
                    'cpu': cpu_usage,
                }
                series.append(container_usage)
                index += 1
            container_info['container_id'] = container_id
            container_info['container_name'] = container_name
            container_info['container_data'] = series
            container_list.append(container_info)
        result['container_list'] = container_list
        return result


def get_interval(current, previous):
    cur = datetime.datetime.strptime(current[:-4], "%Y-%m-%dT%H:%M:%S.%f")
    prev = datetime.datetime.strptime(previous[:-4], "%Y-%m-%dT%H:%M:%S.%f")
    return (cur - prev).total_seconds() * 1000000000