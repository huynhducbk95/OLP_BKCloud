/* Additional JavaScript for service_management. */
$(document).ready(function () {

    var vm_select_element = $("#instance_id");
    var get_vm_list = $("#instance_id").data('vm-list-url');
    console.log('123');
    console.log(get_vm_list);
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


    $('#instance_id').on('change', function () {
        var vm_id = this.value;
        var vm_data_url = $(this).data("vm-data-url") + "?instance_id=" + vm_id.toString();
        vm_chart.clear_chart_list();
        console.log(vm_data_url);
        var vm_line_charts = $('div[data-chart-type="vm_line_chart"]');
        vm_line_charts.attr('data-vm-detail-url', vm_data_url);
        setTimeout(function () {
            vm_chart.setup_line_chart('div[data-chart-type="vm_line_chart"]');
        }, 100);
    });
});
