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

import django
from horizon import forms
from horizon import tables
from openstack_dashboard.dashboards.container.auto_scaling import forms as add_rule_forms
from openstack_dashboard.dashboards.container.auto_scaling import tables as rule_tables

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
        return rules

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['VM'] = ['swarm-olp','cal-olp','test','demo']
        return context

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

