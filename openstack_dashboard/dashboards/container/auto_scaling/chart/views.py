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

    def get(self, request, *args, **kwargs):
        instance_id = self.request.GET.get('instance_id', None)
        result = {}
        try:
            instance = api.nova.server_get(self.request, instance_id)
            instance_ip = instance.addresses.values()[0][0]['addr']
            full_flavor = api.nova.flavor_get(
                self.request, instance.flavor["id"])
            # vm_data = self.get_cpu_ram_usage(instance_ip, '8080', full_flavor)
            container_id = '3014bb409730e961fe4f39f6d1576c' +\
                '3dc98d3d09d05cd115b9a84b31b9f20931'
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
                        {'y': cpu_usage * 1000, 'x': cur['timestamp']})
                    index += 1
                data['value'] = data_timestamp_list
                data['id'] = container_id

            vm_data = {'cpu_data': {'value': data['value']}}

            container_data = cadvisor_api.get_container_detail(
                host_ip=HOST_IP, container_id=container_id)
            if container_data != 'Error':
                container_name = container_data['name']
                container_ram_data = container_data['realtime_data']
                data_timestamp_list = []
                data = {}
                data['name'] = container_name
                data['unit'] = 'MB'
                for value_unit in container_ram_data['/docker/' +
                                                     container_id]:
                    data_timestamp_list.append(
                        {'y': float(value_unit['memory']['usage']) / (1024 * 1024),
                         'x': value_unit['timestamp']})
                data['value'] = data_timestamp_list
                data['id'] = container_id
            vm_data['ram_data'] = {'value': data['value']}

        except Exception:
            instance = None

        return HttpResponse(json.dumps(vm_data),
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
