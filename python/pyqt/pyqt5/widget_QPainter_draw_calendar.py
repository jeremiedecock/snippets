#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See https://www.youtube.com/watch?v=0wAU5usATX8/

import sys
import datetime

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt


class CalendarWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Set window background color
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)

        self.setPalette(palette)

        self.time_label_margin = 30
        self.margin_size = 5
        self.border_size = 2
        self.task_label_font_size = 9
        self.time_label_font_size = 7

        # DATA ##################################

        self.starting_time_str = "05:00"
        self.ending_time_str = "23:00"
        self.current_time_str = "12:17"

        self.starting_time = datetime.datetime.strptime(self.starting_time_str, "%H:%M")
        self.ending_time = datetime.datetime.strptime(self.ending_time_str, "%H:%M")
        self.working_day_duration = self.ending_time - self.starting_time

        self.data = [
                        {"start": "06:00", "end": "06:30", "label": "wakeup"},
                        {"start": "12:00", "end": "13:00", "label": "lunch"}
                    ]


    def timeCoordinateMapper(self, time_str):
        """Convert time string to widget y pixels coordinate"""
        widget_height = self.size().height() - 2*self.margin_size - 2*self.border_size

        if widget_height > 0:
            relative_time = datetime.datetime.strptime(time_str, "%H:%M") - self.starting_time
            y_pos = self.margin_size + self.border_size + relative_time * widget_height / self.working_day_duration
        else:
            y_pos = self.margin_size + self.border_size

        return y_pos


    def paintEvent(self, event):
        qp = QPainter(self)

        qp.setRenderHint(QPainter.Antialiasing)           # <- Set anti-aliasing  See https://wiki.python.org/moin/PyQt/Painting%20and%20clipping%20demonstration

        size = self.size()
        widget_width, widget_height = size.width(), size.height()

        # Make fonts

        time_label_font = qp.font()
        time_label_font.setPointSize(self.time_label_font_size)

        task_label_font = qp.font()
        task_label_font.setPointSize(self.task_label_font_size)

        # Frame

        qp.setPen(QPen(Qt.black, self.border_size, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.white, Qt.SolidPattern))

        qp.drawRect(self.margin_size + self.time_label_margin,                  # x_start
                    self.margin_size,                                           # y_start
                    widget_width - 2*self.margin_size - self.time_label_margin, # x_size
                    widget_height - 2*self.margin_size)                         # y_size

        # Starting time label

        qp.setFont(time_label_font)

        qp.drawText(0, #self.margin_size,   # x_start
                    self.margin_size - int(self.time_label_font_size/2), # y_start
                    self.time_label_margin, # x_size
                    self.time_label_font_size,   # y_size
                    Qt.AlignCenter,
                    self.starting_time_str)

        # Ending time label

        qp.setFont(time_label_font)

        qp.drawText(0, #self.margin_size,   # x_start
                    widget_height - self.margin_size - int(self.time_label_font_size/2), # y_start
                    self.time_label_margin, # x_size
                    self.time_label_font_size,   # y_size
                    Qt.AlignCenter,
                    self.ending_time_str)

        # Draw a line for each hour

        qp.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
        qp.setFont(time_label_font)

        i = 1
        marker_time = datetime.datetime(year=self.starting_time.year,
                                       month=self.starting_time.month,
                                       day=self.starting_time.day,
                                       hour=self.starting_time.hour + i)

        while marker_time.hour <= self.ending_time.hour:
            time_marker_str = marker_time.strftime("%H:%M")
            marker_time_y_pos = self.timeCoordinateMapper(time_marker_str)

            qp.drawLine(self.margin_size + self.time_label_margin,  # x_start
                        marker_time_y_pos,                          # y_start
                        widget_width - self.margin_size,            # x_end
                        marker_time_y_pos)                          # y_end

            qp.drawText(0, #self.margin_size,   # x_start
                        marker_time_y_pos - int(self.time_label_font_size/2), # y_start
                        self.time_label_margin, # x_size
                        self.time_label_font_size,   # y_size
                        Qt.AlignCenter,
                        time_marker_str)

            if marker_time.hour == 23:
                break

            i += 1
            marker_time = datetime.datetime(year=self.starting_time.year,
                                           month=self.starting_time.month,
                                           day=self.starting_time.day,
                                           hour=self.starting_time.hour + i)

        # Tasks

        qp.setPen(QPen(Qt.black, self.border_size, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))

        qp.setFont(task_label_font)

        for task in self.data:
            y_start = self.timeCoordinateMapper(task["start"])
            y_end = self.timeCoordinateMapper(task["end"])
            qp.drawRect(self.margin_size + self.time_label_margin,                  # x_start
                        y_start,                                                    # y_start
                        widget_width - 2*self.margin_size - self.time_label_margin, # x_size
                        y_end - y_start)                                            # y_size

            qp.drawText(self.margin_size + self.time_label_margin,                  # x_start
                        y_start,                                                    # y_start
                        widget_width - 2*self.margin_size - self.time_label_margin, # x_size
                        y_end - y_start,                                            # y_size
                        Qt.AlignCenter,
                        task["label"])

        # Draw a line to show the current time

        current_time_y_pos = self.timeCoordinateMapper(self.current_time_str)

        qp.setPen(QPen(Qt.red, self.border_size, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        qp.drawLine(self.margin_size + self.time_label_margin,  # x_start
                    current_time_y_pos,                         # y_start
                    widget_width - self.margin_size,            # x_end
                    current_time_y_pos)                         # y_end

        # Current time bullet

        bullet_border = 5
        qp.setPen(QPen(Qt.red, bullet_border, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        qp.setRenderHint(QPainter.Antialiasing)           # <- Set anti-aliasing  See https://wiki.python.org/moin/PyQt/Painting%20and%20clipping%20demonstration

        bullet_radius = 3
        qp.drawEllipse(self.margin_size + self.time_label_margin - bullet_radius,  # x_start,
                       current_time_y_pos - bullet_radius,                         # y_start,
                       2 * bullet_radius,
                       2 * bullet_radius)

        ## Current time label

        #qp.setFont(time_label_font)

        #qp.drawText(0, #self.margin_size,   # x_start
        #            current_time_y_pos - int(self.time_label_font_size/2), # y_start
        #            self.time_label_margin, # x_size
        #            self.time_label_font_size,   # y_size
        #            Qt.AlignCenter,
        #            self.current_time_str)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = CalendarWidget()
    widget.show()

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)

