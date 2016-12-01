from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables


class DeleteRule(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete rule",
            u"Delete rules",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted rule",
            u"Deleted rules",
            count
        )

    def delete(self, request, rule_id):
        pass


class AddRule(tables.LinkAction):
    name = "add_rule"
    verbose_name = _("Add rule")
    url = "horizon:container:auto_scaling:add_rule"
    classes = ("ajax-modal",)
    icon = "plus"

    def allowed(self, request, datum=None):
        return True


class ScalingRuleTable(tables.DataTable):
    metric = tables.Column('metric', verbose_name=_("Metric"))
    upper_threshold = tables.Column('upper_threshold', verbose_name=_("Upper threshold"))
    lower_threshold = tables.Column('lower_threshold', verbose_name=_("Lower threshold"))
    node_up = tables.Column('node_up', verbose_name=_("Node up"))
    node_down = tables.Column('node_down', verbose_name=_("Node down"))

    def __init__(self, request, *args, **kwargs):
        super(ScalingRuleTable, self).__init__(request, *args, **kwargs)

    class Meta(object):
        verbose_name = "Scaling Rule"
        name = 'scaling_rule'
        table_actions = (AddRule, DeleteRule,)
