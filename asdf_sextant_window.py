# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/lion/workspace/code/asdf_sextant/asdf_sextant_window.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(1201, 818)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 700))
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.select_file_button = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.select_file_button.setFont(font)
        self.select_file_button.setObjectName(_fromUtf8("select_file_button"))
        self.horizontalLayout.addWidget(self.select_file_button)
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.central_tab = QtGui.QTabWidget(self.centralwidget)
        self.central_tab.setObjectName(_fromUtf8("central_tab"))
        self.waveform_tab = QtGui.QWidget()
        self.waveform_tab.setObjectName(_fromUtf8("waveform_tab"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout(self.waveform_tab)
        self.horizontalLayout_13.setObjectName(
            _fromUtf8("horizontalLayout_13")
        )
        self.waveform_vertical_splitter = QtGui.QSplitter(self.waveform_tab)
        self.waveform_vertical_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.waveform_vertical_splitter.setObjectName(
            _fromUtf8("waveform_vertical_splitter")
        )
        self.layoutWidget = QtGui.QWidget(self.waveform_vertical_splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem1)
        self.close_file_button = QtGui.QPushButton(self.layoutWidget)
        self.close_file_button.setObjectName(_fromUtf8("close_file_button"))
        self.horizontalLayout_3.addWidget(self.close_file_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.open_files_list_widget = QtGui.QListWidget(self.layoutWidget)
        self.open_files_list_widget.setMinimumSize(QtCore.QSize(0, 125))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.open_files_list_widget.setFont(font)
        self.open_files_list_widget.setObjectName(
            _fromUtf8("open_files_list_widget")
        )
        self.verticalLayout_3.addWidget(self.open_files_list_widget)
        self.waveform_left_side_splitter = QtGui.QSplitter(self.layoutWidget)
        self.waveform_left_side_splitter.setOrientation(QtCore.Qt.Vertical)
        self.waveform_left_side_splitter.setObjectName(
            _fromUtf8("waveform_left_side_splitter")
        )
        self.station_view = StationTreeWidget(self.waveform_left_side_splitter)
        self.station_view.setAnimated(False)
        self.station_view.setHeaderHidden(True)
        self.station_view.setObjectName(_fromUtf8("station_view"))
        self.station_view.headerItem().setText(0, _fromUtf8("1"))
        self.web_view = QtWebKit.QWebView(self.waveform_left_side_splitter)
        self.web_view.setProperty("url", QtCore.QUrl(_fromUtf8("about:blank")))
        self.web_view.setObjectName(_fromUtf8("web_view"))
        self.verticalLayout_3.addWidget(self.waveform_left_side_splitter)
        self.layoutWidget1 = QtGui.QWidget(self.waveform_vertical_splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.reset_view_push_button = QtGui.QPushButton(self.layoutWidget1)
        self.reset_view_push_button.setEnabled(False)
        self.reset_view_push_button.setObjectName(
            _fromUtf8("reset_view_push_button")
        )
        self.horizontalLayout_2.addWidget(self.reset_view_push_button)
        spacerItem2 = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem2)
        self.detrend_and_demean_check_box = QtGui.QCheckBox(self.layoutWidget1)
        self.detrend_and_demean_check_box.setObjectName(
            _fromUtf8("detrend_and_demean_check_box")
        )
        self.horizontalLayout_2.addWidget(self.detrend_and_demean_check_box)
        self.normalize_check_box = QtGui.QCheckBox(self.layoutWidget1)
        self.normalize_check_box.setObjectName(
            _fromUtf8("normalize_check_box")
        )
        self.horizontalLayout_2.addWidget(self.normalize_check_box)
        spacerItem3 = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem3)
        self.custom_processing_check_box = QtGui.QCheckBox(self.layoutWidget1)
        self.custom_processing_check_box.setText(_fromUtf8(""))
        self.custom_processing_check_box.setObjectName(
            _fromUtf8("custom_processing_check_box")
        )
        self.horizontalLayout_2.addWidget(self.custom_processing_check_box)
        self.custom_processing_push_button = QtGui.QPushButton(
            self.layoutWidget1
        )
        self.custom_processing_push_button.setObjectName(
            _fromUtf8("custom_processing_push_button")
        )
        self.horizontalLayout_2.addWidget(self.custom_processing_push_button)
        spacerItem4 = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem4)
        self.references_push_button = QtGui.QPushButton(self.layoutWidget1)
        self.references_push_button.setObjectName(
            _fromUtf8("references_push_button")
        )
        self.horizontalLayout_2.addWidget(self.references_push_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.graph = GraphicsLayoutWidget(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graph.sizePolicy().hasHeightForWidth()
        )
        self.graph.setSizePolicy(sizePolicy)
        self.graph.setMouseTracking(False)
        self.graph.setToolTip(_fromUtf8(""))
        self.graph.setObjectName(_fromUtf8("graph"))
        self.verticalLayout_2.addWidget(self.graph)
        self.horizontalLayout_13.addWidget(self.waveform_vertical_splitter)
        self.central_tab.addTab(self.waveform_tab, _fromUtf8("Waveforms"))
        self.auxiliary_data_tab = QtGui.QWidget()
        self.auxiliary_data_tab.setObjectName(_fromUtf8("auxiliary_data_tab"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.auxiliary_data_tab)
        self.horizontalLayout_11.setObjectName(
            _fromUtf8("horizontalLayout_11")
        )
        self.auxiliary_data_tree_view = QtGui.QTreeWidget(
            self.auxiliary_data_tab
        )
        self.auxiliary_data_tree_view.setObjectName(
            _fromUtf8("auxiliary_data_tree_view")
        )
        self.auxiliary_data_tree_view.headerItem().setText(0, _fromUtf8("1"))
        self.auxiliary_data_tree_view.header().setVisible(False)
        self.horizontalLayout_11.addWidget(self.auxiliary_data_tree_view)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.auxiliary_data_stacked_widget = QtGui.QStackedWidget(
            self.auxiliary_data_tab
        )
        self.auxiliary_data_stacked_widget.setObjectName(
            _fromUtf8("auxiliary_data_stacked_widget")
        )
        self.auxiliary_data_graph_page = QtGui.QWidget()
        self.auxiliary_data_graph_page.setObjectName(
            _fromUtf8("auxiliary_data_graph_page")
        )
        self.horizontalLayout_8 = QtGui.QHBoxLayout(
            self.auxiliary_data_graph_page
        )
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.auxiliary_data_graph = GraphicsLayoutWidget(
            self.auxiliary_data_graph_page
        )
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.auxiliary_data_graph.sizePolicy().hasHeightForWidth()
        )
        self.auxiliary_data_graph.setSizePolicy(sizePolicy)
        self.auxiliary_data_graph.setMouseTracking(False)
        self.auxiliary_data_graph.setToolTip(_fromUtf8(""))
        self.auxiliary_data_graph.setObjectName(
            _fromUtf8("auxiliary_data_graph")
        )
        self.horizontalLayout_8.addWidget(self.auxiliary_data_graph)
        self.auxiliary_data_stacked_widget.addWidget(
            self.auxiliary_data_graph_page
        )
        self.auxiliary_data_file_page = QtGui.QWidget()
        self.auxiliary_data_file_page.setObjectName(
            _fromUtf8("auxiliary_data_file_page")
        )
        self.horizontalLayout_9 = QtGui.QHBoxLayout(
            self.auxiliary_data_file_page
        )
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.auxiliary_file_browser = QtGui.QTextBrowser(
            self.auxiliary_data_file_page
        )
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Andale Mono"))
        font.setPointSize(12)
        self.auxiliary_file_browser.setFont(font)
        self.auxiliary_file_browser.setObjectName(
            _fromUtf8("auxiliary_file_browser")
        )
        self.horizontalLayout_9.addWidget(self.auxiliary_file_browser)
        self.auxiliary_data_stacked_widget.addWidget(
            self.auxiliary_data_file_page
        )
        self.verticalLayout_4.addWidget(self.auxiliary_data_stacked_widget)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(
            _fromUtf8("horizontalLayout_10")
        )
        self.show_auxiliary_provenance_button = QtGui.QPushButton(
            self.auxiliary_data_tab
        )
        self.show_auxiliary_provenance_button.setEnabled(False)
        self.show_auxiliary_provenance_button.setAutoDefault(False)
        self.show_auxiliary_provenance_button.setDefault(False)
        self.show_auxiliary_provenance_button.setFlat(False)
        self.show_auxiliary_provenance_button.setObjectName(
            _fromUtf8("show_auxiliary_provenance_button")
        )
        self.horizontalLayout_10.addWidget(
            self.show_auxiliary_provenance_button
        )
        spacerItem5 = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum
        )
        self.horizontalLayout_10.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.groupBox = QtGui.QGroupBox(self.auxiliary_data_tab)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.auxiliary_data_info_table_view = QtGui.QTableWidget(self.groupBox)
        self.auxiliary_data_info_table_view.setObjectName(
            _fromUtf8("auxiliary_data_info_table_view")
        )
        self.auxiliary_data_info_table_view.setColumnCount(0)
        self.auxiliary_data_info_table_view.setRowCount(0)
        self.auxiliary_data_info_table_view.horizontalHeader().setSortIndicatorShown(
            False
        )
        self.horizontalLayout_5.addWidget(self.auxiliary_data_info_table_view)
        self.horizontalLayout_7.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.auxiliary_data_tab)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.auxiliary_data_detail_table_view = QtGui.QTableWidget(
            self.groupBox_2
        )
        self.auxiliary_data_detail_table_view.setObjectName(
            _fromUtf8("auxiliary_data_detail_table_view")
        )
        self.auxiliary_data_detail_table_view.setColumnCount(0)
        self.auxiliary_data_detail_table_view.setRowCount(0)
        self.horizontalLayout_6.addWidget(
            self.auxiliary_data_detail_table_view
        )
        self.horizontalLayout_7.addWidget(self.groupBox_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_11.addLayout(self.verticalLayout_4)
        self.horizontalLayout_11.setStretch(0, 3)
        self.horizontalLayout_11.setStretch(1, 10)
        self.central_tab.addTab(self.auxiliary_data_tab, _fromUtf8(""))
        self.provenance_tab = QtGui.QWidget()
        self.provenance_tab.setObjectName(_fromUtf8("provenance_tab"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.provenance_tab)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.provenance_list_view = QtGui.QListView(self.provenance_tab)
        self.provenance_list_view.setObjectName(
            _fromUtf8("provenance_list_view")
        )
        self.horizontalLayout_4.addWidget(self.provenance_list_view)
        self.provenance_graphics_view = SvgGraphicsView(self.provenance_tab)
        self.provenance_graphics_view.setObjectName(
            _fromUtf8("provenance_graphics_view")
        )
        self.horizontalLayout_4.addWidget(self.provenance_graphics_view)
        self.horizontalLayout_4.setStretch(0, 3)
        self.horizontalLayout_4.setStretch(1, 10)
        self.central_tab.addTab(self.provenance_tab, _fromUtf8(""))
        self.event_tab = QtGui.QWidget()
        self.event_tab.setObjectName(_fromUtf8("event_tab"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout(self.event_tab)
        self.horizontalLayout_12.setObjectName(
            _fromUtf8("horizontalLayout_12")
        )
        self.event_tree_widget = QtGui.QTreeWidget(self.event_tab)
        self.event_tree_widget.setObjectName(_fromUtf8("event_tree_widget"))
        self.event_tree_widget.headerItem().setText(0, _fromUtf8("1"))
        self.event_tree_widget.header().setVisible(False)
        self.horizontalLayout_12.addWidget(self.event_tree_widget)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.events_web_view = QtWebKit.QWebView(self.event_tab)
        self.events_web_view.setProperty(
            "url", QtCore.QUrl(_fromUtf8("about:blank"))
        )
        self.events_web_view.setObjectName(_fromUtf8("events_web_view"))
        self.verticalLayout_5.addWidget(self.events_web_view)
        self.events_text_browser = QtGui.QTextBrowser(self.event_tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Andale Mono"))
        font.setPointSize(12)
        self.events_text_browser.setFont(font)
        self.events_text_browser.setObjectName(
            _fromUtf8("events_text_browser")
        )
        self.verticalLayout_5.addWidget(self.events_text_browser)
        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 1)
        self.horizontalLayout_12.addLayout(self.verticalLayout_5)
        self.horizontalLayout_12.setStretch(0, 4)
        self.horizontalLayout_12.setStretch(1, 6)
        self.central_tab.addTab(self.event_tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.central_tab)
        MainWindow.setCentralWidget(self.centralwidget)
        self.status_bar = QtGui.QStatusBar(MainWindow)
        self.status_bar.setObjectName(_fromUtf8("status_bar"))
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)
        self.central_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            _translate("MainWindow", "ASDF Sextant", None)
        )
        self.select_file_button.setText(
            _translate("MainWindow", "Open File", None)
        )
        self.label.setText(
            _translate(
                "MainWindow",
                "Or just drag & drop an ASDF file into this window",
                None,
            )
        )
        self.label_2.setText(_translate("MainWindow", "Open Files", None))
        self.close_file_button.setText(
            _translate("MainWindow", "Close File", None)
        )
        self.station_view.setSortingEnabled(False)
        self.reset_view_push_button.setText(
            _translate("MainWindow", "Reset View", None)
        )
        self.detrend_and_demean_check_box.setText(
            _translate("MainWindow", "Detrend and Demean", None)
        )
        self.normalize_check_box.setText(
            _translate("MainWindow", "Normalize", None)
        )
        self.custom_processing_push_button.setText(
            _translate("MainWindow", "Custom Processing", None)
        )
        self.references_push_button.setText(
            _translate("MainWindow", "References", None)
        )
        self.show_auxiliary_provenance_button.setText(
            _translate("MainWindow", "Show Provenance", None)
        )
        self.groupBox.setTitle(
            _translate("MainWindow", "Data Information", None)
        )
        self.groupBox_2.setTitle(_translate("MainWindow", "Parameters", None))
        self.central_tab.setTabText(
            self.central_tab.indexOf(self.auxiliary_data_tab),
            _translate("MainWindow", "Auxiliary Data", None),
        )
        self.central_tab.setTabText(
            self.central_tab.indexOf(self.provenance_tab),
            _translate("MainWindow", "Provenance", None),
        )
        self.central_tab.setTabText(
            self.central_tab.indexOf(self.event_tab),
            _translate("MainWindow", "Events", None),
        )


from PyQt4 import QtWebKit
from pyqtgraph import GraphicsLayoutWidget
from station_tree_widget import StationTreeWidget
from svg_graphics_view import SvgGraphicsView
