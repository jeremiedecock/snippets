#include <QApplication>

#include "paint_widget.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    MyPaintWidget widget;
    widget.show();
    return app.exec();
}
