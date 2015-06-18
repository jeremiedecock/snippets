#include <QtGui>
#include <iostream>

#include "paint_widget.h"

/**
 *
 */
MyPaintWidget::MyPaintWidget(QWidget * parent) : QWidget(parent)
{
    setWindowTitle(tr("Basic Shapes"));
    resize(200, 200);
}

/**
 *
 */
void MyPaintWidget::paintEvent(QPaintEvent *)
{
    // 
    int side = qMin(this->width(), this->height());

    // 
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    painter.translate(this->width() / 2, this->height() / 2);
    painter.scale(side / 200.0, side / 200.0);

    // Line
    painter.drawLine(80, 0, 96, 0);

    // Line
    painter.save();
    painter.rotate(90.0);
    painter.drawLine(80, 0, 96, 0);
    painter.restore();

    // Line
    painter.save();
    QColor color1(0, 127, 127, 191);
    painter.setBrush(color1);
    painter.setPen(color1);

    painter.rotate(180.0);
    painter.drawLine(80, 0, 96, 0);
    painter.restore();

    // Polygon
    static const QPointF polygonPoints[4] = {
        QPointF(-30.0, 30.0),
        QPointF(50.0, 30.0),
        QPointF(30.0, -30.0),
        QPointF(-30.0, -30.0)
    };

    painter.drawConvexPolygon(polygonPoints, 4);

}
