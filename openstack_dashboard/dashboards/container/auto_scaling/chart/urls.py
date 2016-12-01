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

from django.conf.urls import url

from openstack_dashboard.dashboards.container.auto_scaling\
    .chart import views

urlpatterns = [
    # url(r'^container_cpu_detail$', views.ContainerCPUDetailView.as_view(),
    #     name='container_cpu_detail'),
    url(r'^vm_detail$', views.GetVMDetail.as_view(),
        name='vm_detail'),
    # url(r'^container_list$', views.ContainerListView.as_view(),
    #     name='container_list'),
    # url(r'^service_container_list', views.GetContainerListInService.as_view(),
    #     name='container_list_in_service'),
    url(r'^vm_list', views.GetVMList.as_view(), name='vm_list'),
]

