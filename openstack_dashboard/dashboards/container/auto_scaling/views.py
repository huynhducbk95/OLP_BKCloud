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

from django.utils.translation import ugettext_lazy as _

from horizon import tables
from openstack_dashboard.dashboards.container.auto_scaling import tables as rule_tables


class Rule:
    def __init__(self, rule_id, metric, upper_threshold, lower_threshold, node_up, node_down):
        self.rule_id = rule_id
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
        return rules
