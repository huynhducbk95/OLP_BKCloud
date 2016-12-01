from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

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
        return True

    def get_success_url(self):
        return reverse("horizon:container:auto_scaling:index")

    def get_failure_url(self):
        return reverse("horizon:container:auto_scaling:index")
