#ifndef ANALOGCLOCK_H
#define ANALOGCLOCK_H

#include <QWidget>

class MyPaintWidget : public QWidget
{
    Q_OBJECT

    public:
        MyPaintWidget(QWidget * parent = 0);

    protected:
        void paintEvent(QPaintEvent * event);
};

#endif
