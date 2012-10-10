#ifndef PAINT_WIDGET_H
#define PAINT_WIDGET_H

#include <QWidget>

class MyPaintWidget : public QWidget
{
    Q_OBJECT

    public:
        MyPaintWidget(QWidget * parent = 0);
        ~MyPaintWidget();

    protected:
        void paintEvent(QPaintEvent * event);
        QTimer * timer;

};

#endif // PAINT_WIDGET_H
