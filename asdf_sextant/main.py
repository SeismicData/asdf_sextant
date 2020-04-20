#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Graphical utility to visualize ASDF files.

:copyright:
    Lion Krischer (lion.krischer@gmail.com), 2013-2020
:license:
    MIT
"""
from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QDesktopWidget
import pyqtgraph as pg
import qdarkstyle

import collections
import itertools
import os
import platform
import subprocess
import sys
import threading
import time
import tempfile

import numpy as np
from obspy.core import AttribDict
import obspy.core.event
import pyasdf

from .DateAxisItem import DateAxisItem
from . import asdf_sextant_window
from .python_syntax_highlighting import PythonHighlighter


# Enums only exists in Python 3 and we don't really need them here...
STATION_VIEW_ITEM_TYPES = {
    "NETWORK": 0,
    "STATION": 1,
    "STATIONXML": 2,
    "WAVEFORM": 3,
}

EVENT_VIEW_ITEM_TYPES = {"EVENT": 0, "ORIGIN": 1, "MAGNITUDE": 2, "FOCMEC": 3}

AUX_DATA_ITEM_TYPES = {"DATA_TYPE": 0, "DATA_ITEM": 1}


# Colors for the datasets.
DATASET_COLORS = [
    "#CCCCCC",
    "#32B165",
    "#A38CF4",
    "#CE8F31",
    "#F67088",
    "#38A7D0",
    "#96A331",
]


# Default to antialiased drawing.
pg.setConfigOptions(
    antialias=True, foreground=(200, 200, 200), background=None
)


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


def make_icon(colors, width=24, height=24):
    """
    Make a QIcon with all the desired colors.
    """
    pm = QtGui.QPixmap(width, height)
    p = QtGui.QPainter(pm)

    # Draw stripes.
    for _i, color in enumerate(colors):
        x = int(round(_i * width / len(colors)))
        y = 0
        w = int(round((_i + 1) * width / len(colors))) - x
        h = height
        p.fillRect(x, y, w, h, QtGui.QColor(color))

    p.end()

    return QtGui.QIcon(pm)


__filename_memoization_dict = {}


def resolve_filename(filename):
    """
    Resolves filename.

    Really only needed for some version of OSX that return posix files ids
    for the drop events.

    :param filename: The filename to resolve.
    """
    # The osascript call might be expensive - cache it.
    if filename not in __filename_memoization_dict:
        # Only affects OSX.
        if platform.system().lower() != "darwin":
            return filename

        # Only resolve file ids.
        if "/.file/id" not in filename:
            return filename

        # This is slow and complicated but appears to be the most reasonable
        # solution.
        process = subprocess.Popen(
            [
                "osascript",
                "-e",
                "get posix path of my posix file "
                '"file://%s" -- kthx. bai' % filename,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = process.communicate()
        # Might fail for any number of reasons.
        if process.returncode != 0:
            __filename_memoization_dict[filename] = filename
            return filename
        if hasattr(out, "decode"):
            out = out.decode()
        __filename_memoization_dict[filename] = out.strip()

    return __filename_memoization_dict[filename]


class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = asdf_sextant_window.Ui_MainWindow()  # NOQA
        self.ui.setupUi(self)

        self.provenance_list_model = QtGui.QStandardItemModel(
            self.ui.provenance_list_view
        )
        self.ui.provenance_list_view.setModel(self.provenance_list_model)

        # Station view.
        map_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "resources/index.html")
        )
        self.ui.web_engine_view.load(QtCore.QUrl.fromLocalFile(map_file))

        # Event view.
        map_file = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "resources/index_event.html"
            )
        )
        self.ui.events_web_engine_view.load(
            QtCore.QUrl.fromLocalFile(map_file)
        )

        # Trial and error to find reasonable initial sizes of the splitters.
        # This can probably be done in a simpler way but it appears to work.
        self.ui.waveform_vertical_splitter.setSizes([20, 250])
        self.ui.waveform_left_side_splitter.setSizes([30, 30])

        self._state = {
            # Initially open the file-open dialogue in the current working
            # directory. For subsequent cases the parent dir of the
            # previously chosen file will be used.
            "file_open_dir": os.path.abspath(os.getcwd()),
            "custom_processing_script": (
                "# This function will modify each waveform stream. It must\n"
                "# be called process() and it takes three arguments: \n"
                "#\n"
                "# * st: The obspy.Stream object with the waveforms.\n"
                "# * inv: The obspy.Inventory object with the metadata.\n"
                "# * tag: The name of the currently selected tag.\n\n"
                "import numpy as np\n\n\n"
                "def process(st, inv, tag):\n"
                "    # Do whatever you want in here, but return st.\n"
                "    return st"
            ),
        }

        self._open_files = collections.OrderedDict()

        tmp = tempfile.mkstemp("asdf_sextant")
        os.close(tmp[0])
        try:
            os.remove(tmp[1])
        except Exception:
            pass
        self._tempfile = tmp[1] + ".svg"

        # Install an event filter to intercept all drop events; also those
        # on child events.
        class EventFilter(QtCore.QObject):
            def eventFilter(self, obj, event):
                if not isinstance(
                    event, (QtGui.QDragEnterEvent, QtGui.QDragMoveEvent)
                ):
                    return False

                def _get_filenames(event):
                    try:
                        paths = [
                            resolve_filename(_i.path())
                            for _i in event.mimeData().urls()
                        ]
                    except Exception:
                        return False
                    for p in paths:
                        if not os.path.isfile(p) or not p.endswith(".h5"):
                            return False
                    return paths

                # We always only deal with HDF5 files.
                filenames = _get_filenames(event)
                if not filenames:
                    return False

                event.acceptProposedAction()
                return True

        filter = EventFilter(self)
        self.installEventFilter(filter)

        self.setAcceptDrops(True)

    def dropEvent(self, event):
        """
        Enable drag and drop for ASDF files.
        """
        # The drag enter and move already assert that the file exists and
        # that it ends with `.h5`.
        filenames = [
            resolve_filename(_i.path()) for _i in event.mimeData().urls()
        ]
        for filename in filenames:
            self.open_file(filename=filename)

    def __del__(self):
        try:
            os.remove(self._tempfile)
        except Exception:
            pass

    def __connect_signal_and_slots(self):
        """
        Connect special signals and slots not covered by the named signals and
        slots from pyuic4.
        """
        self.ui.station_view.itemEntered.connect(
            self.on_station_view_itemEntered
        )
        self.ui.station_view.itemExited.connect(
            self.on_station_view_itemExited
        )

    def _update(self):
        # First try to reset everything.
        self.ui.open_files_list_widget.clear()
        # Remove all stations from the map.
        self.ui.web_engine_view.page().runJavaScript("removeAllStations()")
        # Same for the events
        self.ui.events_web_engine_view.page().runJavaScript(
            "removeAllEvents()"
        )
        # Clear provenance list.
        self.provenance_list_model.clear()
        # Clear station view list.
        self.ui.station_view.clear()
        # Clear all the events.
        self.ui.events_text_browser.clear()
        self.ui.event_tree_widget.clear()
        # Last but not least of course also the auxiliary data.
        self.ui.auxiliary_data_tree_view.clear()
        self.ui.auxiliary_data_graph.clear()
        self.ui.auxiliary_data_detail_table_view.clear()
        self.ui.auxiliary_data_info_table_view.clear()
        self.ui.auxiliary_file_browser.clear()
        self.ui.show_auxiliary_provenance_button.setEnabled(False)

        # Collect all coordinates.
        all_coordinates = {}

        for filename, info in self._open_files.items():
            # First fill the open files list.
            _f = filename.split(os.sep)
            text = "[%s] %s" % (
                info["ds"].pretty_filesize,
                # Shortened absolute path.
                "/".join([_i[:1] for _i in _f[:-1]] + _f[-1:]),
            )

            item = QtGui.QListWidgetItem(
                make_icon(colors=[info["color"]]), text
            )
            # Make it non-selectable.
            item.setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.open_files_list_widget.addItem(item)

            # Add station coordinates.
            for k, v in info["contents"].items():
                if "coordinates" in v:
                    all_coordinates[k] = v["coordinates"]

        # Add all stations to the map.
        for k, c in all_coordinates.items():
            js_call = "addStation('{station_id}', {latitude}, {longitude})"
            if "latitude" not in c or "longitude" not in c:
                continue
            self.ui.web_engine_view.page().runJavaScript(
                js_call.format(
                    station_id=k,
                    latitude=c["latitude"],
                    longitude=c["longitude"],
                )
            )

        # Add provenance.
        prov = set()
        for v in self._open_files.values():
            for p in v["provenance"]:
                prov.add(p)
        prov = sorted(prov)
        for provenance in sorted(prov):
            item = QtGui.QStandardItem(provenance)
            self.provenance_list_model.appendRow(item)

        # Show station and event lists.
        self.build_station_view_list()
        self.build_event_tree_view()

        # Also add the auxiliary data.
        def recursive_tree(name, item):
            if isinstance(item, pyasdf.utils.AuxiliaryDataAccessor):
                data_type_item = QtGui.QTreeWidgetItem(
                    [name], type=AUX_DATA_ITEM_TYPES["DATA_TYPE"]
                )
                children = []
                for sub_item in item.list():
                    children.append(recursive_tree(sub_item, item[sub_item]))
                data_type_item.addChildren(children)
            elif isinstance(item, pyasdf.utils.AuxiliaryDataContainer):
                data_type_item = QtGui.QTreeWidgetItem(
                    [name], type=AUX_DATA_ITEM_TYPES["DATA_ITEM"]
                )
            else:
                raise NotImplementedError
            return data_type_item

        file_items = []

        for filename, info in self._open_files.items():
            items = []
            # Deal with a missing auxiliary group.
            try:
                aux_items = info["ds"].auxiliary_data.list()
            except KeyError:
                aux_items = []
            for data_type in aux_items:
                items.append(
                    recursive_tree(
                        data_type, info["ds"].auxiliary_data[data_type]
                    )
                )
            if not items:
                continue
            f = QtGui.QTreeWidgetItem([filename])
            f.setIcon(0, make_icon([info["color"]]))
            f.addChildren(items)
            file_items.append(f)

        if file_items:
            self.ui.auxiliary_data_tree_view.insertTopLevelItems(0, file_items)

    def open_file(self, filename):
        # Don't open again.
        if filename in self._open_files:
            return
        ds = pyasdf.ASDFDataSet(filename, mode="r")

        station_info = {}

        for station in ds.waveforms:
            info = {}

            try:
                info["coordinates"] = station.coordinates
            except Exception:
                pass

            info["waveform_tags"] = station.get_waveform_tags()
            info["has_stationxml"] = "StationXML" in station

            station_info[station._station_name] = info

        # Get the first unused dataset color.
        used_colors = [_i["color"] for _i in self._open_files.values()]
        for color in DATASET_COLORS:
            if color in used_colors:
                continue
            break

        try:
            prov = ds.provenance.list()
        except KeyError:
            prov = []

        self._open_files[filename] = {
            "ds": ds,
            "color": color,
            "contents": station_info,
            "provenance": prov,
            "events": ds.events,
        }

        self._update()

    def build_event_tree_view(self):
        events = {}
        for v in self._open_files.values():
            for event in v["events"]:
                res_id = str(event.resource_id)
                if res_id in events:
                    continue
                events[res_id] = event
        self.ui.event_tree_widget.clear()

        items = []
        self._state["quake_ids"] = {}

        for event in events.values():
            if event.origins:
                org = event.preferred_origin() or event.origins[0]

                js_call = "addEvent('{event_id}', {latitude}, {longitude});".format(  # NOQA
                    event_id=event.resource_id.id,
                    latitude=org.latitude,
                    longitude=org.longitude,
                )
                self.ui.events_web_engine_view.page().runJavaScript(js_call)

            event_item = QtGui.QTreeWidgetItem(
                [event.resource_id.id], type=EVENT_VIEW_ITEM_TYPES["EVENT"]
            )
            self._state["quake_ids"][event.resource_id.id] = event_item

            origin_item = QtGui.QTreeWidgetItem(["Origins"], type=-1)
            magnitude_item = QtGui.QTreeWidgetItem(["Magnitudes"], type=-1)
            focmec_item = QtGui.QTreeWidgetItem(["Focal Mechanisms"], type=-1)

            org_items = []
            for origin in event.origins:
                org_items.append(
                    QtGui.QTreeWidgetItem(
                        [origin.resource_id.id],
                        type=EVENT_VIEW_ITEM_TYPES["ORIGIN"],
                    )
                )
                self._state["quake_ids"][origin.resource_id.id] = org_items[-1]
            origin_item.addChildren(org_items)

            mag_items = []
            for magnitude in event.magnitudes:
                mag_items.append(
                    QtGui.QTreeWidgetItem(
                        [magnitude.resource_id.id],
                        type=EVENT_VIEW_ITEM_TYPES["MAGNITUDE"],
                    )
                )
                self._state["quake_ids"][magnitude.resource_id.id] = mag_items[
                    -1
                ]
            magnitude_item.addChildren(mag_items)

            focmec_items = []
            for focmec in event.focal_mechanisms:
                focmec_items.append(
                    QtGui.QTreeWidgetItem(
                        [focmec.resource_id.id],
                        type=EVENT_VIEW_ITEM_TYPES["FOCMEC"],
                    )
                )
                self._state["quake_ids"][focmec.resource_id.id] = focmec_items[
                    -1
                ]
            focmec_item.addChildren(focmec_items)

            event_item.addChildren([origin_item, magnitude_item, focmec_item])
            items.append(event_item)

        self.ui.event_tree_widget.insertTopLevelItems(0, items)

    def build_station_view_list(self):
        if not self._open_files:
            return
        self.ui.station_view.clear()

        # Merge stations.
        all_stations = {}
        for info in self._open_files.values():
            for station_name, v in info["contents"].items():
                if station_name in all_stations:
                    s = all_stations[station_name]
                else:
                    s = collections.defaultdict(list)
                for tag in v["waveform_tags"]:
                    s[tag].append({"color": info["color"], "ds": info["ds"]})

                if "has_stationxml" in v:
                    s["StationXML"].append({"color": info["color"]})

                all_stations[station_name] = s

        # Sort is important for the group-by operation to work correctly.
        all_stations = sorted(all_stations.items(), key=lambda x: x[0])

        items = []
        for key, group in itertools.groupby(
            all_stations, key=lambda x: x[0].split(".")[0]
        ):

            network_item = QtGui.QTreeWidgetItem(
                [key], type=STATION_VIEW_ITEM_TYPES["NETWORK"]
            )
            all_colors_for_network = set()
            group = sorted(group, key=lambda x: x[0])

            for name, content in group:
                station_item = QtGui.QTreeWidgetItem(
                    [name.split(".")[-1]],
                    type=STATION_VIEW_ITEM_TYPES["STATION"],
                )

                all_colors_for_station = set()

                children = []
                content = sorted(content.items(), key=lambda x: x[0])
                # First StationXML.
                for tag, info in content:
                    if tag != "StationXML":
                        continue
                    c = [_i["color"] for _i in info]
                    all_colors_for_station.update(c)
                    icon = make_icon(colors=c)
                    children.append(
                        QtGui.QTreeWidgetItem(
                            [tag], type=STATION_VIEW_ITEM_TYPES["STATIONXML"]
                        )
                    )
                    children[-1].setIcon(0, icon)
                # Then the rest - sorry for being lazy.
                for tag, info in content:
                    if tag == "StationXML":
                        continue
                    c = [_i["color"] for _i in info]
                    all_colors_for_station.update(c)
                    icon = make_icon(colors=c)
                    children.append(
                        QtGui.QTreeWidgetItem(
                            [tag], type=STATION_VIEW_ITEM_TYPES["WAVEFORM"]
                        )
                    )
                    children[-1].setIcon(0, icon)
                station_item.addChildren(children)
                station_item.setIcon(0, make_icon(all_colors_for_station))
                all_colors_for_network.update(all_colors_for_station)

                network_item.addChild(station_item)
            network_item.setIcon(0, make_icon(all_colors_for_network))
            items.append(network_item)

        self.ui.station_view.insertTopLevelItems(0, items)

    @QtCore.Slot()
    def on_close_file_button_released(self):
        popup = QtGui.QMenu()

        for filename, info in self._open_files.items():

            def get_action_fct():
                _filename = filename

                def _action(check):
                    del self._open_files[_filename]["ds"]
                    del self._open_files[_filename]
                    self._update()

                return _action

            # Bind with a closure.
            popup.addAction(
                make_icon([info["color"]]), "Close %s" % filename
            ).triggered.connect(get_action_fct())

        popup.exec_(
            self.ui.close_file_button.parentWidget().mapToGlobal(
                self.ui.close_file_button.pos()
            )
        )

    @QtCore.Slot()
    def on_custom_processing_push_button_released(self):
        new_processing_script, ok = ProcessingScriptDialog.edit(
            self._state["custom_processing_script"]
        )

        # If cancel or something else has been pressed, just return
        if ok is not True:
            return

        self._state["custom_processing_script"] = new_processing_script
        self.update_waveform_plot()

    @QtCore.Slot()
    def on_reset_view_push_button_released(self):
        self.reset_view()

    def show_provenance_for_id(self, prov_id):
        for v in self._open_files.values():
            try:
                info = v["ds"].provenance.get_provenance_document_for_id(
                    prov_id
                )
                break
            except Exception:
                pass
        else:
            msg_box = QtGui.QMessageBox()
            msg_box.setText("Could not find provenance document.")
            msg_box.exec_()
            return

        # Find the item.
        item = self.provenance_list_model.findItems(info["name"])[0]
        index = self.provenance_list_model.indexFromItem(item)
        self.ui.provenance_list_view.setCurrentIndex(index)
        self.show_provenance_document(info["name"])
        self.ui.central_tab.setCurrentWidget(self.ui.provenance_tab)

    def show_referenced_object(self, object_type, object_id):
        if object_type.lower() == "provenance":
            self.show_provenance_for_id(object_id)
        else:
            self.show_event(attribute=object_type.lower(), object_id=object_id)

    def show_event(self, attribute, object_id):
        item = self._state["quake_ids"][object_id]
        self.ui.event_tree_widget.collapseAll()
        self.ui.event_tree_widget.setCurrentItem(item)

        self.on_event_tree_widget_itemClicked(item, 0)

        self.ui.central_tab.setCurrentWidget(self.ui.event_tab)

    @QtCore.Slot()
    def on_show_auxiliary_provenance_button_released(self):
        if (
            "current_auxiliary_data_provenance_id" not in self._state
            or not self._state["current_auxiliary_data_provenance_id"]
        ):
            return
        self.show_provenance_for_id(
            self._state["current_auxiliary_data_provenance_id"]
        )

    @QtCore.Slot()
    def on_references_push_button_released(self):
        if "current_station_objects" not in self._state:
            return
        objects = self._state["current_station_objects"]

        main_popup = QtGui.QMenu()

        for filename, obj in objects.items():
            ds = self._open_files[filename]["ds"]
            popup = main_popup.addMenu(
                make_icon([self._open_files[filename]["color"]]), filename
            )
            for waveform in obj.list():
                if not waveform.endswith(
                    "__" + self._state["current_waveform_tag"]
                ):
                    continue
                menu = popup.addMenu(waveform)
                attributes = dict(
                    ds._waveform_group[obj._station_name][waveform].attrs
                )

                for key, value in sorted(
                    [_i for _i in attributes.items()], key=lambda x: x[0]
                ):
                    if not key.endswith("_id"):
                        continue
                    key = key[:-3].capitalize()

                    try:
                        value = value.decode()
                    except Exception:
                        pass

                    def get_action_fct():
                        _key = key
                        _value = value

                        def _action(check):
                            self.show_referenced_object(_key, _value)

                        return _action

                    # Bind with a closure.
                    menu.addAction("%s: %s" % (key, value)).triggered.connect(
                        get_action_fct()
                    )

        main_popup.exec_(
            self.ui.references_push_button.parentWidget().mapToGlobal(
                self.ui.references_push_button.pos()
            )
        )

    @QtCore.Slot()
    def on_select_file_button_released(self):
        """
        Fill the station tree widget upon opening a new file.
        """
        filename = QtGui.QFileDialog.getOpenFileName(
            parent=self,
            caption="Choose File",
            directory=self._state["file_open_dir"],
            filter="ASDF files (*.h5)",
        )
        if not filename:
            return

        # Open the parent dir of the current file the next time the file
        # dialogue is opened.
        self._state["file_open_dir"] = os.path.dirname(filename[0])

        self.open_file(filename[0])

    @QtCore.Slot(int)
    def on_custom_processing_check_box_stateChanged(self, state):
        self.update_waveform_plot()

    @QtCore.Slot(int)
    def on_detrend_and_demean_check_box_stateChanged(self, state):
        self.update_waveform_plot()

    @QtCore.Slot(int)
    def on_normalize_check_box_stateChanged(self, state):
        self.update_waveform_plot()

    def update_waveform_plot(self):
        if not hasattr(self, "st"):
            return

        self.ui.reset_view_push_button.setEnabled(True)

        # Get the filter settings.
        filter_settings = {}
        filter_settings[
            "detrend_and_demean"
        ] = self.ui.detrend_and_demean_check_box.isChecked()
        filter_settings["normalize"] = self.ui.normalize_check_box.isChecked()

        temp_st = self.st.copy()

        if self.ui.custom_processing_check_box.isChecked():
            # Load code.
            _d = _DynamicModule()
            _d.load(self._state["custom_processing_script"])
            processing_function = _d.process

            # Try to find the stationxml file.
            inv = None
            for station_object in self._state[
                "current_station_objects"
            ].values():
                try:
                    inv = station_object.StationXML
                    break
                except Exception:
                    pass

            # Execute it.
            temp_st = processing_function(
                st=temp_st, inv=inv, tag=self._state["current_waveform_tag"]
            )
        else:
            if filter_settings["detrend_and_demean"]:
                temp_st.detrend("linear")
                temp_st.detrend("demean")

            if filter_settings["normalize"]:
                temp_st.normalize()

        self.ui.graph.clear()

        starttimes = []
        endtimes = []
        min_values = []
        max_values = []

        self._state["waveform_plots"] = collections.OrderedDict()

        # Plot per component!
        components = sorted(set(tr.stats.channel[-1] for tr in temp_st))
        for _i, component in enumerate(components):
            st = [tr for tr in temp_st if tr.stats.channel[-1] == component]
            plot = self.ui.graph.addPlot(
                _i,
                0,
                title=st[0].id,
                axisItems={
                    "bottom": DateAxisItem(orientation="bottom", utcOffset=0)
                },
            )
            plot.show()
            self._state["waveform_plots"][component] = plot
            for tr in st:
                plot.plot(
                    tr.times() + tr.stats.starttime.timestamp,
                    tr.data,
                    pen=QtGui.QColor(tr.stats.__color),
                )
                starttimes.append(tr.stats.starttime)
                endtimes.append(tr.stats.endtime)
                min_values.append(tr.data.min())
                max_values.append(tr.data.max())

        self._state["waveform_plots_min_time"] = min(starttimes)
        self._state["waveform_plots_max_time"] = max(endtimes)
        self._state["waveform_plots_min_value"] = min(min_values)
        self._state["waveform_plots_max_value"] = max(max_values)

        wf = list(self._state["waveform_plots"].values())
        for plot in wf[1:]:
            plot.setXLink(wf[0])
            plot.setYLink(wf[0])

        self.reset_view()

    def reset_view(self):
        wf = list(self._state["waveform_plots"].values())[0]

        wf.setXRange(
            self._state["waveform_plots_min_time"].timestamp,
            self._state["waveform_plots_max_time"].timestamp,
        )
        min_v = self._state["waveform_plots_min_value"]
        max_v = self._state["waveform_plots_max_value"]

        y_range = max_v - min_v
        min_v -= 0.1 * y_range
        max_v += 0.1 * y_range
        wf.setYRange(min_v, max_v)

    def show_provenance_document(self, document_name):
        for v in self._open_files.values():
            if document_name in v["ds"].provenance:
                doc = v["ds"].provenance[document_name]
                break
        else:
            msg_box = QtGui.QMessageBox()
            msg_box.setText("Could not find provenance document.")
            msg_box.exec_()
            return

        doc.plot(filename=self._tempfile, use_labels=True)

        self.ui.provenance_graphics_view.open_file(self._tempfile)

    @QtCore.Slot(QtGui.QTreeWidgetItem, int)
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

            for v in self._open_files.values():
                if (
                    station in v["contents"]
                    and v["contents"][station]["has_stationxml"]
                ):
                    try:
                        v["ds"].waveforms[station].StationXML.plot_response(
                            0.001
                        )
                    except Exception:
                        continue
                    break
            else:
                msg_box = QtGui.QMessageBox()
                msg_box.setText("Could not find StationXML document.")
                msg_box.exec_()
                return

        elif t == STATION_VIEW_ITEM_TYPES["WAVEFORM"]:
            station = get_station(item)
            tag = item.text(0)
            self._state["current_waveform_tag"] = tag

            self._state["current_station_objects"] = {}
            st = obspy.Stream()
            for filename, info in self._open_files.items():
                if station not in info["ds"].waveforms:
                    continue
                _station = info["ds"].waveforms[station]
                self._state["current_station_objects"][filename] = _station
                if tag not in _station:
                    continue
                # Store the color for each trace.
                _st = _station[tag]
                for tr in _st:
                    tr.stats.__color = info["color"]
                    tr.stats.sextant = AttribDict()
                    tr.stats.sextant.filename = filename
                st += _st
            self.st = st
            self.update_waveform_plot()
        else:
            pass

    @QtCore.Slot(QtGui.QTreeWidgetItem, int)
    def on_event_tree_widget_itemClicked(self, item, column):
        t = item.type()
        if t not in EVENT_VIEW_ITEM_TYPES.values():
            return

        text = str(item.text(0))

        res_id = obspy.core.event.ResourceIdentifier(id=text)

        obj = res_id.get_referred_object()
        if obj is None:
            msg_box = QtGui.QMessageBox()
            msg_box.setText("Did not find the correct event.")
            msg_box.exec_()
            return
        self.ui.events_text_browser.setPlainText(
            str(res_id.get_referred_object())
        )

        if t == EVENT_VIEW_ITEM_TYPES["EVENT"]:
            event = text
        elif t == EVENT_VIEW_ITEM_TYPES["ORIGIN"]:
            event = str(item.parent().parent().text(0))
        elif t == EVENT_VIEW_ITEM_TYPES["MAGNITUDE"]:
            event = str(item.parent().parent().text(0))
        elif t == EVENT_VIEW_ITEM_TYPES["FOCMEC"]:
            event = str(item.parent().parent().text(0))

        js_call = "highlightEvent('{event_id}');".format(event_id=event)
        self.ui.events_web_engine_view.page().runJavaScript(js_call)

    @QtCore.Slot(QtGui.QTreeWidgetItem, int)
    def on_auxiliary_data_tree_view_itemClicked(self, item, column):
        t = item.type()
        if t != AUX_DATA_ITEM_TYPES["DATA_ITEM"]:
            return

        tag = str(item.text(0))

        def recursive_path(item):
            p = item.parent()
            if p is None:
                return []
            path = [str(p.text(0))]
            path.extend(recursive_path(p))
            return path

        # Find the full path.
        path = recursive_path(item)
        path.reverse()

        filename = path[0]
        path = path[1:]

        graph = self.ui.auxiliary_data_graph
        graph.clear()

        ds = self._open_files[filename]["ds"]

        group = ds.auxiliary_data["/".join(path)]
        aux_data = group[tag]

        # Files are a bit special.
        if len(aux_data.data.shape) == 1 and path[0].lower() in [
            "file",
            "files",
        ]:
            self.ui.auxiliary_file_browser.setPlainText(
                aux_data.file.read().decode()
            )
            self.ui.auxiliary_data_stacked_widget.setCurrentWidget(
                self.ui.auxiliary_data_file_page
            )
        elif (
            len(aux_data.data.shape) == 1
            or sum(aux_data.data.shape[1:]) == len(aux_data.data.shape) - 1
        ):
            plot = graph.addPlot(title="%s/%s" % ("/".join(path), tag))
            plot.show()

            data = aux_data.data[()].ravel()

            npts = len(data)
            t = np.arange(npts)
            if path[0].lower() in [
                "crosscorrelation",
                "crosscorrelations",
                "xcorr",
                "xcorrs",
                "corr",
                "corrs",
                "correlation",
                "correlations",
            ]:
                dt_names = ["dt", "delta", "sample_spacing", "sample_interval"]
                dt_names += [_i.upper() for _i in dt_names]
                dt_names += [_i.capitalize() for _i in dt_names]

                dt = None
                for key in dt_names:
                    if key in aux_data.parameters:
                        dt = aux_data.parameters[key]
                        break
                if dt:
                    length = (npts - 1) * dt
                    t = np.linspace(-length / 2.0, length / 2.0, npts)
                    plot.setLabel(axis="bottom", text="Lag Time [s]")

            plot.plot(t, data)
            self.ui.auxiliary_data_stacked_widget.setCurrentWidget(
                self.ui.auxiliary_data_graph_page
            )
        # 2D Shapes.
        elif len(aux_data.data.shape) == 2:
            # If 6 or less components on the first dimensions and a lot on
            # the second, assume its a 2D array of time series.
            if aux_data.data.shape[0] <= 6 and aux_data.data.shape[1] >= 100:
                first_plot = None
                for _i in range(aux_data.data.shape[0]):
                    plot = graph.addPlot(_i, 0)
                    plot.plot(aux_data.data.value[_i])
                    # Link plots.
                    if _i == 0:
                        first_plot = plot
                    else:
                        plot.setXLink(first_plot)
                        plot.setYLink(first_plot)
                self.ui.auxiliary_data_stacked_widget.setCurrentWidget(
                    self.ui.auxiliary_data_graph_page
                )
            # Otherwise assume its a 2D image.
            else:
                img = pg.ImageItem(border="#3D8EC9")
                img.setImage(aux_data.data.value)
                vb = graph.addViewBox()
                vb.setAspectLocked(True)
                vb.addItem(img)
                self.ui.auxiliary_data_stacked_widget.setCurrentWidget(
                    self.ui.auxiliary_data_graph_page
                )
        # Anything else is currently not supported.
        else:
            raise NotImplementedError

        # Show the parameters.
        tv = self.ui.auxiliary_data_detail_table_view
        tv.clear()

        self._state[
            "current_auxiliary_data_provenance_id"
        ] = aux_data.provenance_id
        if aux_data.provenance_id:
            self.ui.show_auxiliary_provenance_button.setEnabled(True)
        else:
            self.ui.show_auxiliary_provenance_button.setEnabled(False)

        tv.setRowCount(len(aux_data.parameters))
        tv.setColumnCount(2)
        tv.setHorizontalHeaderLabels(["Parameter", "Value"])
        tv.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        tv.verticalHeader().hide()

        for _i, key in enumerate(sorted(aux_data.parameters.keys())):
            key_item = QtGui.QTableWidgetItem(key)
            v = aux_data.parameters[key]
            try:
                v = v.decode()
            except Exception:
                pass
            value_item = QtGui.QTableWidgetItem(str(v))

            tv.setItem(_i, 0, key_item)
            tv.setItem(_i, 1, value_item)

        # Show details about the data.
        details = [
            ("shape", str(aux_data.data.shape)),
            ("dtype", str(aux_data.data.dtype)),
            ("dimensions", str(len(aux_data.data.shape))),
            (
                "uncompressed size",
                sizeof_fmt(aux_data.data.dtype.itemsize * aux_data.data.size),
            ),
        ]

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

    @QtCore.Slot(QtCore.QModelIndex)
    def on_provenance_list_view_clicked(self, model_index):
        # Compat for different pyqt/sip versions.
        try:
            data = str(model_index.data().toString())
        except Exception:
            data = str(model_index.data())

        self.show_provenance_document(data)

    @QtCore.Slot(QtGui.QTreeWidgetItem)
    def on_station_view_itemEntered(self, item):
        t = item.type()

        def get_station(item, parent=True):
            if parent:
                station = str(item.parent().text(0))
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
            self.ui.web_engine_view.page().runJavaScript(js_call)
        elif t == STATION_VIEW_ITEM_TYPES["STATION"]:
            station = get_station(item, parent=False)
            js_call = "highlightStation('{station}')".format(station=station)
            self.ui.web_engine_view.page().runJavaScript(js_call)
        elif t == STATION_VIEW_ITEM_TYPES["STATIONXML"]:
            station = get_station(item)
            js_call = "highlightStation('{station}')".format(station=station)
            self.ui.web_engine_view.page().runJavaScript(js_call)
        elif t == STATION_VIEW_ITEM_TYPES["WAVEFORM"]:
            station = get_station(item)
            js_call = "highlightStation('{station}')".format(station=station)
            self.ui.web_engine_view.page().runJavaScript(js_call)
        else:
            pass

    @QtCore.Slot()
    def on_station_view_itemExited(self, *args):
        js_call = "setAllInactive()"
        self.ui.web_engine_view.page().runJavaScript(js_call)


class NoTabQPlainTextEdit(QtGui.QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super(NoTabQPlainTextEdit, self).__init__(*args, **kwargs)

        self.textChanged.connect(self.on_text_changed)

    def keyPressEvent(self, key):
        if key.text() == "\t":
            self.insertPlainText("    ")
        else:
            super(NoTabQPlainTextEdit, self).keyPressEvent(key)

    @QtCore.Slot()
    def on_text_changed(self, *args):
        # Convert all tabs to spaces - will be called for example on text
        # pasting.
        txt = self.toPlainText()
        if "\t" in txt:
            txt = txt.replace("\t", "    ")
            self.setPlainText(txt)


class ProcessingScriptDialog(QtGui.QDialog):
    def __init__(self, parent=None, script=""):
        super(ProcessingScriptDialog, self).__init__(parent)
        self.resize(800, 500)

        self.setWindowTitle("Edit Custom Processing Script")

        layout = QtGui.QVBoxLayout(self)

        label = QtGui.QLabel(
            "Edit this script for flexible custom "
            "processing using all of ObsPy and the Python "
            "ecosystem!"
        )
        layout.addWidget(label)

        self.editor = NoTabQPlainTextEdit()

        self.hl = PythonHighlighter(self.editor.document())
        self.editor.setPlainText(script)

        layout.addWidget(self.editor)

        # OK and Cancel buttons
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_script(self):
        return str(self.editor.toPlainText())

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def edit(script, parent=None):
        dialog = ProcessingScriptDialog(parent=parent, script=script)
        result = dialog.exec_()
        return (dialog.get_script(), result == QtGui.QDialog.Accepted)


class _DynamicModule(object):
    """
    From https://stackoverflow.com/a/5371449.
    """

    def load(self, code):
        execdict = {}  # optional, to increase safety
        exec(code, execdict)
        keys = execdict.get(
            "__all__",  # use __all__ attribute if defined
            # else all non-private attributes
            (key for key in execdict if not key.startswith("_")),
        )
        for key in keys:
            setattr(self, key, execdict[key])


def launch():
    import argparse

    parser = argparse.ArgumentParser(description="Visualize ASDF files.")

    parser.add_argument(
        "filename",
        metavar="ASDF-FILE",
        type=str,
        help="Directly open a file.",
        nargs="?",
    )

    args = parser.parse_args()

    if args.filename and not os.path.exists(args.filename):
        raise ValueError(f"'{args.filename}' does not exist.")

    # Launch and open the window.
    app = QtGui.QApplication(sys.argv)

    # Set application name for OS - does not work on OSX but seems to work
    # on others.
    app.setApplicationName("ASDF Sextant")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

    # Set the application icon
    app_icon = QtGui.QIcon()
    app_icon.addFile(
        os.path.join(os.path.dirname(__file__), "icon.png"),
        QtCore.QSize(1024, 1024),
    )
    app.setWindowIcon(app_icon)

    window = Window()

    # Move window to center of screen.
    window_rect = window.frameGeometry()
    window_rect.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(window_rect.topLeft())

    # Delayed file open to give some time for the javascript to catch up.
    if args.filename:

        def delayed_file_open():
            time.sleep(2)
            window.open_file(args.filename)

        t = threading.Thread(target=delayed_file_open)
        t.start()

    # Show and bring window to foreground.
    window.show()
    app.installEventFilter(window)
    window.raise_()
    ret_val = app.exec_()
    window.__del__()
    os._exit(ret_val)


if __name__ == "__main__":
    launch()
