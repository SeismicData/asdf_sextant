import sip

try:
    sip.setapi("QString", 2)
except:
    pass

from PyQt4 import QtGui, QtSvg, QtCore  # NOQA


class SvgGraphicsView(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(SvgGraphicsView, self).__init__(parent)

        # Native renderer
        self.renderer = 0
        self.setViewport(QtGui.QWidget())
        self.svgItem = None

        self.setScene(QtGui.QGraphicsScene(self))
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)

    def open_file(self, filename):
        svg_file = QtCore.QFile(filename)

        if not svg_file.exists():
            return

        s = self.scene()

        s.clear()
        self.resetTransform()

        self.svgItem = QtSvg.QGraphicsSvgItem(svg_file.fileName())
        self.svgItem.setFlags(QtGui.QGraphicsItem.ItemClipsToShape)
        self.svgItem.setCacheMode(QtGui.QGraphicsItem.NoCache)
        self.svgItem.setZValue(0)

        s.addItem(self.svgItem)

        s.setSceneRect(self.svgItem.boundingRect().adjusted(-10, -10, 10, 10))

    def wheelEvent(self, event):
        factor = 1.2 ** (event.delta() / 240.0)
        self.scale(factor, factor)
        event.accept()
