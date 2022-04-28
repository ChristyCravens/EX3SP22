# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Problem1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1075, 750)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gb_Input = QtWidgets.QGroupBox(Form)
        self.gb_Input.setObjectName("gb_Input")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gb_Input)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layout_GridInput = QtWidgets.QGridLayout()
        self.layout_GridInput.setObjectName("layout_GridInput")
        self.label_6 = QtWidgets.QLabel(self.gb_Input)
        self.label_6.setObjectName("label_6")
        self.layout_GridInput.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gb_Input)
        self.label_2.setObjectName("label_2")
        self.layout_GridInput.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gb_Input)
        self.label_3.setObjectName("label_3")
        self.layout_GridInput.addWidget(self.label_3, 2, 0, 1, 1)
        self.le_Magnitude = QtWidgets.QLineEdit(self.gb_Input)
        self.le_Magnitude.setObjectName("le_Magnitude")
        self.layout_GridInput.addWidget(self.le_Magnitude, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gb_Input)
        self.label_4.setObjectName("label_4")
        self.layout_GridInput.addWidget(self.label_4, 3, 0, 1, 1)
        self.le_Frequency = QtWidgets.QLineEdit(self.gb_Input)
        self.le_Frequency.setObjectName("le_Frequency")
        self.layout_GridInput.addWidget(self.le_Frequency, 4, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gb_Input)
        self.label_5.setObjectName("label_5")
        self.layout_GridInput.addWidget(self.label_5, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gb_Input)
        self.label.setObjectName("label")
        self.layout_GridInput.addWidget(self.label, 0, 0, 1, 1)
        self.le_R = QtWidgets.QLineEdit(self.gb_Input)
        self.le_R.setObjectName("le_R")
        self.layout_GridInput.addWidget(self.le_R, 0, 1, 1, 1)
        self.le_L = QtWidgets.QLineEdit(self.gb_Input)
        self.le_L.setObjectName("le_L")
        self.layout_GridInput.addWidget(self.le_L, 1, 1, 1, 1)
        self.le_Phase = QtWidgets.QLineEdit(self.gb_Input)
        self.le_Phase.setObjectName("le_Phase")
        self.layout_GridInput.addWidget(self.le_Phase, 5, 1, 1, 1)
        self.le_C = QtWidgets.QLineEdit(self.gb_Input)
        self.le_C.setObjectName("le_C")
        self.layout_GridInput.addWidget(self.le_C, 2, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gb_Input)
        self.pushButton.setObjectName("pushButton")
        self.layout_GridInput.addWidget(self.pushButton, 6, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.layout_GridInput)
        self.verticalLayout.addWidget(self.gb_Input)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.clickedButton)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        # Set the window title from default "form" to a legitimate title
        Form.setWindowTitle(_translate("Form", "Circuit Plot"))
        # Setting the title for the user input to "Input"
        self.gb_Input.setTitle(_translate("Form", "Input"))
        # Setting the titles for all of the entries needed from the user
        self.label_6.setText(_translate("Form", "Phase"))
        self.label_2.setText(_translate("Form", "L (H)"))
        self.label_3.setText(_translate("Form", "C (µF)"))
        self.label_4.setText(_translate("Form", "Magnitude"))
        self.label_5.setText(_translate("Form", "Frequency"))
        self.label.setText(_translate("Form", "R (ohms)"))
        # Titling the button to calculate using the input values
        self.pushButton.setText(_translate("Form", "Calculate"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

