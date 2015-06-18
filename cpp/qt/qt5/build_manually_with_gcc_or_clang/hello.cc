/*
 * A very basic snippet of Qt5.
 *
 * DEBIAN PACKAGE REQUIRED: qt5-default (on Debian Jessie)
 *
 * USAGE (with GCC):
 *    g++ -fPIC $(pkg-config --cflags Qt5Widgets) -c hello.cc
 *    g++ -o hello $(pkg-config --libs Qt5Widgets) hello.o
 */

#include <QApplication>
#include <QTextEdit>

int main(int argv, char ** argc) {

    QApplication app(argv, argc);

    QTextEdit widget;
    widget.show();

    return app.exec();

}
