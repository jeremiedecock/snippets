#include <QtGui>
#include <iostream>

#include "paint_widget.h"

/**
 *
 */
MyPaintWidget::MyPaintWidget(QWidget * parent) : QWidget(parent)
{
    this->timer = new QTimer(this);
    connect(this->timer, SIGNAL(timeout()), this, SLOT(update()));
    this->timer->start(40);     // update widget every 40 ms
    //this->timer->start(1000); // update widget every 1000 ms

    setWindowTitle(tr("Basic Animation"));
    resize(200, 200);
}

/**
 *
 */
MyPaintWidget::~MyPaintWidget()
{
    delete this->timer;
}

/**
 *
 */
void MyPaintWidget::paintEvent(QPaintEvent *)
{
    static const QTime start_time = QTime::currentTime();

    // 
    int side = qMin(this->width(), this->height());

    // 
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    painter.translate(this->width() / 2, this->height() / 2);
    painter.scale(side / 200.0, side / 200.0);

    //
    QTime current_time = QTime::currentTime();
    int ellapsed_ms = start_time.msecsTo(current_time);

    // Ellipse
    double angle = ellapsed_ms / 50.0; // % 360.0
    painter.rotate(angle);
    painter.drawLine(80, 0, 96, 0);

    std::cout << "time: " << ellapsed_ms << " - " << "angle: " << angle << std::endl;
}
