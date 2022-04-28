from EX3P2SP22_GUI import Ui_CircuitStructuralDesign
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from EX3P2SP22_stem import CircuitController
import sys

# Modified from Smay's code for HW9

class MainWindow(Ui_CircuitStructuralDesign, qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_Open.clicked.connect(self.OpenFile)
        self.spnd_Zoom.valueChanged.connect(self.setZoom) #$NEW$ double spinner widget for setting zoom level

        self.controller=CircuitController()
        self.controller.setDisplayWidgets((self.te_DesignReport, self.gv_Main))
        self.controller.view.scene.installEventFilter(self)
        self.gv_Main.setMouseTracking(True)

        self.show()

    def setZoom(self):
        self.gv_Main.resetTransform()
        self.gv_Main.scale(self.spnd_Zoom.value(), self.spnd_Zoom.value())

    def eventFilter(self, obj, event):
        """
        This overrides the default eventFilter of the widget.  It takes action on events and then passes the event
        along to the parent widget.
        :param obj: The object on which the event happened
        :param event: The event itself
        :return: boolean from the parent widget
        """
        if obj == self.controller.view.scene:
            et = event.type()
            if et == qtc.QEvent.GraphicsSceneMouseMove:
                scenePos = event.scenePos()
                strScene = "Mouse Position:  x = {}, y = {}".format(round(scenePos.x(), 2), round(-scenePos.y(), 2))
                self.lbl_MousePos.setText(strScene)  # display information in a label
            if event.type() == qtc.QEvent.GraphicsSceneWheel:  # I added this to zoom on mouse wheel scroll
                if event.delta() > 0:
                    self.spnd_Zoom.stepUp()
                else:
                    self.spnd_Zoom.stepDown()
                pass

        # pass the event along to the parent widget if there is one.
        return super(MainWindow, self).eventFilter(obj, event)

    def OpenFile(self):
        filename = qtw.QFileDialog.getOpenFileName()[0]
        if len(filename) == 0:  # no file selected
            return
        self.te_Path.setText(filename)
        file = open(filename, 'r')  # open the file
        data = file.readlines()  # read all the lines of the file into a list of strings
        self.controller.ImportFromFile(data)  # import the pipe network information

def Main():
    app=qtw.QApplication(sys.argv)
    mw=MainWindow()
    sys.exit(app.exec())

if __name__=="__main__":
    Main()