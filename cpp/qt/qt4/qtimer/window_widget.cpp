#include <QtGui>
#include <iostream>

#include "window_widget.h"

/**
 *
 */
MyWindowWidget::MyWindowWidget(QWidget * parent) : QWidget(parent)
{
    this->timer = new QTimer(this);
    connect(this->timer, SIGNAL(timeout()), this, SLOT(update()));
    this->timer->start(1000);

    this->label = new QLabel("0");
    this->label->setAlignment(Qt::AlignCenter);

    QVBoxLayout * layout = new QVBoxLayout;
    layout->addWidget(this->label);

    this->setLayout(layout);

    setWindowTitle(tr("Timer Snippet"));
    resize(200, 200);
}

/**
 *
 */
MyWindowWidget::~MyWindowWidget()
{
    delete this->timer;
    delete this->label;
}

/**
 *
 */
void MyWindowWidget::paintEvent(QPaintEvent *)
{
    // Trace paintEvent calls.
    // Point out the fact that each second, paintEvent is called twice:
    // - one time by this->timer
    // - one time by this->label->setText()
    static int cpt = 0;
    std::cout << cpt++ << std::endl;

    // Update the label: display elapsed time
    static const QTime start_time = QTime::currentTime();

    QTime current_time = QTime::currentTime();
    int ellapsed_sec = start_time.secsTo(current_time);

    this->label->setText(QString::number(ellapsed_sec));
}
