from PySide2 import QtGui, QtSvg, QtCore, QtWidgets  # NOQA


class SvgGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(SvgGraphicsView, self).__init__(parent)

        # Native renderer
        self.renderer = 0
        self.setViewport(QtWidgets.QWidget())
        self.svgItem = None

        self.setScene(QtWidgets.QGraphicsScene(self))
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)

    def open_file(self, filename):
        svg_file = QtCore.QFile(filename)

        if not svg_file.exists():
            return

        s = self.scene()

        s.clear()
        self.resetTransform()

        self.svgItem = QtSvg.QGraphicsSvgItem(svg_file.fileName())
        self.svgItem.setFlags(QtWidgets.QGraphicsItem.ItemClipsToShape)
        self.svgItem.setCacheMode(QtWidgets.QGraphicsItem.NoCache)
        self.svgItem.setZValue(0)

        s.addItem(self.svgItem)

        s.setSceneRect(self.svgItem.boundingRect().adjusted(-10, -10, 10, 10))

    def wheelEvent(self, event):
        factor = 1.2 ** (event.delta() / 240.0)
        self.scale(factor, factor)
        event.accept()
