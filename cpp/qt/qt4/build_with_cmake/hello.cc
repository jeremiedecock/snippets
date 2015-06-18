#include <QApplication>
#include <QTextEdit>

int main(int argv, char ** argc) {

    QApplication app(argv, argc);

    QTextEdit widget;
    widget.show();

    return app.exec();

}
