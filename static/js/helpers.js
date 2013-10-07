function getDeviceMode()
{
    var envs = ['xs', 'sm', 'md', 'lg'];

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

function drawDesktopChart(element,data)
{
    google.load('visualization', '1', {'packages':['annotatedtimeline']});

    function drawChart()
    {
        var graphData = new google.visualization.DataTable();
        graphData.addColumn(data.dateType, data.dateName);
        graphData.addColumn(data.valType, data.valName);
        
        for(i in data.series)
        {
            graphData.addRows(data.series[i]);
        }

        var chart = new google.visualization.AnnotatedTimeLine(element);
        chart.draw(graphData, {displayAnnotations: true, height:data.height});
    }

    google.setOnLoadCallback(drawChart);
}

function drawMobileChart(element,data)
{

    google.load('visualization', '1.0', {'packages':['corechart']});

    function drawChart()
    {
        var graphData = new google.visualization.DataTable();
        graphData.addColumn(data.dateType, data.dateName);
        graphData.addColumn(data.valType, data.valName);
        
        for(i in data.series)
        {
            graphData.addRows(data.series[i]);
        }

        var chart = new google.visualization.LineChart(element);
        chart.draw(graphData, {curveType: "function",height:data.height});
    }

    google.setOnLoadCallback(drawChart);

}

function drawIndicatorsChart(element,data)
{

    google.load('visualization', '1.0', {'packages':['corechart']});

    function drawChart()
    {
        var graphData = new google.visualization.DataTable();
        graphData.addColumn("date","Date");
        graphData.addColumn("number","Min");
        graphData.addColumn("number","Max");
        graphData.addColumn("number","Avg");
        graphData.addRows(data);
        graphData.sort([{column:0}]);

        var dataView = new google.visualization.DataView(graphData);
        dataView.setColumns(
            [
                {calc: function(data, row) { return data.getFormattedValue(row, 0); }, type:'string'},
                1,
                2,
                3
            ]);
        
        var options =
        {
            title: 'Min, Max and Avg Temperature'
        };


        var chart = new google.visualization.LineChart(element);
        chart.draw(dataView, options);
    }

    google.setOnLoadCallback(drawChart);

}