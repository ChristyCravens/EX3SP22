import numpy as np
import math
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

# This was edited from Dr. Smay's Truss app, modified to accommodate the changes necessary for the circuit

class Position():
    """
    I made this position for holding a position in 3D space (i.e., a point).  I've given it some ability to do
    vector arithmitic and vector algebra (i.e., a dot product).  I could have used a numpy array, but I wanted
    to create my own.  This class uses operator overloading as explained in the class.
    """

    def __init__(self, pos=None, x=None, y=None, z=None):
        """
        x, y, and z have the expected meanings
        :param pos: a tuple (x,y,z)
        :param x: float
        :param y: float
        :param z: float
        """
        # set default values
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        # unpack position from a tuple if given
        if pos is not None:
            self.x, self.y, self.z = pos
        # override the x,y,z defaults if they are given as arguments
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y
        self.z = z if z is not None else self.z

    # region operator overloads $NEW$ 4/7/21
    def __eq__(self, other):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.z != other.z:
            return False
        return True

    # this is overloading the addition operator.  Allows me to add Position objects with simple math: c=a+b, where
    # a, b, and c are all position objects.
    def __add__(self, other):
        return Position((self.x + other.x, self.y + other.y, self.z + other.z))

    # this overloads the iterative add operator
    def __iadd__(self, other):
        if other in (float, int):
            self.x += other
            self.y += other
            self.z += other
            return self
        if type(other) == Position:
            self.x += other.x
            self.y += other.y
            self.z += other.z
            return self

    # this is overloading the subtraction operator.  Allows me to subtract Positions. (i.e., c=b-a)
    def __sub__(self, other):
        return Position((self.x - other.x, self.y - other.y, self.z - other.z))

    # this overloads the iterative subtraction operator
    def __isub__(self, other):
        if other in (float, int):
            self.x -= other
            self.y -= other
            self.z -= other
            return self
        if type(other) == Position:
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            return self

    # this is overloading the multiply operator.  Allows me to multiply a scalar or do a dot product (i.e., b=s*a or c=b*a)
    def __mul__(self, other):
        if type(other) in (float, int):
            return Position((self.x * other, self.y * other, self.z * other))
        if type(other) is Position:
            return Position((self.x * other.x, self.y * other.y, self.z * other.z))

    # this is overloading the __rmul__ operator so that s*Pt works.
    def __rmul__(self, other):
        return self * other

    # this is overloading the *= operator.  Same as a = Position((a.x*other, a.y*other, a.z*other))
    def __imul__(self, other):
        if type(other) in (float, int):
            self.x *= other
            self.y *= other
            self.z *= other
            return self

    # this is overloading the division operator.  Allows me to divide by a scalar (i.e., b=a/s)
    def __truediv__(self, other):
        if type(other) in (float, int):
            return Position((self.x / other, self.y / other, self.z / other))

    # this is overloading the /= operator.  Same as a = Position((a.x/other, a.y/other, a.z/other))
    def __idiv__(self, other):
        if type(other) in (float, int):
            self.x /= other
            self.y /= other
            self.z /= other
            return self

    # endregion

    def set(self, strXYZ=None, tupXYZ=None):
        # set position by string or tuple
        if strXYZ is not None:
            cells = strXYZ.replace('(', '').replace(')', '').strip().split(',')
            x, y, z = float(cells[0]), float(cells[1]), float(cells[2])
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
        elif tupXYZ is not None:
            x, y, z = tupXYZ  # [0], strXYZ[1],strXYZ[2]
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

    def getTup(self):  # return (x,y,z) as a tuple
        return (self.x, self.y, self.z)

    def getStr(self, nPlaces=3):
        return '{}, {}, {}'.format(round(self.x, nPlaces), round(self.y, nPlaces), round(self.z, nPlaces))

    def mag(self):  # normal way to calculate magnitude of a vector
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def normalize(self):  # typical way to normalize to a unit vector
        l = self.mag()
        if l <= 0.0:
            return
        self.__idiv__(l)

    def getAngleRad(self):
        """
        Gets angle of position relative to an origin (0,0) in the x-y plane
        :return: angle in x-y plane in radians
        """
        l = self.mag()
        if l <= 0.0:
            return 0
        if self.y >= 0.0:
            return math.acos(self.x / l)
        return 2.0 * math.pi - math.acos(self.x / l)
    # pass
    def getAngleDeg(self):
        """
        Gets angle of position relative to an origin (0,0) in the x-y plane
        :return: angle in x-y plane in degrees
        """
        return 180.0 / math.pi * self.getAngleRad()
    # pass

# Changed this class to reflect the components of the resistor
class Component():
    def __init__(self, capacitor=None, inductor=None, resistor=None, voltage=None):
        self.capacitor = capacitor
        self.inductor = inductor
        self.resistor = resistor
        self.voltage = voltage


class Node():
    def __init__(self, name=None, position=None):
        self.name = name
        self.position = position if position is not None else Position()

    def __eq__(self, other):
        """
        This overloads the == operator such that I can compare two nodes to see if they are the same node.  This is
        useful when reading in nodes to make sure I don't get duplicate nodes
        """
        if self.name != other.name:
            return False
        if self.position != other.position:
            return False
        return True


class Link():
    def __init__(self, name="", node1="1", node2="2", length=None, angleRad=None):
        """
        Basic definition of a link contains a name and names of node1 and node2
        """
        self.name = ""
        self.node1_Name = node1
        self.node2_Name = node2
        self.length = None
        self.angleRad = None

    def __eq__(self, other):
        """
        This overloads the == operator for comparing equivalence of two links.
        """
        if self.node1_Name != other.node1_Name: return False
        if self.node2_Name != other.node2_Name: return False
        if self.length != other.length: return False
        if self.angleRad != other.angleRad: return False
        return True

    def set(self, node1=None, node2=None, length=None, angleRad=None):
        self.node1_Name = node1
        self.node2_Name = node2
        self.length = length
        self.angleRad = angleRad


class CircuitModel():
    def __init__(self):
        self.title = None
        self.links = []
        self.nodes = []
        self.component = Component()

    def getNode(self, name):
        for n in self.nodes:
            if n.name == name:
                return n


class CircuitController():
    def __init__(self):
        self.circuit = CircuitModel()
        self.view = CircuitView()

    def ImportFromFile(self, data):
        """
        Data is the list of strings read from the data file.
        We need to parse this file and build the lists of nodes and links that make up the truss.
        Also, we need to parse the lines that give the truss title, material (and strength values).

        Reading Nodes:
        I create a new node object and the set its name and position.x and position.y values.  Next, I check to see
        if the list of nodes in the truss model has this node with self.hasNode(n.name).  If the trussModel does not
        contain the node, I append it to the list of nodes

        Reading Links:
        The links should come after the nodes.  Each link has a name and two node names.  See method addLink
        """
        self.title = None
        # For loop to go through each line of data
        for line in data:
            # Strip all leading and trailing spaces, then split using ',' delimiter
            line = line.strip()
            cells = line.split(',')
            keyword = cells[0].lower().strip()
            # Using keywords to organize appropriate data from txt file
            if keyword == 'title':
                self.circuit.title = cells[1].replace("'", "")
            # Couldn't seem to change material to component without crashing
            elif keyword == 'material':
                self.circuit.component.resistor = float(cells[1])
                self.circuit.component.inductor = float(cells[2])
                self.circuit.component.capacitor = float(cells[3])
            elif keyword == 'voltage':
                self.circuit.component.voltage = cells[1].replace("'", "")
            elif keyword == 'node':
                node = Node()
                node.name = cells[1].strip()
                node.position.x = float(cells[2].strip())
                node.position.y = float(cells[3].strip())
                if self.hasNode(node.name) is False:
                    self.circuit.nodes.append(node)

            elif keyword == 'link':
                link = Link()
                link.name = (cells[1].strip())
                for cell in cells[2:]:
                    link.node1_Name= (cells[2].strip())
                for cell in cells[3:]:
                    link.node2_Name = (cells[3].strip())
                self.circuit.links.append(link)
        self.calcLinkVals()
        self.displayReport()
        self.drawTruss()

    def hasNode(self, name):
        for n in self.circuit.nodes:
            if n.name == name:
                return True
        return False

    def addNode(self, node):
        self.circuit.nodes.append(node)

    def getNode(self, name):
        for n in self.circuit.nodes:
            if n.name == name:
                return n

    def addLink(self, link):
        self.circuit.links.append(link)

    def calcLinkVals(self):
        for l in self.circuit.links:
            n1 = None
            n2 = None
            if self.hasNode(l.node1_Name):
                n1 = self.getNode(l.node1_Name)
            if self.hasNode(l.node2_Name):
                n2 = self.getNode(l.node2_Name)
            if n1 is not None and n2 is not None:
                r = n2.position - n1.position
                l.length = r.mag()
                l.angleRad = r.getAngleRad()

    def setDisplayWidgets(self, args):
        self.view.setDisplayWidgets(args)

    def displayReport(self):
        self.view.displayReport(circuit=self.circuit)

    def drawTruss(self):
        self.view.buildScene(truss=self.circuit)


class CircuitView():
    def __init__(self):
        # setup widgets for display.  redefine these when you have a gui to work with using setDisplayWidgets
        self.scene = qtw.QGraphicsScene()
        self.le_LongLinkName = qtw.QLineEdit()
        self.le_LongLinkNode1 = qtw.QLineEdit()
        self.le_LongLinkNode2 = qtw.QLineEdit()
        self.le_LongLinkLength = qtw.QLineEdit()
        self.te_Report = qtw.QTextEdit()
        self.gv = qtw.QGraphicsView()

        # region setup pens and brushes and scene
        # make the pens first
        # a thick darkGray pen
        self.penLink = qtg.QPen(qtc.Qt.darkGray)
        self.penLink.setWidth(4)
        # a medium darkBlue pen
        self.penNode = qtg.QPen(qtc.Qt.darkBlue)
        self.penNode.setStyle(qtc.Qt.SolidLine)
        self.penNode.setWidth(1)
        # a pen for the grid lines
        self.penGridLines = qtg.QPen()
        self.penGridLines.setWidth(1)
        # I wanted to make the grid lines more subtle, so set alpha=25
        self.penGridLines.setColor(qtg.QColor.fromHsv(197, 144, 228, alpha=50))
        # now make some brushes
        # build a brush for filling with solid red
        self.brushFill = qtg.QBrush(qtc.Qt.darkRed)
        # a brush that makes a hatch pattern
        self.brushNode = qtg.QBrush(qtg.QColor.fromCmyk(0, 0, 255, 0, alpha=100))
        # a brush for the background of my grid
        self.brushGrid = qtg.QBrush(qtg.QColor.fromHsv(87, 98, 245, alpha=128))
        # endregion

    def setDisplayWidgets(self, args):
        self.te_Report = args[0]
        # Since lines of code were unnecessary and removed here, self.gv becomes the second
        # argument instead of the 5th now
        self.gv = args[1]
        self.gv.setScene(self.scene)

    def displayReport(self, circuit=None):
        st = '\tCircuit Design Report\n'
        st += 'Title:  {}\n'.format(circuit.title)
        st += 'Farads:  {:0.2f}\n'.format(circuit.component.capacitor)
        st += 'Henrys:  {:0.2f}\n'.format(circuit.component.inductor)
        st += 'Ohms:  {:0.2f}\n'.format(circuit.component.resistor)
        st += 'Volts:  {}\n'.format(circuit.component.voltage)
        self.te_Report.setText(st)

    def buildScene(self, truss=None):
        # Create a QRect() object to help with drawing the background grid.
        rect = qtc.QRect()
        rect.setTop(truss.nodes[0].position.y)
        rect.setLeft(truss.nodes[0].position.x)
        rect.setHeight(0)
        rect.setWidth(0)
        for n in truss.nodes:
            if n.position.y > rect.top(): rect.setTop(n.position.y)
            if n.position.y < rect.bottom(): rect.setBottom(n.position.y)
            if n.position.x > rect.right(): rect.setRight(n.position.x)
            if n.position.x < rect.left(): rect.setLeft(n.position.x)
        rect.adjust(-50, 0, 50, -150)  # xLeft, Width, Height, yTop

        # clear out the old scene first
        self.scene.clear()

        # draw a grid
        self.drawAGrid(DeltaX=10, DeltaY=10, Height=abs(rect.height()), Width=abs(rect.width()),
                       CenterX=rect.center().x(), CenterY=rect.center().y())
        # draw the truss
        self.drawLinks(truss=truss)
        self.drawNodes(truss=truss)


    def drawAGrid(self, DeltaX=10, DeltaY=10, Height=320, Width=180, CenterX=120, CenterY=60):
        """
        This makes a grid for reference.  No snapping to grid enabled.
        :param DeltaX: grid spacing in x direction
        :param DeltaY: grid spacing in y direction
        :param Height: height of grid (y)
        :param Width: width of grid (x)
        :param CenterX: center of grid (x, in scene coords)
        :param CenterY: center of grid (y, in scene coords)
        :param Pen: pen for grid lines
        :param Brush: brush for background
        :return: nothing
        """
        Pen = self.penGridLines
        Brush = self.brushGrid
        H = self.scene.sceneRect().height() if Height is None else Height
        W = self.scene.sceneRect().width() if Width is None else Width
        L = self.scene.sceneRect().left() if CenterX is None else (CenterX - W / 2.0)
        R = self.scene.sceneRect().right() if CenterX is None else (CenterX + W / 2.0)
        T = self.scene.sceneRect().top() if CenterY is None else (CenterY - H / 2.0)
        B = self.scene.sceneRect().bottom() if CenterY is None else (CenterY + H / 2.0)
        Dx = DeltaX
        Dy = DeltaY
        P = qtg.QPen() if Pen is None else Pen

        # Making the nice background rectangle
        if Brush is not None:
            Rectangle = qtw.QGraphicsRectItem(L, T, W, H)
            Rectangle.setBrush(Brush)
            Rectangle.setPen(P)
            self.scene.addItem(Rectangle)
        # Input vertical lines
        x = L
        while x <= R:
            vertLine = qtw.QGraphicsLineItem(x, T, x, B)
            vertLine.setPen(qtg.QPen(qtc.Qt.lightGray))
            self.scene.addItem(vertLine)
            x += Dx
        # Input horizontal lines
        y = T
        while y <= B:
            horLine = qtw.QGraphicsLineItem(L, y, R, y)
            horLine.setPen(qtg.QPen(qtc.Qt.black))
            self.scene.addItem(horLine)
            y += Dy

    def drawLinks(self, truss=None):
        scene = self.scene
        for n in truss.links:
            n1 = truss.getNode(n.node1_Name)
            n2 = truss.getNode(n.node2_Name)
            p1 = n1.position
            p2 = n2.position
            Link = qtw.QGraphicsLineItem(p1.x, -p1.y, p2.x, -p2.y)
            Link.setPen(self.penLink)
            scene.addItem(Link)

    def drawNodes(self, truss=None, scene=None):
        """
        Draws a circle for each node along with a label and creates the tool tip.
        """
        if scene is None:
            scene = self.scene
        PN = self.penNode
        BN = self.brushNode
        PNOutline = qtg.QPen() if PN is None else PN
        PNLabel = qtg.QPen(qtc.Qt.darkMagenta)
        BNFill = qtg.QBrush() if BN is None else BN
        for n in truss.nodes:
            x = n.position.x
            y = -n.position.y
            self.drawACircle(x, y, 5, brush=BNFill, pen=PNOutline, name=('node:'+'need get name'))
            self.drawALabel(x - 20, y + 2, str=n.name, pen=PNLabel)

    def drawALabel(self, x, y, str='', pen=None, brush=None, tip=None):
        """
        I've decided that x,y are the center of the label.  Find corner based on label width and height.
        """
        scene = self.scene
        lbl = qtw.QGraphicsTextItem(str)
        W = lbl.boundingRect().width()
        H = lbl.boundingRect().height()
        lbl.setX(x - W / 2.0)
        lbl.setY(y - H)
        if tip is not None:
            lbl.setToolTip(tip)
        if pen is not None:
            lbl.setDefaultTextColor(pen.color())
        if brush is not None:
            # this makes a nice background
            bkg = qtw.QGraphicsRectItem(lbl.x(), lbl.y(), W, H)
            bkg.setBrush(brush)
            outlinePen = qtg.QPen(brush.color())
            bkg.setPen(outlinePen)
            scene.addItem(bkg)
        scene.addItem(lbl)

    def drawACircle(self, centerX, centerY, Radius, angle=0, brush=None, pen=None, name=None):
        Ellipse = qtw.QGraphicsEllipseItem(centerX - Radius, centerY - Radius, 2 * Radius, 2 * Radius)
        if pen is not None:
            Ellipse.setPen(pen)
        if brush is not None:
            Ellipse.setBrush(brush)
        self.scene.addItem(Ellipse)