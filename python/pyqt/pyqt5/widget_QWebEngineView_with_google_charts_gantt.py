#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See:
# - https://developers.google.com/chart/interactive/docs/gallery/ganttchart
# - https://stackoverflow.com/questions/50830399/how-to-add-a-horizontal-scroll-bar-to-google-gantt-chart

HTML = r'''<!DOCTYPE html>
<head>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  <script type="text/javascript">
    google.charts.load('current', {'packages':['gantt']});
    google.charts.setOnLoadCallback(drawChart);

    function daysToMilliseconds(days) {
      return days * 24 * 60 * 60 * 1000;
    }

    function drawChart() {

      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Task ID');
      data.addColumn('string', 'Task Name');
      data.addColumn('string', 'Resource');
      data.addColumn('date', 'Start Date');
      data.addColumn('date', 'End Date');
      data.addColumn('number', 'Duration');
      data.addColumn('number', 'Percent Complete');
      data.addColumn('string', 'Dependencies');

      data.addRows([
        ['Research', 'Find sources', null,
         new Date(2015, 0, 1), new Date(2015, 0, 25), null,  100,  null],
        ['Write', 'Write paper', 'write',
         null, new Date(2015, 1, 9), daysToMilliseconds(3), 25, 'Research,Outline'],
        ['Cite', 'Create bibliography', 'write',
         null, new Date(2015, 1, 7), daysToMilliseconds(1), 20, 'Research'],
        ['Complete', 'Hand in paper', 'complete',
         new Date(2015, 2, 6), null, daysToMilliseconds(30), 0, 'Cite,Write'],
        ['Outline', 'Outline paper', 'write',
         null, new Date(2015, 1, 6), daysToMilliseconds(1), 100, 'Research']

      ]);

      var options = {
        height: 275,    // gantt chart height
        width: 3000     // gantt chart width
      };

      var chart = new google.visualization.Gantt(document.getElementById('chart_div'));

      chart.draw(data, options);
    }
  </script>
</head>
<body>
  <div id="chart_div"></div>
</body>
</html>

'''

# The next two lines are a workaround to fix an issue with QWebEngineView (see https://github.com/ContinuumIO/anaconda-issues/issues/9199#issuecomment-383842265)
import ctypes
ctypes.CDLL("libGL.so.1", mode=ctypes.RTLD_GLOBAL)

import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

# Setting "/" as the base_url may be a bad idea : JS script can access any (readable) file of the system...
# It's probably much better to isolate external files in a dedicated directory (e.g. /tmp/...) as everybody do for webservers (/var/www/html)
base_url = QUrl.fromLocalFile("/")

web = QWebEngineView()
web.setHtml(HTML, base_url)
web.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
