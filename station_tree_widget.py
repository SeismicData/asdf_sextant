from PySide2 import QtGui, QtCore


class StationTreeWidget(QtGui.QTreeWidget):
    # cellExited = QtCore.pyqtSignal(int, int)
    # itemExited = QtCore.pyqtSignal(QtGui.QTreeWidgetItem)

    def __init__(self, *args, **kwargs):
        QtGui.QTreeWidget.__init__(self, *args, **kwargs)
        self._last_index = QtCore.QPersistentModelIndex()
        self.viewport().installEventFilter(self)
        self.setMouseTracking(True)

    def eventFilter(self, widget, event):
        if widget is self.viewport():
            index = self._last_index
            if event.type() == QtCore.QEvent.MouseMove:
                index = self.indexAt(event.pos())
            elif event.type() == QtCore.QEvent.Leave:
                index = QtCore.QModelIndex()
            if index != self._last_index:
                row = self._last_index.row()
                column = self._last_index.column()
                item = self.itemAt(row, column)
                if item is not None:
                    self.itemExited.emit(item)
                self.cellExited.emit(row, column)
                self._last_index = QtCore.QPersistentModelIndex(index)
        return QtGui.QTreeWidget.eventFilter(self, widget, event)
