#ifndef WINDOW_WIDGET_H
#define WINDOW_WIDGET_H

#include <QWidget>
#include <QLabel>

class MyWindowWidget : public QWidget
{
    Q_OBJECT

    public:
        MyWindowWidget(QWidget * parent = 0);
        ~MyWindowWidget();

    protected:
        void paintEvent(QPaintEvent * event);
        QLabel * label;
        QTimer * timer;
};

#endif // WINDOW_WIDGET_H
