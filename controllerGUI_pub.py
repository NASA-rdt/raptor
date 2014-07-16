
import sys, time
from PyQt4 import QtGui, QtCore
from multiprocessing import Process, Queue
import xbox_read

import rospy
from std_msgs.msg import Int32, String

def scale(x, in_min, in_max, out_min, out_max):
	value = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
	value = min(value,out_max)
	value = max(value, out_min)
	return value

class SavedPosition(QtGui.QWidget):
	def __init__(self,name, position, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.name_root=name[0]
		if (len(name) > 0):
			self.name_extension = name[1]
		else:
			self.name_extension = ''
		self.name = self.name_root + self.name_extension
		self.position=position
		self.button = QtGui.QPushButton(self.name, self)
		self.button.clicked.connect(self.calluser)
	def calluser(self):
		info = 'SavedPosition_%s has position length: %d.' % (self.name,len(self.position)) 
		print(info)

class Communicate(QtCore.QObject):
    
    updateStick = QtCore.pyqtSignal(int, int, int)
    sendCommand = QtCore.pyqtSignal(int)

class Joystick():
	def __init__(self,x,y,inner_rad = 5,outer_rad = 15,scale = 32768): 
		self.center = QtCore.QPoint(x,y)
		self.value=QtCore.QPoint(0,0)
		self.inner_rad = inner_rad
		self.outer_rad = outer_rad
		self.scale = scale
	def setValue(self,index,x):
		val = scale(x,-self.scale,self.scale,-self.outer_rad,self.outer_rad)
		if index == 0:#X
			self.value.setX(-val)
		elif index == 1:#X
			self.value.setY(val)
	def drawWidget(self, qp):
		qp.setBrush(QtGui.QColor(200, 200, 80))
		qp.setPen(QtGui.QColor(0,0,0))#QtGui.QColor(0, 0, 0))
		value = self.center.__sub__(self.value)
		qp.drawEllipse(value,self.inner_rad,self.inner_rad)#drawRect(0, 0, full, h)
	
class ControllerWidget(QtGui.QWidget):
  
    def __init__(self):      
        super(ControllerWidget, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setMinimumSize(200, 200)
	self.joysticks = [Joystick(46,99),Joystick(196,145)]

	fileName = '/home/nasa/Pictures/xbox-controller-hi.png'
	image = QtGui.QImage(fileName)
	if image.isNull():
		QtGui.QMessageBox.information(self, "Image Viewer",
			"Cannot load %s." % fileName)
		return
	pixmap = QtGui.QPixmap.fromImage(image)
	self.pixmap = pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)


    def setValue(self, index, stick, value):
	if(index < len(self.joysticks)):
		self.joysticks[index].setValue(stick,value)
	self.repaint()

#	def resizeEvent(self,e):
#		print 'resized'

    def paintEvent(self, e):
      
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()
      
      
    def drawWidget(self, qp):

        size = self.size()
      	qp.drawPixmap(0,0,self.pixmap)
	for stick in self.joysticks:
		stick.drawWidget(qp)
DEADZONE = 4000
 #     QtCore.QObject.connect(self.processThread, QtCore.SIGNAL("progress(int)"),self.progressBar, #QtCore.SLOT("setValue(int)"), QtCore.Qt.QueuedConnection)
class ControllerCore(QtCore.QThread):

    #This is the signal that will be emitted during the processing.
    #By including int as an argument, it lets the signal know to expect
    #an integer argument when emitting.
    updateProgress = QtCore.pyqtSignal(int,int,int)

    #You can do any extra things in this init you need, but for this example
    #nothing else needs to be done expect call the super's init
    def __init__(self,controller):
        QtCore.QThread.__init__(self)
	self.controller = controller

    #A QThread is run by calling it's start() function, which calls this run()
    #function in it's own "thread". 
    def run(self):
	for event in xbox_read.event_stream():#deadzone = DEADZONE):
		if event.key == 'X1':
			print event.key,':',event.value
			self.updateProgress.emit(0,0,event.value)
		elif event.key == 'Y1':
			print event.key,':',event.value
			self.updateProgress.emit(0,1,event.value)
		elif event.key == 'X2':
			print event.key,':',event.value
			self.updateProgress.emit(1,0,event.value)
		elif event.key == 'Y2':
			print event.key,':',event.value
			self.updateProgress.emit(1,1,event.value)

class RoboGUI(QtGui.QWidget):
	
	def __init__(self):
		super(RoboGUI, self).__init__()
		self.initUI()
	
	def initUI(self):

		#ROS:
		
		self.pubCommands = rospy.Publisher('commands', Int32, queue_size=10)
		self.pubExecute = rospy.Publisher('execute', String, queue_size=10)
		self.pubGripperVal = rospy.Publisher('gripper_value', Int32, queue_size=10)
		self.pubPointEE = rospy.Publisher('ee_pose', Int32, queue_size=10)
		self.pubJointVal = rospy.Publisher('jointVal', Int32, queue_size=10)
		rospy.init_node('ControllerGUI', anonymous=True)
		self.savedPositions = []
		self.c = Communicate()


		self.layout = QtGui.QHBoxLayout()
		self.layoutRight = QtGui.QVBoxLayout()
#build top buttons

		buttonHome = QtGui.QPushButton('Home', self)
		buttonHome.clicked[bool].connect(self.goToPosition)
		buttonSave = QtGui.QPushButton('Save', self)
		buttonSave.clicked[bool].connect(self.savePosition)
		buttonClear = QtGui.QPushButton('Clear', self)
		buttonClear.clicked[bool].connect(self.clearPosition)
        	self.saveName = QtGui.QLineEdit()

		self.layoutTopButtons = QtGui.QGridLayout()
		self.layoutTopButtons.addWidget(buttonHome,0,0)
		self.layoutTopButtons.addWidget(buttonSave,0,1)
		self.layoutTopButtons.addWidget(buttonClear,1,0)
		self.layoutTopButtons.addWidget(self.saveName,1,1)

		self.topButtons = QtGui.QWidget()
		self.topButtons.setLayout(self.layoutTopButtons)
#build middle sliders

		sld_gripper = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		sld_gripper.setFocusPolicy(QtCore.Qt.NoFocus)
		sld_gripper.setGeometry(10, 40, 300, 300)
		sld_gripper.valueChanged[int].connect(self.setGripper)

		sld_wrist = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		sld_wrist.setFocusPolicy(QtCore.Qt.NoFocus)
		sld_wrist.setGeometry(10, 40, 300, 300)
		sld_wrist.valueChanged[int].connect(self.setWrist)

		self.gripperLabel = self.createLabel(self.tr("Gripper Value"))
		self.wristLabel = self.createLabel(self.tr("Wrist Roll"))
		self.layoutMiddleSliders = QtGui.QVBoxLayout()
		self.layoutMiddleSliders.addWidget(self.gripperLabel)
		self.layoutMiddleSliders.addWidget(sld_gripper)
		self.layoutMiddleSliders.addWidget(self.wristLabel)
		self.layoutMiddleSliders.addWidget(sld_wrist)
		#self.layoutMiddleSliders.addWidget(buttonSave,0,1)

		self.middleSliders = QtGui.QWidget()
		self.middleSliders.setLayout(self.layoutMiddleSliders)
#build left side
		self.leftLabel = self.createLabel(self.tr("Available Actions"))
		self.layoutLeft = QtGui.QVBoxLayout()
		self.layoutLeft.addWidget(self.leftLabel)
		self.layoutLeft.addWidget(self.topButtons)
		self.layoutLeft.addWidget(self.middleSliders)
		self.layoutMiddleSliders.addWidget(self.createLabel(self.tr("Controller Input")))
		self.controllerImage = ControllerWidget()
		self.c.updateStick[int,int,int].connect(self.controllerImage.setValue)
		self.controllerImage.setGeometry(300,300,300,300)
		#t1 = Thread(target=getInput, args=[self.controllerImage,])
		#t1.daemon = True
		#t1.start()

		self.controllerProcess = ControllerCore(self.controllerImage)#Process(target=getInput, args=(self.controllerImage,controllerQueue))
		self.controllerProcess.updateProgress.connect(self.controllerImage.setValue)
		self.controllerProcess.start()	

		self.layoutLeft.addWidget(self.controllerImage)
		self.layoutLeft.addStretch(1)

		self.leftSide = QtGui.QWidget()
		self.leftSide.setLayout(self.layoutLeft)

#build right side
		self.camView = QtGui.QLabel()
		#self.camView.setPixmap()
		self.actionLabel = self.createLabel(self.tr("Saved Positions"))
		self.layoutRight = QtGui.QVBoxLayout()
		self.layoutRight.addWidget(self.actionLabel)
		self.layoutRight.addStretch(1)

		self.rightSide = QtGui.QWidget()
		self.rightSide.setLayout(self.layoutRight)
#build divider

		label = QtGui.QLabel()
		label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
		label.setLineWidth(2)
#build layout
		self.layout.addWidget(self.leftSide)
		self.layout.addWidget(label)
		self.layout.addWidget(self.rightSide)

		#elf.middleSliders = QtGui.QWidget()
		#self.middleSliders.setLayout(self.layoutMiddleSliders)


		#self.bottomImage = QtGui.QWidget()
		#self.topButtons.setLayout(self.layoutLeft)

        	self.setLayout(self.layout)
		self.setGeometry(600, 300, 680, 340)
		self.setWindowTitle('Arm Control')
		self.changeStyle('Cleanlooks')
		self.show()
	def goToPosition(self, pressed):
		self.pubExecute.publish('test')
	def changeStyle(self, styleName):
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(styleName))
		QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
		#self.changePalette()

	def changePalette(self):
		if (self.useStylePaletteCheckBox.isChecked()):
			QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
		else:
			QtGui.QApplication.setPalette(self.originalPalette)


	def getPosition(self):
		print 'generating fake joint values...'
		return [1,2,3,4]#want to return real values
	def addButton(self, name,layout=None, index = -1 ):
		print 'creating newButton'
		newPosition = SavedPosition(name,self.getPosition())
		print 'savedPositions:',len(self.savedPositions)
		if( layout is not None):
			if( index >= 0 ):
				layout.insertWidget(index,newPosition.button)
			else:
				layout.addWidget(newPosition.button)
		self.savedPositions.append(newPosition)
		return newPosition

	def createLabel(self, text):
		label = QtGui.QLabel(text)
		label.setAlignment(QtCore.Qt.AlignCenter)
		label.setMargin(2)
		label.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
		return label

	def setGripper(self, value):
		value = scale(value,0.0,100.0,0.0015,0.015)
		print "Setting gripper to %f" % (value)

	def setWrist(self, value):
		print "Setting wrist to %d" % (value)

	def savePosition(self, pressed):
		print "Saving current position..."
		name = self.saveName.text()
		extension = ''
		if( name != '' ):
			inc = 0
			for position in self.savedPositions:
				if name == position.name_root:
					inc+=1
			if(inc > 0):
				extension ='_'+str(inc)
			print 'field is: %s' % self.saveName.text()
		if( name == '' ):
			print 'empty field'
			name = "Saved"
			extension = '_' + str(len(self.savedPositions))
		self.addButton([name,extension],self.layoutRight,1)
	def clearPosition(self, pressed):
		print "Clearing saved positions..."
		for button in self.savedPositions:
			print "removing."
			self.layoutRight.removeWidget(button.button)
    			button.deleteLater()
    			button.button.deleteLater()
		self.savedPositions = []
	def something(self, pressed):
		if pressed:
			isPressed = "True"
		else:
			isPressed = "False"
		print "pressed: %s" % (isPressed)
def main():
	
	app = QtGui.QApplication(sys.argv)
	#app.aboutToQuit.connect(quit)
	ex = RoboGUI()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main() 
