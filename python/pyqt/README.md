# PyQt

* https://riverbankcomputing.com/software/pyqt/intro
* https://www.riverbankcomputing.com/software/pyqt/download5
* https://wiki.python.org/moin/PyQt

## Differences between PySide and PyQt

* https://wiki.qt.io/Differences_Between_PySide_and_PyQt

Discussions:
* https://askubuntu.com/questions/140740/should-i-use-pyqt-or-pyside-for-a-new-qt-project
* https://stackoverflow.com/questions/6888750/pyqt-or-pyside-which-one-to-use
* https://www.reddit.com/r/Python/comments/424n4y/pyqt_or_pyside_debate_over_which_to_learn/

## Differences between PyQt4 and PyQt5

* http://pyqt.sourceforge.net/Docs/PyQt5/pyqt4_differences.html

## Qt documentation

* http://doc.qt.io/qt-5/model-view-programming.html
* http://doc.qt.io/qt-5/graphicsview.html
* http://doc.qt.io/qt-5/qtmodules.html
* http://doc.qt.io/qt-5/classes.html
* http://doc.qt.io/qt-5/functions.html

## PyQt5 reference

* http://pyqt.sourceforge.net/Docs/PyQt5/
* Modules: http://pyqt.sourceforge.net/Docs/PyQt5/modules.html#ref-module-index

## PyQt4 tutorials and examples

* http://www.tutorialspoint.com/pyqt/

## PyQt5 tutorials and examples

* http://zetcode.com/gui/pyqt5/
* https://pythonspot.com/en/pyqt5/
* https://github.com/baoboa/pyqt5/tree/master/examples (hundreds of examples!)
* http://projects.skylogic.ca/blog/how-to-install-pyqt5-and-build-your-first-gui-in-python-3-4/
* http://pythonthusiast.pythonblogs.com/230_pythonthusiast/archive/1348_developing_cross_platform_application_using_qt_pyqt_and_pyside__introduction-part_1_of_5.html
* http://www.boxcontrol.net/beginners-pyqt5-and-qml-integration-tutorial.html#.VeVlsHWlyko
* https://wiki.python.org/moin/PyQt/SampleCode
* https://www.youtube.com/watch?v=53oeJPKRttY&list=PLA955A8F9A95378CE

* http://www.thehackeruniversity.com/2014/01/23/pyqt5-beginner-tutorial/
* http://www.thehackeruniversity.com/2014/01/26/pyqt5-beginner-tutorial-part-2/
* http://www.thehackeruniversity.com/2014/02/20/pyqt5-beginner-tutorial-part-3/


* https://wiki.python.org/moin/PyQt/Tutorials
* https://www.quora.com/What-are-the-best-PyQt5-tutorial
* https://www.reddit.com/r/learnpython/comments/3j6k8x/is_there_any_proper_tutorials_for_pyqt5/
* https://stackoverflow.com/questions/20996193/is-there-a-tutorial-specifically-for-pyqt5

## Tools (QtDesigner, QML, QtQuick)

Source: https://stackoverflow.com/questions/20996193/is-there-a-tutorial-specifically-for-pyqt5

* QtDesigner:
    For those days when your keyboard catches fire, there's a rockin' GUI-Builder called in the installation package. When you see the code this produces (perhaps only in the community version?), you'll see why this may not be the panacea it seems.
* QML:
    Another candidate for panacea: declarative GUI building from formatted JSON. Yum.
* Qt Quick:
    The framework for QML. By this point, it may seem tantalizingly easy, but don't get sucked in by this stuff just yet. It always seems to come down to learning it by hand.
* The Model-View Framework:
    Model-View (not MVC) separates the code that deals with presentation/interaction from the code that manages the data, with the aim of providing modularity.

    Coding in PyQt5 is greatly simplified by using the set of classes that
    implement the Model-View design pattern. Model-View is an evolution of
    Model-View-Controller (MVC), in which the Controller has been reunited with the
    View. They seem like strange bedfellows, but, most of the program's logic is
    dealing with either the user, or data: it seems to make a certain sense, at
    least at a stratospheric level. 
