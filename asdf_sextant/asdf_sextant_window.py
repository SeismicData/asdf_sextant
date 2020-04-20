# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asdf_sextant_window.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide2.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QIcon,
    QKeySequence,
    QLinearGradient,
    QPalette,
    QPainter,
    QPixmap,
    QRadialGradient,
)
from PySide2.QtWidgets import *

from PySide2.QtWebEngineWidgets import QWebEngineView

from pyqtgraph import GraphicsLayoutWidget
from .svg_graphics_view import SvgGraphicsView
from .station_tree_widget import StationTreeWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1201, 818)
        MainWindow.setMinimumSize(QSize(1024, 700))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.select_file_button = QPushButton(self.centralwidget)
        self.select_file_button.setObjectName("select_file_button")
        font = QFont()
        font.setPointSize(12)
        self.select_file_button.setFont(font)

        self.horizontalLayout.addWidget(self.select_file_button)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.central_tab = QTabWidget(self.centralwidget)
        self.central_tab.setObjectName("central_tab")
        self.waveform_tab = QWidget()
        self.waveform_tab.setObjectName("waveform_tab")
        self.horizontalLayout_13 = QHBoxLayout(self.waveform_tab)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.waveform_vertical_splitter = QSplitter(self.waveform_tab)
        self.waveform_vertical_splitter.setObjectName(
            "waveform_vertical_splitter"
        )
        self.waveform_vertical_splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.waveform_vertical_splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 2, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.horizontalSpacer_5 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.close_file_button = QPushButton(self.layoutWidget)
        self.close_file_button.setObjectName("close_file_button")

        self.horizontalLayout_3.addWidget(self.close_file_button)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.open_files_list_widget = QListWidget(self.layoutWidget)
        self.open_files_list_widget.setObjectName("open_files_list_widget")
        self.open_files_list_widget.setMinimumSize(QSize(0, 125))
        self.open_files_list_widget.setMaximumSize(QSize(400, 150))
        font1 = QFont()
        font1.setPointSize(10)
        self.open_files_list_widget.setFont(font1)

        self.verticalLayout_3.addWidget(self.open_files_list_widget)

        self.waveform_left_side_splitter = QSplitter(self.layoutWidget)
        self.waveform_left_side_splitter.setObjectName(
            "waveform_left_side_splitter"
        )
        self.waveform_left_side_splitter.setOrientation(Qt.Vertical)
        self.station_view = StationTreeWidget(self.waveform_left_side_splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, "1")
        self.station_view.setHeaderItem(__qtreewidgetitem)
        self.station_view.setObjectName("station_view")
        self.station_view.setSortingEnabled(False)
        self.station_view.setAnimated(False)
        self.station_view.setHeaderHidden(True)
        self.waveform_left_side_splitter.addWidget(self.station_view)
        self.web_engine_view = QWebEngineView(self.waveform_left_side_splitter)
        self.web_engine_view.setObjectName("web_engine_view")
        self.web_engine_view.setProperty("url", QUrl("about:blank"))
        self.waveform_left_side_splitter.addWidget(self.web_engine_view)

        self.verticalLayout_3.addWidget(self.waveform_left_side_splitter)

        self.waveform_vertical_splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.waveform_vertical_splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.reset_view_push_button = QPushButton(self.layoutWidget1)
        self.reset_view_push_button.setObjectName("reset_view_push_button")
        self.reset_view_push_button.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.reset_view_push_button)

        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.detrend_and_demean_check_box = QCheckBox(self.layoutWidget1)
        self.detrend_and_demean_check_box.setObjectName(
            "detrend_and_demean_check_box"
        )

        self.horizontalLayout_2.addWidget(self.detrend_and_demean_check_box)

        self.normalize_check_box = QCheckBox(self.layoutWidget1)
        self.normalize_check_box.setObjectName("normalize_check_box")

        self.horizontalLayout_2.addWidget(self.normalize_check_box)

        self.horizontalSpacer_6 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.custom_processing_check_box = QCheckBox(self.layoutWidget1)
        self.custom_processing_check_box.setObjectName(
            "custom_processing_check_box"
        )

        self.horizontalLayout_2.addWidget(self.custom_processing_check_box)

        self.custom_processing_push_button = QPushButton(self.layoutWidget1)
        self.custom_processing_push_button.setObjectName(
            "custom_processing_push_button"
        )

        self.horizontalLayout_2.addWidget(self.custom_processing_push_button)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.references_push_button = QPushButton(self.layoutWidget1)
        self.references_push_button.setObjectName("references_push_button")

        self.horizontalLayout_2.addWidget(self.references_push_button)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.graph = GraphicsLayoutWidget(self.layoutWidget1)
        self.graph.setObjectName("graph")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.graph.sizePolicy().hasHeightForWidth()
        )
        self.graph.setSizePolicy(sizePolicy1)
        self.graph.setMouseTracking(False)

        self.verticalLayout_2.addWidget(self.graph)

        self.waveform_vertical_splitter.addWidget(self.layoutWidget1)

        self.horizontalLayout_13.addWidget(self.waveform_vertical_splitter)

        self.central_tab.addTab(self.waveform_tab, "")
        self.central_tab.setTabText(
            self.central_tab.indexOf(self.waveform_tab), "Waveforms"
        )
        self.auxiliary_data_tab = QWidget()
        self.auxiliary_data_tab.setObjectName("auxiliary_data_tab")
        self.horizontalLayout_11 = QHBoxLayout(self.auxiliary_data_tab)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.auxiliary_data_tree_view = QTreeWidget(self.auxiliary_data_tab)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, "1")
        self.auxiliary_data_tree_view.setHeaderItem(__qtreewidgetitem1)
        self.auxiliary_data_tree_view.setObjectName("auxiliary_data_tree_view")
        self.auxiliary_data_tree_view.header().setVisible(False)

        self.horizontalLayout_11.addWidget(self.auxiliary_data_tree_view)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.auxiliary_data_stacked_widget = QStackedWidget(
            self.auxiliary_data_tab
        )
        self.auxiliary_data_stacked_widget.setObjectName(
            "auxiliary_data_stacked_widget"
        )
        self.auxiliary_data_graph_page = QWidget()
        self.auxiliary_data_graph_page.setObjectName(
            "auxiliary_data_graph_page"
        )
        self.horizontalLayout_8 = QHBoxLayout(self.auxiliary_data_graph_page)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.auxiliary_data_graph = GraphicsLayoutWidget(
            self.auxiliary_data_graph_page
        )
        self.auxiliary_data_graph.setObjectName("auxiliary_data_graph")
        sizePolicy1.setHeightForWidth(
            self.auxiliary_data_graph.sizePolicy().hasHeightForWidth()
        )
        self.auxiliary_data_graph.setSizePolicy(sizePolicy1)
        self.auxiliary_data_graph.setMouseTracking(False)

        self.horizontalLayout_8.addWidget(self.auxiliary_data_graph)

        self.auxiliary_data_stacked_widget.addWidget(
            self.auxiliary_data_graph_page
        )
        self.auxiliary_data_file_page = QWidget()
        self.auxiliary_data_file_page.setObjectName("auxiliary_data_file_page")
        self.horizontalLayout_9 = QHBoxLayout(self.auxiliary_data_file_page)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.auxiliary_file_browser = QTextBrowser(
            self.auxiliary_data_file_page
        )
        self.auxiliary_file_browser.setObjectName("auxiliary_file_browser")
        font2 = QFont()
        font2.setFamily("Andale Mono")
        font2.setPointSize(12)
        self.auxiliary_file_browser.setFont(font2)

        self.horizontalLayout_9.addWidget(self.auxiliary_file_browser)

        self.auxiliary_data_stacked_widget.addWidget(
            self.auxiliary_data_file_page
        )

        self.verticalLayout_4.addWidget(self.auxiliary_data_stacked_widget)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.show_auxiliary_provenance_button = QPushButton(
            self.auxiliary_data_tab
        )
        self.show_auxiliary_provenance_button.setObjectName(
            "show_auxiliary_provenance_button"
        )
        self.show_auxiliary_provenance_button.setEnabled(False)
        self.show_auxiliary_provenance_button.setAutoDefault(False)
        self.show_auxiliary_provenance_button.setFlat(False)

        self.horizontalLayout_10.addWidget(
            self.show_auxiliary_provenance_button
        )

        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_10.addItem(self.horizontalSpacer_4)

        self.verticalLayout_4.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.groupBox = QGroupBox(self.auxiliary_data_tab)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.auxiliary_data_info_table_view = QTableWidget(self.groupBox)
        self.auxiliary_data_info_table_view.setObjectName(
            "auxiliary_data_info_table_view"
        )
        self.auxiliary_data_info_table_view.horizontalHeader().setProperty(
            "showSortIndicator", False
        )

        self.horizontalLayout_5.addWidget(self.auxiliary_data_info_table_view)

        self.horizontalLayout_7.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.auxiliary_data_tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.auxiliary_data_detail_table_view = QTableWidget(self.groupBox_2)
        self.auxiliary_data_detail_table_view.setObjectName(
            "auxiliary_data_detail_table_view"
        )

        self.horizontalLayout_6.addWidget(
            self.auxiliary_data_detail_table_view
        )

        self.horizontalLayout_7.addWidget(self.groupBox_2)

        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_11.addLayout(self.verticalLayout_4)

        self.horizontalLayout_11.setStretch(0, 3)
        self.horizontalLayout_11.setStretch(1, 10)
        self.central_tab.addTab(self.auxiliary_data_tab, "")
        self.provenance_tab = QWidget()
        self.provenance_tab.setObjectName("provenance_tab")
        self.horizontalLayout_4 = QHBoxLayout(self.provenance_tab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.provenance_list_view = QListView(self.provenance_tab)
        self.provenance_list_view.setObjectName("provenance_list_view")

        self.horizontalLayout_4.addWidget(self.provenance_list_view)

        self.provenance_graphics_view = SvgGraphicsView(self.provenance_tab)
        self.provenance_graphics_view.setObjectName("provenance_graphics_view")

        self.horizontalLayout_4.addWidget(self.provenance_graphics_view)

        self.horizontalLayout_4.setStretch(0, 3)
        self.horizontalLayout_4.setStretch(1, 10)
        self.central_tab.addTab(self.provenance_tab, "")
        self.event_tab = QWidget()
        self.event_tab.setObjectName("event_tab")
        self.horizontalLayout_12 = QHBoxLayout(self.event_tab)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.event_tree_widget = QTreeWidget(self.event_tab)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setText(0, "1")
        self.event_tree_widget.setHeaderItem(__qtreewidgetitem2)
        self.event_tree_widget.setObjectName("event_tree_widget")
        self.event_tree_widget.header().setVisible(False)

        self.horizontalLayout_12.addWidget(self.event_tree_widget)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.events_web_engine_view = QWebEngineView(self.event_tab)
        self.events_web_engine_view.setObjectName("events_web_engine_view")
        self.events_web_engine_view.setProperty("url", QUrl("about:blank"))

        self.verticalLayout_5.addWidget(self.events_web_engine_view)

        self.events_text_browser = QTextBrowser(self.event_tab)
        self.events_text_browser.setObjectName("events_text_browser")
        self.events_text_browser.setFont(font2)

        self.verticalLayout_5.addWidget(self.events_text_browser)

        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 1)

        self.horizontalLayout_12.addLayout(self.verticalLayout_5)

        self.horizontalLayout_12.setStretch(0, 4)
        self.horizontalLayout_12.setStretch(1, 6)
        self.central_tab.addTab(self.event_tab, "")

        self.verticalLayout.addWidget(self.central_tab)

        MainWindow.setCentralWidget(self.centralwidget)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)

        self.central_tab.setCurrentIndex(0)
        self.show_auxiliary_provenance_button.setDefault(False)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "ASDF Sextant", None)
        )
        self.select_file_button.setText(
            QCoreApplication.translate("MainWindow", "Open File", None)
        )
        self.label.setText(
            QCoreApplication.translate(
                "MainWindow",
                "Or just drag & drop an ASDF file into this window",
                None,
            )
        )
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", "Open Files", None)
        )
        self.close_file_button.setText(
            QCoreApplication.translate("MainWindow", "Close File", None)
        )
        self.reset_view_push_button.setText(
            QCoreApplication.translate("MainWindow", "Reset View", None)
        )
        self.detrend_and_demean_check_box.setText(
            QCoreApplication.translate(
                "MainWindow", "Detrend and Demean", None
            )
        )
        self.normalize_check_box.setText(
            QCoreApplication.translate("MainWindow", "Normalize", None)
        )
        self.custom_processing_check_box.setText("")
        self.custom_processing_push_button.setText(
            QCoreApplication.translate("MainWindow", "Custom Processing", None)
        )
        self.references_push_button.setText(
            QCoreApplication.translate("MainWindow", "References", None)
        )
        # if QT_CONFIG(tooltip)
        self.graph.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.auxiliary_data_graph.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.show_auxiliary_provenance_button.setText(
            QCoreApplication.translate("MainWindow", "Show Provenance", None)
        )
        self.groupBox.setTitle(
            QCoreApplication.translate("MainWindow", "Data Information", None)
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate("MainWindow", "Parameters", None)
        )
        self.central_tab.setTabText(
            self.central_tab.indexOf(self.auxiliary_data_tab),
            QCoreApplication.translate("MainWindow", "Auxiliary Data", None),
        )
        self.central_tab.setTabText(
            self.central_tab.indexOf(self.provenance_tab),
            QCoreApplication.translate("MainWindow", "Provenance", None),
        )
        self.central_tab.setTabText(
            self.central_tab.indexOf(self.event_tab),
            QCoreApplication.translate("MainWindow", "Events", None),
        )

    # retranslateUi
