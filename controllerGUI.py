
import sys
from PyQt4 import QtGui, QtCore

def scale(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

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
	def __init__(self,x,y,inner_rad = 5,outer_rad = 15,scale = 100): 
		self.center = QtCore.QPoint(x,y)
		self.value=self.center
		self.inner_rad = inner_rad
		self.outer_rad = outer_rad
		self.scale = scale
	def setValue(self,x,y):
		x = scale(x,-self.scale,self.scale,-self.outer_rad,self.outer_rad)
		y = scale(y,-self.scale,self.scale,-self.outer_rad,self.outer_rad)
		self.value = self.center.__sub__(QtCore.QPoint(x,y))
	def drawWidget(self, qp):
		qp.setBrush(QtGui.QColor(200, 200, 80))
		qp.setPen(QtGui.QColor(0,0,0))#QtGui.QColor(0, 0, 0))
		qp.drawEllipse(self.value,self.inner_rad,self.inner_rad)#drawRect(0, 0, full, h)
	
class Controller(QtGui.QWidget):
  
    def __init__(self):      
        super(Controller, self).__init__()
        
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


    def setValue(self, index, valueX, valueY):
	if(index < len(self.joysticks)):
		print 'changing values..'
		self.joysticks[index].setValue(valueX,valueY)

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


class RoboGUI(QtGui.QWidget):
	
	def __init__(self):
		super(RoboGUI, self).__init__()
		
		self.initUI()
	
	def initUI(self):
		self.savedPositions = []
		self.c = Communicate()


		self.layout = QtGui.QHBoxLayout()
		self.layoutRight = QtGui.QVBoxLayout()
#build top buttons

		buttonHome = QtGui.QPushButton('Home', self)
		buttonHome.setCheckable(False)
		buttonSave = QtGui.QPushButton('Save', self)
		buttonSave.setCheckable(False)
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
		self.controllerImage = Controller()
		self.c.updateStick[int,int,int].connect(self.controllerImage.setValue)
		self.controllerImage.setGeometry(300,300,300,300)
		self.layoutLeft.addWidget(self.controllerImage)
		self.layoutLeft.addStretch(1)

		self.leftSide = QtGui.QWidget()
		self.leftSide.setLayout(self.layoutLeft)

#build right side
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
		self.show()

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
		print "Setting gripper to %d" % (value)
		self.c.updateStick.emit(0,value,value) 
		self.controllerImage.repaint()  
		#self.changeLeftValue(value,value)

	def setWrist(self, value):
		print "Setting wrist to %d" % (value)
		self.c.updateStick.emit(1,value,value)
		self.controllerImage.repaint()
		#self.changeRightValue(value,value)

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
	ex = RoboGUI()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main() 
