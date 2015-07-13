#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Graphical user interface for Instaseis.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2013-2014
:license:
    GNU Lesser General Public License, Version 3 [non-commercial/academic use]
    (http://www.gnu.org/copyleft/lgpl.html)
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

from glob import iglob
import imp
import inspect
import os
import sys


import pyasdf

from DateAxisItem import DateAxisItem


# Default to antialiased drawing.
pg.setConfigOptions(antialias=True, foreground=(50, 50, 50), background=None)


def compile_and_import_ui_files():
    """
    Automatically compiles all .ui files found in the same directory as the
    application py file.
    They will have the same name as the .ui files just with a .py extension.

    Needs to be defined in the same file as function loading the gui as it
    modifies the globals to be able to automatically import the created py-ui
    files. Its just very convenient.
    """
    directory = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    for filename in iglob(os.path.join(directory, '*.ui')):
        ui_file = filename
        py_ui_file = os.path.splitext(ui_file)[0] + os.path.extsep + 'py'
        if not os.path.exists(py_ui_file) or \
                (os.path.getmtime(ui_file) >= os.path.getmtime(py_ui_file)):
            from PyQt4 import uic
            print("Compiling ui file: %s" % ui_file)
            with open(py_ui_file, 'w') as open_file:
                uic.compileUi(ui_file, open_file)
        # Import the (compiled) file.
        try:
            import_name = os.path.splitext(os.path.basename(py_ui_file))[0]
            globals()[import_name] = imp.load_source(import_name, py_ui_file)
        except ImportError as e:
            print("Error importing %s" % py_ui_file)
            print(e.message)


class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        # Injected by the compile_and_import_ui_files() function.
        self.ui = sd5_sextant_window.Ui_MainWindow()  # NOQA
        self.ui.setupUi(self)

    def on_select_file_button_released(self):
        """
        Fill the station tree widget upon opening a new file.
        """
        pwd = os.getcwd()
        self.filename = str(QtGui.QFileDialog.getOpenFileName(
            parent=self, caption="Choose File",
            directory=pwd,
            filter="SD5 files (*.h5 *.sd5)"))
        if not self.filename:
            return

        self.ds = pyasdf.ASDFDataSet(self.filename)

        self.ui.station_view.clear()

        items = []
        for station in self.ds.waveforms:
            item = QtGui.QTreeWidgetItem([station._station_name])

            contents = dir(station)
            waveform_contents = sorted([_i for _i in contents if _i not in
                                        ("StationXML", "_station_name")])

            # Add children.
            children = []
            if "StationXML" in contents:
                children.append(QtGui.QTreeWidgetItem(["StationXML"]))
            for waveform in waveform_contents:
                children.append(QtGui.QTreeWidgetItem([waveform]))
            item.insertChildren(0, children)

            items.append(item)
        self.ui.station_view.insertTopLevelItems(0, items)

        sb = self.ui.status_bar
        if hasattr(sb, "_widgets"):
            for i in sb._widgets:
                sb.removeWidget(i)

        w = QtGui.QLabel("File: %s (%s)" % (self.ds.filename,
                                            self.ds.pretty_filesize))
        sb._widgets = [w]
        sb.addPermanentWidget(w)
        w.show()
        sb.show()
        sb.reformat()

    def on_detrend_and_demean_check_box_stateChanged(self, state):
        self.update_waveform_plot()

    def on_normalize_check_box_stateChanged(self, state):
        self.update_waveform_plot()

    def update_waveform_plot(self):

        #from PyQt4.QtCore import pyqtRemoveInputHook
        #pyqtRemoveInputHook()
        #from IPython.core.debugger import Tracer; Tracer(colors="Linux")()

        # Get the filter settings.
        filter_settings = {}
        filter_settings["detrend_and_demean"] = \
            self.ui.detrend_and_demean_check_box.isChecked()
        filter_settings["normalize"] = self.ui.normalize_check_box.isChecked()

        temp_st = self.st.copy()

        if filter_settings["detrend_and_demean"]:
            temp_st.detrend("linear")
            temp_st.detrend("demean")

        if filter_settings["normalize"]:
            temp_st.normalize()

        self.ui.graph.clear()
        all_plots = []
        for _i, tr in enumerate(temp_st):
            plot = self.ui.graph.addPlot(
                _i, 0, title=tr.id,
                axisItems={'bottom': DateAxisItem(orientation='bottom')})
            all_plots.append(plot)
            plot.plot(tr.times() + tr.stats.starttime.timestamp, tr.data,
                      pen="#333333")

        for plot in all_plots[1:]:
            all_plots[0].setXLink(plot)
            plot.setXLink(all_plots[0])
            all_plots[0].setYLink(plot)
            plot.setYLink(all_plots[0])

    def on_station_view_itemClicked(self, item, column):
        if item.parent() is None:
            return
        station = item.parent().text(0)
        tag = item.text(0)

        if tag == "StationXML":
            return

        self.st = getattr(getattr(self.ds.waveforms,
                                  station.replace(".", "_")), tag).sort()
        self.update_waveform_plot()


def launch():
    # Automatically compile all ui files if they have been changed.
    compile_and_import_ui_files()

    # Launch and open the window.
    app = QtGui.QApplication(sys.argv, QtGui.QApplication.GuiClient)
    window = Window()

    # Show and bring window to foreground.
    window.show()
    app.installEventFilter(window)
    window.raise_()
    os._exit(app.exec_())


if __name__ == "__main__":
    launch()
