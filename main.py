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

from PyQt4 import QtGui, QtCore, QtWebKit
import pyqtgraph as pg
import qdarkstyle

from glob import iglob
import imp
import inspect
import itertools
import os
import sys

import pyasdf

from DateAxisItem import DateAxisItem


# Enums only exists in Python 3 and we don't really need them here...
STATION_VIEW_ITEM_TYPES = {
    "NETWORK": 0,
    "STATION": 1,
    "STATIONXML": 2,
    "WAVEFORM": 3}

AUX_DATA_ITEM_TYPES = {
    "DATA_TYPE": 0,
    "TAG": 1}


# Default to antialiased drawing.
pg.setConfigOptions(antialias=True, foreground=(200, 200, 200),
                    background=None)


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


def sizeof_fmt(num):
    """
    Handy formatting for human readable filesize.

    From http://stackoverflow.com/a/1094933/1657047
    """
    for x in ["bytes", "KB", "MB", "GB"]:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, "TB")


class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        # Injected by the compile_and_import_ui_files() function.
        self.ui = sd5_sextant_window.Ui_MainWindow()  # NOQA
        self.ui.setupUi(self)

        self.provenance_list_model = QtGui.QStandardItemModel(
            self.ui.provenance_list_view)
        self.ui.provenance_list_view.setModel(self.provenance_list_model)

        map_file = os.path.abspath("resources/index.html")
        self.ui.web_view.load(QtCore.QUrl.fromLocalFile(map_file))
        # Enable debugging of the web view.
        self.ui.web_view.settings().setAttribute(
            QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)

        self._state = {}

    def __connect_signal_and_slots(self):
        """
        Connect special signals and slots not covered by the named signals and
        slots from pyuic4.
        """
        self.ui.station_view.itemEntered.connect(
            self.on_station_view_itemEntered)
        self.ui.station_view.itemExited.connect(
            self.on_station_view_itemExited)

    def build_station_view_list(self):
        if not hasattr(self, "ds") or not self.ds:
            return
        self.ui.station_view.clear()

        items = []

        if self.ui.group_by_network_check_box.isChecked():
            for key, group in itertools.groupby(
                    self.ds.waveforms,
                    key=lambda x: x._station_name.split(".")[0]):
                network_item = QtGui.QTreeWidgetItem(
                    [key],
                    type=STATION_VIEW_ITEM_TYPES["NETWORK"])
                group = sorted(group, key=lambda x: x._station_name)
                for station in sorted(group, key=lambda x: x._station_name):
                    station_item = QtGui.QTreeWidgetItem([
                        station._station_name.split(".")[-1]],
                        type=STATION_VIEW_ITEM_TYPES["STATION"])

                    contents = dir(station)
                    waveform_contents = sorted([
                        _i for _i in contents
                        if _i not in ("StationXML", "_station_name",
                                      "coordinates", "channel_coordinates")])

                    # Add children.
                    children = []
                    if "StationXML" in contents:
                        children.append(
                            QtGui.QTreeWidgetItem(
                                ["StationXML"],
                                type=STATION_VIEW_ITEM_TYPES["STATIONXML"]))
                    for waveform in waveform_contents:
                        children.append(
                            QtGui.QTreeWidgetItem(
                                [waveform],
                                type=STATION_VIEW_ITEM_TYPES["WAVEFORM"]))
                    station_item.addChildren(children)

                    network_item.addChild(station_item)
                items.append(network_item)

        else:
            # Add all the waveforms and stations.
            for station in self.ds.waveforms:
                item = QtGui.QTreeWidgetItem(
                    [station._station_name],
                    type=STATION_VIEW_ITEM_TYPES["STATION"])

                contents = dir(station)
                waveform_contents = sorted([
                    _i for _i in contents
                    if _i not in ("StationXML", "_station_name", "coordinates",
                                  "channel_coordinates")])

                # Add children.
                children = []
                if "StationXML" in contents:
                    children.append(
                        QtGui.QTreeWidgetItem(
                            ["StationXML"],
                            type=STATION_VIEW_ITEM_TYPES["STATIONXML"]))
                for waveform in waveform_contents:
                    children.append(
                        QtGui.QTreeWidgetItem(
                            [waveform],
                            type=STATION_VIEW_ITEM_TYPES["WAVEFORM"]))
                item.addChildren(children)

                items.append(item)

        self.ui.station_view.insertTopLevelItems(0, items)

    def on_reset_view_push_button_released(self):
        self.reset_view()

    def on_select_file_button_released(self):
        """
        Fill the station tree widget upon opening a new file.
        """
        self.filename = str(QtGui.QFileDialog.getOpenFileName(
            parent=self, caption="Choose File",
            directory=os.path.expanduser("~"),
            filter="SD5 files (*.h5 *.sd5)"))
        if not self.filename:
            return

        self.ds = pyasdf.ASDFDataSet(self.filename)

        for station_id, coordinates in self.ds.get_all_coordinates().items():
            if not coordinates:
                continue
            js_call = "addStation('{station_id}', {latitude}, {longitude})"
            self.ui.web_view.page().mainFrame().evaluateJavaScript(
                js_call.format(station_id=station_id,
                               latitude=coordinates["latitude"],
                               longitude=coordinates["longitude"]))

        self.build_station_view_list()

        # Add all the provenance items
        self.provenance_list_model.clear()
        for provenance in dir(self.ds.provenance):
            item = QtGui.QStandardItem(provenance)
            self.provenance_list_model.appendRow(item)

        # Also add the auxiliary data.
        items = []
        for data_type in sorted(dir(self.ds.auxiliary_data)):
            data_type_item = QtGui.QTreeWidgetItem(
                [data_type],
                type=AUX_DATA_ITEM_TYPES["DATA_TYPE"])

            children = []
            data = getattr(self.ds.auxiliary_data, data_type)
            for tag in sorted(dir(data)):
                children.append(
                    QtGui.QTreeWidgetItem(
                        [tag],
                        type=AUX_DATA_ITEM_TYPES["TAG"]))
            data_type_item.addChildren(children)
            items.append(data_type_item)

        self.ui.auxiliary_data_tree_view.insertTopLevelItems(0, items)

        sb = self.ui.status_bar
        if hasattr(sb, "_widgets"):
            for i in sb._widgets:
                sb.removeWidget(i)

        w = QtGui.QLabel("File: %s    (%s)" % (self.ds.filename,
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

    def on_group_by_network_check_box_stateChanged(self, state):
        self.build_station_view_list()

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

        #from PyQt4.QtCore import pyqtRemoveInputHook
        #pyqtRemoveInputHook()
        #from IPython.core.debugger import Tracer; Tracer(colors="Linux")()

        starttimes = []
        endtimes = []
        min_values = []
        max_values = []

        self._state["waveform_plots"] = []
        for _i, tr in enumerate(temp_st):
            plot = self.ui.graph.addPlot(
                _i, 0, title=tr.id,
                axisItems={'bottom': DateAxisItem(orientation='bottom',
                                                  utcOffset=0)})
            plot.show()
            self._state["waveform_plots"].append(plot)
            plot.plot(tr.times() + tr.stats.starttime.timestamp, tr.data)
            starttimes.append(tr.stats.starttime)
            endtimes.append(tr.stats.endtime)
            min_values.append(tr.data.min())
            max_values.append(tr.data.max())

        self._state["waveform_plots_min_time"] = min(starttimes)
        self._state["waveform_plots_max_time"] = max(endtimes)
        self._state["waveform_plots_min_value"] = min(min_values)
        self._state["waveform_plots_max_value"] = max(max_values)

        for plot in self._state["waveform_plots"][1:]:
            plot.setXLink(self._state["waveform_plots"][0])
            plot.setYLink(self._state["waveform_plots"][0])

        self.reset_view()

    def reset_view(self):
        self._state["waveform_plots"][0].setXRange(
            self._state["waveform_plots_min_time"].timestamp,
            self._state["waveform_plots_max_time"].timestamp)
        min_v = self._state["waveform_plots_min_value"]
        max_v = self._state["waveform_plots_max_value"]

        y_range = max_v - min_v
        min_v -= 0.1 * y_range
        max_v += 0.1 * y_range
        self._state["waveform_plots"][0].setYRange(min_v, max_v)

    def show_provenance_document(self, document_name):
        tmp_svg = "temp.svg"
        doc = getattr(self.ds.provenance, document_name)
        doc.plot(filename=tmp_svg, use_labels=True)

        self.ui.provenance_graphics_view.open_file(tmp_svg)

    def on_station_view_itemClicked(self, item, column):
        t = item.type()

        def get_station(item):
            station = item.parent().text(0)
            if "." not in station:
                station = item.parent().parent().text(0) + "." + station
            return station

        if t == STATION_VIEW_ITEM_TYPES["NETWORK"]:
            pass
        elif t == STATION_VIEW_ITEM_TYPES["STATION"]:
            pass
        elif t == STATION_VIEW_ITEM_TYPES["STATIONXML"]:
            station = get_station(item)
            getattr(getattr(self.ds.waveforms, station.replace(".", "_")),
                    "StationXML").plot_response(0.001)
        elif t == STATION_VIEW_ITEM_TYPES["WAVEFORM"]:
            station = get_station(item)
            self.st = getattr(getattr(
                self.ds.waveforms, station.replace(".", "_")),
                item.text(0)).sort()
            self.update_waveform_plot()
        else:
            pass

    def on_auxiliary_data_tree_view_itemClicked(self, item, column):
        t = item.type()
        if t != AUX_DATA_ITEM_TYPES["TAG"]:
            return

        tag = item.text(0)
        data_type = item.parent().text(0)

        graph = self.ui.auxiliary_data_graph
        graph.clear()

        aux_data = getattr(getattr(self.ds.auxiliary_data, data_type), tag)

        if len(aux_data.data.shape) == 1 and data_type != "File":
            plot = graph.addPlot(title="%s - %s" % (data_type, tag))
            plot.show()
            plot.plot(aux_data.data.value)
            self.ui.auxiliary_data_stacked_widget.setCurrentWidget(
                self.ui.auxiliary_data_graph_page)
        # Files are a bit special.
        elif len(aux_data.data.shape) == 1 and data_type == "File":
            self.ui.auxiliary_file_browser.setPlainText(
                aux_data.file.read().decode())
            self.ui.auxiliary_data_stacked_widget.setCurrentWidget(
                self.ui.auxiliary_data_file_page)
        # 2D Shapes.
        elif len(aux_data.data.shape) == 2:
            img = pg.ImageItem(border="#3D8EC9")
            img.setImage(aux_data.data.value)
            vb = graph.addViewBox()
            vb.setAspectLocked(True)
            vb.addItem(img)
            self.ui.auxiliary_data_stacked_widget.setCurrentWidget(
                self.ui.auxiliary_data_graph_page)
        # Anything else is currently not supported.
        else:
            raise NotImplementedError

        # Show the parameters.
        tv = self.ui.auxiliary_data_detail_table_view
        tv.clear()

        tv.setRowCount(len(aux_data.parameters))
        tv.setColumnCount(2)
        tv.setHorizontalHeaderLabels(["Parameter", "Value"])
        tv.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        tv.verticalHeader().hide()

        for _i, key in enumerate(sorted(aux_data.parameters.keys())):
            key_item = QtGui.QTableWidgetItem(key)
            value_item = QtGui.QTableWidgetItem(str(aux_data.parameters[key]))

            tv.setItem(_i, 0, key_item)
            tv.setItem(_i, 1, value_item)

        # Show details about the data.
        details = [
            ("shape", str(aux_data.data.shape)),
            ("dtype", str(aux_data.data.dtype)),
            ("dimensions", str(len(aux_data.data.shape))),
            ("uncompressed size", sizeof_fmt(
                aux_data.data.dtype.itemsize * aux_data.data.size))]

        tv = self.ui.auxiliary_data_info_table_view
        tv.clear()

        tv.setRowCount(len(details))
        tv.setColumnCount(2)
        tv.setHorizontalHeaderLabels(["Attribute", "Value"])
        tv.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        tv.verticalHeader().hide()

        for _i, item in enumerate(details):
            key_item = QtGui.QTableWidgetItem(item[0])
            value_item = QtGui.QTableWidgetItem(item[1])

            tv.setItem(_i, 0, key_item)
            tv.setItem(_i, 1, value_item)

    def on_provenance_list_view_clicked(self, model_index):
        self.show_provenance_document(model_index.data())

    def on_station_view_itemEntered(self, item):

        t = item.type()

        def get_station(item, parent=True):
            if parent:
                station = item.parent().text(0)
                if "." not in station:
                    station = item.parent().parent().text(0) + "." + station
            else:
                station = item.text(0)
                if "." not in station:
                    station = item.parent().text(0) + "." + station
            return station

        if t == STATION_VIEW_ITEM_TYPES["NETWORK"]:
            network = item.text(0)
            js_call = "highlightNetwork('{network}')".format(network=network)
            self.ui.web_view.page().mainFrame().evaluateJavaScript(js_call)
        elif t == STATION_VIEW_ITEM_TYPES["STATION"]:
            station = get_station(item, parent=False)
            js_call = "highlightStation('{station}')".format(station=station)
            self.ui.web_view.page().mainFrame().evaluateJavaScript(js_call)
        elif t == STATION_VIEW_ITEM_TYPES["STATIONXML"]:
            station = get_station(item)
            js_call = "highlightStation('{station}')".format(station=station)
            self.ui.web_view.page().mainFrame().evaluateJavaScript(js_call)
        elif t == STATION_VIEW_ITEM_TYPES["WAVEFORM"]:
            station = get_station(item)
            js_call = "highlightStation('{station}')".format(station=station)
            self.ui.web_view.page().mainFrame().evaluateJavaScript(js_call)
        else:
            pass

    def on_station_view_itemExited(self, *args):
        js_call = "setAllInactive()"
        self.ui.web_view.page().mainFrame().evaluateJavaScript(js_call)


def launch():
    # Automatically compile all ui files if they have been changed.
    compile_and_import_ui_files()

    # Launch and open the window.
    app = QtGui.QApplication(sys.argv, QtGui.QApplication.GuiClient)
    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    window = Window()

    # Move window to center of screen.
    window.move(
        app.desktop().screen().rect().center() - window.rect().center())

    # Show and bring window to foreground.
    window.show()
    app.installEventFilter(window)
    window.raise_()
    os._exit(app.exec_())


if __name__ == "__main__":
    launch()
