from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.container.auto_scaling.database import database_service

from horizon import forms


class AddRuleForm(forms.SelfHandlingForm):
    NUM_CHOICE = [
        ('cpu', _('CPU')),
        ('mem', _('Memory')), ]
    metric = forms.ChoiceField(label=_("Metric"),
                               required=True,
                               choices=NUM_CHOICE, )
    upper_threshold = forms.CharField(max_length=255, label=_("Upper threshold"),
                                      required=False)
    lower_threshold = forms.CharField(max_length=255, label=_("Lower threshold"),
                                      required=False)
    node_up = forms.CharField(max_length=255,
                              label=_("Number of node will be added when scale out"),
                              required=False)
    node_down = forms.CharField(max_length=255,
                                label=_("Number of node will be added when scale in"),
                                required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddRuleForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        metric = data['metric']
        upper_threshold = data['upper_threshold']
        lower_threshold = data['lower_threshold']
        node_up = data['node_up']
        node_down = data['node_down']
        rule = database_service.Rule(metric = metric,
                                     upper_threshold = upper_threshold,
                                     lower_threshold = lower_threshold,
                                     node_up = node_up,
                                     node_down = node_down)
        database_service.updateRule(rule)
        return True

    def get_success_url(self):
        return reverse("horizon:container:auto_scaling:index")

    def get_failure_url(self):
        return reverse("horizon:container:auto_scaling:index")
