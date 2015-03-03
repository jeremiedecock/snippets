/*
 * A very basic snippet of Qt5 with a Makefile.
 *
 * DEBIAN PACKAGE REQUIRED: qt5-default (on Debian Jessie)
 *
 */

#include <QApplication>
#include <QTextEdit>

int main(int argv, char ** argc) {

    QApplication app(argv, argc);

    QTextEdit widget;
    widget.show();

    return app.exec();

}
