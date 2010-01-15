/* 
 * OSG Model
 *
 * Copyright (c) 2009 Jérémie Decock
 */

#include <osgDB/ReadFile>
#include <osgViewer/Viewer>
#include <iostream>

#include <osgGA/GUIEventHandler>

double angle(0.);

void rotate(void) {
	angle += 0.01;
}

class myKeyboardEventHandler : public osgGA::GUIEventHandler {
	public:
		virtual bool handle(const osgGA::GUIEventAdapter& ea,osgGA::GUIActionAdapter&);

		virtual void accept(osgGA::GUIEventHandlerVisitor& v) {
			v.visit(*this);
		};
};

bool myKeyboardEventHandler::handle(const osgGA::GUIEventAdapter& ea, osgGA::GUIActionAdapter& aa) {
	switch(ea.getEventType()) {
		case(osgGA::GUIEventAdapter::KEYDOWN): 	{
				switch(ea.getKey()) {
					case 'w':
						//std::cout << " w key pressed" << std::endl;
						rotate();
						return false;
						break;
					default:
						return false;
				} 
			}
		default:
			return false;
	}
}

int main(int, char **) {

	// Create scene and viewer
	osg::Node* model = osgDB::readNodeFile("cessna.osg"); // could be also .obj files, ...

	osgViewer::Viewer viewer;
	viewer.setSceneData(model);

	viewer.getCamera()->setProjectionMatrixAsPerspective(40., 1., 1., 100.);

	osg::Matrix trans;
	osg::Matrix rot;

	trans.makeTranslate(0., 0., -10.);

	myKeyboardEventHandler* myEventHandler = new myKeyboardEventHandler();
	viewer.addEventHandler(myEventHandler);

	// Enter a simulation loop
	while(!viewer.done()) {
		rot.makeRotate(angle, osg::Vec3(1., 0., 0.));

		viewer.getCamera()->setViewMatrix(trans * rot);	

		viewer.frame();
	}

	return 0;
}
