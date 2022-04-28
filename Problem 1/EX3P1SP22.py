from PyQt5.QtWidgets import QApplication, QWidget
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from Problem1 import Ui_Form
import sys
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from math import pi, sin
from matplotlib.backends.backend_qt5agg import  NavigationToolbar2QT as NavigationToolbar

class main_window(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupImageLabel()
        self.show()
        self.MakeCanvas()

        # Add navigation toolbar
        self.toolbar=NavigationToolbar(self.canvas,self) #HW10 addition from Smay's code
        # Add navigation controller widget
        self.layout_GridInput.addWidget(self.toolbar) #HW10 addition from Smay's code

    def clickedButton(self):
        """
        This tells the computer to create the graph when the button is clicked.
        """
        # Clearing the previous figure
        self.figure.clear()
        # setting the axis accordingly
        self.ax = self.figure.add_subplot()
        # Creating the new graph using the Create Graph function
        self.createGraph()

    def MakeCanvas(self):
        """
        This was taken from HW8, problem 2 GUI file, with slight modifications.

        Create a place to make graph of currents and voltage over capacitor
        Step 1:  create a Figure object called self.figure
        Step 2:  create a FigureCanvasQTAgg object called self.canvas
        Step 3:  create an axes object for making plot
        Step 4:  add self.canvas to self.gb_Output.layout() which is a grid layout
        :return:
        """
        #Step 1.
        self.figure=Figure(figsize=(2,4),tight_layout=True, frameon=True)
        #Step 2.
        self.canvas=FigureCanvasQTAgg(self.figure)
        #Step 3.
        self.ax = self.figure.add_subplot()
        #Step 4.
        self.layout_GridInput.addWidget(self.canvas, 9,0,1,2)

    def f(self, i, t):
        """
        Taken from Exam2 and modified.
        This creates the ODEs and adds the values we need to solve for using i as a tuple, where t is
        representative of our time in seconds. It then returns the equations for the derivatives of i1 and i2
        to solve more easily using odeint within the main function.
        :param i: tuple used to solve for missing parts
        :param t: time in seconds
        :return: tuple with the equations for i1dot and i2dot
        """
        # I have to turn the le values input by the user into float values so they can be calculated
        R=float(self.le_R.text())
        L=float(self.le_L.text())
        C=float(self.le_C.text())
        Magnitude=float(self.le_Magnitude.text())
        Frequency=float(self.le_Frequency.text())
        Frequency=Frequency*2*pi
        Phase=float(self.le_Phase.text())
        # Designate the values for i1 and i2 to call back later
        i1 = i[0]
        i2 = i[1]
        # Equations for i1dot and i2dot, solved using KVLs from the circuit
        i1dot = (((Magnitude * np.sin((Frequency * t) + Phase)) - R * (i1 - i2)) / L)
        i2dot = i1dot - (i2 / (R * C))
        # Return the ODEs from above as a tuple to solve for i1 and i2 using odeint later
        return [i1dot, i2dot]

    def createGraph(self):
        """
        Taken from Exam2 and modified.
        This function takes the above equations with the missing components and solves them, giving the graph
        with the plots for i1, i2, and Vc(t) all on the same graph, including proper legends and identifiers.
        :return:
        """
        R=float(self.le_R.text())
        tf = 10.0  # final value for t in seconds
        t = np.arange(0, tf, 0.02)  # 500 points for each graph across the time axis

        # Initial conditions
        i0 = [0, 0]
        # Using odeint, we can determine the solution from the above equations of f
        i = odeint(self.f, i0, t)
        i1, i2 = i[:, 0], i[:, 1]
        # Equation for Vc(t)
        vct = R * (i2 - i1)
        # Plot the values of i1, i2, and Vc(t)
        ax1=self.ax
        ax1.clear()
        #fig, ax1 = plt.subplots()
        # Plotting i1 with a solid black line
        ax1.plot(t, i1, '-', color='black')
        # Plotting i2 with a dashed black line
        ax1.plot(t, i2, '--', color='black')
        # Creating the legend for both currents
        ax1.legend(['I1(t)', 'I2(t)'], loc='lower left')
        # Plotting Vc(t) with a dotted black line
        ax2 = ax1.twinx()
        ax2.plot(t, vct, linestyle='dotted', color='black')
        # Label the axes as time, i1/i2, and Vc(t)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('I1 and I2 (A)', color='black')
        ax2.set_ylabel('Vc(t) (V)', color='black')
        # Adding a second legend for Vc(t)
        ax2.legend(['Vc(t)'])
        # Title the plot for the RLC circuit system given
        #plt.title('RLC Circuit Plot')
        # Plot grid lines
        ax1.grid(alpha=0.3)
        ax2.grid(alpha=0.3)
        self.canvas.draw()

    def setupImageLabel(self):
        #region setup a label to display the image of the circuit
        self.pixMap = qtg.QPixmap()
        self.pixMap.load("Circuit1.png")
        self.image_label = qtw.QLabel()
        self.image_label.setPixmap(self.pixMap)
        self.layout_GridInput.addWidget(self.image_label, 8,2,1,2)
        #endregion

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()
    sys.exit(app.exec_())