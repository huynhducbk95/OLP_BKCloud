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
import django.views
import json
from django.http import HttpResponse
# from django.http import Http404
import datetime
# import time
from openstack_dashboard.dashboards.container.auto_scaling\
    .chart import cadvisor_api
from openstack_dashboard import api
import requests


HOST_IP = '127.0.0.1'


class ContainerCPUDetailView(django.views.generic.TemplateView):

    def get(self, request, *args, **kwargs):
        container_id = request.GET.get('id', None)
        container_data = cadvisor_api.get_container_detail(
            host_ip=HOST_IP, container_id=container_id)
        if container_data != 'Error':
            container_name = container_data['name']
            containers_info = container_data['realtime_data']
            data_timestamp_list = []
            data = {}
            data['name'] = container_name
            data['unit'] = 'Cores'
            index = 1
            data_list = containers_info['/docker/' + container_id]
            while index < len(data_list):
                cur = data_list[index]
                prev = data_list[index - 1]
                interval_nano = get_interval(
                    cur['timestamp'], prev['timestamp'])
                cpu_usage = (cur['cpu']['usage']['total'] -
                             prev['cpu']['usage']['total']) / interval_nano
                data_timestamp_list.append(
                    {'y': cpu_usage, 'x': cur['timestamp']})
                index += 1
            data['value'] = data_timestamp_list
            data['id'] = container_id
            return HttpResponse(json.dumps(data),
                                content_type='application/json')

        else:
            context = {
                'status': '400',
                'reason': 'Cannot retreive container data from cadvisor_api'
            }
            response = HttpResponse(json.dumps(context),
                                    content_type='application/json')
            response.status_code = 400
            return response


def get_interval(current, previous):
    cur = datetime.datetime.strptime(current[:-4], "%Y-%m-%dT%H:%M:%S.%f")
    prev = datetime.datetime.strptime(previous[:-4], "%Y-%m-%dT%H:%M:%S.%f")
    return (cur - prev).total_seconds() * 1000000000


class GetVMDetail(django.views.generic.TemplateView):

    def get_cpu_ram_usage(self, ip, port, flavor):
        ip = 'localhost'
        # port = '8080'
        url = 'http://' + ip + ":" + port + '/api/v1.2/docker/'
        data = requests.get(url=url)
        containers = data.json()
        list_key = containers.keys()
        vm_data = {}
        container_list = []
        for container in list_key:
            container_id = containers[container]['aliases'][1]
            container_info = {}
            cpu_data = {}
            ram_data = {}
            stats = containers[container]['stats']
            cpu_value = []
            ram_value = []
            index = 1
            while index < len(stats):
                cur = stats[index]
                prev = stats[index - 1]
                interval_nano = get_interval(
                    cur['timestamp'], prev['timestamp'])
                cpu_usage = (cur['cpu']['usage']['total'] -
                             prev['cpu']['usage']['total']) / interval_nano
                ram_usage = cur['memory']['usage']/(1024*1024)
                cpu = {
                    'x': cur['timestamp'][:19],
                    'y': cpu_usage,
                }
                ram = {
                    'x': cur['timestamp'][:19],
                    'y':ram_usage,
                }
                cpu_value.append(cpu)
                ram_value.append(ram)
                index += 1
            cpu_data['value'] = cpu_value
            ram_data['value'] = cpu_value
            container_info['cpu_data'] = cpu_data
            container_info['ram_data'] = ram_data
            container_list.append(container_info)
        cpu_total = []
        ram_total = []
        container0 = container_list[0]['cpu_data']['value']
        for data in container0:
            cpu_unit = {
                'x': data['x'],
                'y':(data['y']/flavor.vcpus)*100
            }
            cpu_total.append(cpu_unit)
        container1 = container_list[0]['ram_data']['value']
        for data1 in container1:
            ram_unit = {
                'x': data1['x'],
                'y': (data1['y']/flavor.ram)*100
            }
            ram_total.append(ram_unit)
        vm_data = {
            'cpu_data': cpu_data,
            'ram_data': ram_data,
        }
        # vm_data['vm_data'] = container_list
        return vm_data

    def get(self, request, *args, **kwargs):
        instance_id = self.request.GET.get('instance_id', None)
        try:
            instance = api.nova.server_get(self.request, instance_id)
            instance_ip = instance.addresses.values()[0][0]['addr']
            full_flavor = api.nova.flavor_get(
                self.request, instance.flavor["id"])
            result = \
                self.get_cpu_ram_usage(instance_ip,'8080',full_flavor)
        except Exception:
            instance = None
            result = {
            }

        return HttpResponse(json.dumps(result),
                            content_type='application/json')


class GetVMList(django.views.generic.TemplateView):

    def get(self, request, *args, **kwargs):
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
        return HttpResponse(json.dumps(vm_list),
                            content_type='application/json')
