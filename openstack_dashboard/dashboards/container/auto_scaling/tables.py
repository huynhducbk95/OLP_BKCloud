from django.utils.translation import ugettext_lazy as _

from horizon import tables


class ContainerFilter(tables.FilterAction):
    name = 'container_filter'


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
        # row_actions = ()


