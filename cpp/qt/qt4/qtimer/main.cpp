#include <QApplication>

#include "window_widget.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    MyWindowWidget widget;
    widget.show();

    return app.exec();
}
