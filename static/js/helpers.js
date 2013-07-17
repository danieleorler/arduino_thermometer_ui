function getDeviceMode()
{
    var envs = ['phone', 'tablet', 'desktop'];

    $el = $('<div>');
    $el.appendTo($('body'));

    for (var i = envs.length - 1; i >= 0; i--)
    {
        var env = envs[i];
        $el.addClass('hidden-'+env);
        if ($el.is(':hidden'))
        {
            $el.remove();
            return env
        }
    }
}

function drawDesktopChart(element,temp_data)
{
    google.load('visualization', '1', {'packages':['annotatedtimeline']});

    function drawChart()
    {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime', 'Date');
        data.addColumn('number', 'Temperature');
        data.addRows(temp_data);

        var chart = new google.visualization.AnnotatedTimeLine(element);
        chart.draw(data, {displayAnnotations: true});
    }

    google.setOnLoadCallback(drawChart);
}

function drawMobileChart(element,temp_data)
{

    google.load('visualization', '1.0', {'packages':['corechart']});

    function drawChart()
    {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime', 'Date');
        data.addColumn('number', 'Temperature');
        data.addRows(temp_data);

        var chart = new google.visualization.LineChart(element);
        chart.draw(data, {curveType: "function"});
    }

    google.setOnLoadCallback(drawChart);

}