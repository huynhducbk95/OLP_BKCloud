/* Additional JavaScript for service_management. */
$(document).ready(function () {

    var vm_select_element = $("#vm_select");
    var get_vm_list = $("#vm_select").data('vm-list-url');
    $.ajax({
        url: get_vm_list,
        success: function (data) {
            vm_list = data.vm_list;
            vm_list.forEach(function (vm) {
                var option_element = document.createElement('option');
                $(option_element)
                    .attr('value', vm.vm_id)
                    .text(vm.vm_name)
                    .appendTo(vm_select_element);
            })
        },
        error: function (e) {
            console.log('error')
        }
    });


    $('#vm_select').on('change', function () {
        var vm_id = this.value;
        var vm_data_url = $(this).data("vm-data-url") + "?vm_id=" + vm_id.toString();
        vm_chart.clear_chart_list();
        console.log(vm_data_url);
        var vm_line_charts = $('div[data-chart-type="vm_line_chart"]');
        vm_line_charts.attr('data-vm-detail-url', vm_data_url);
        setTimeout(function () {
            vm_chart.setup_line_chart('div[data-chart-type="vm_line_chart"]');
        }, 100);
    });
});
