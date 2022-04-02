# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RSV2.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_win(object):
    def setupUi(self, main_win):
        main_win.setObjectName("main_win")
        main_win.resize(1000, 600)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_win.sizePolicy().hasHeightForWidth())
        main_win.setSizePolicy(sizePolicy)
        main_win.setMinimumSize(QtCore.QSize(1000, 600))
        main_win.setMaximumSize(QtCore.QSize(1000, 600))
        main_win.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(main_win)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setGeometry(QtCore.QRect(270, 0, 391, 91))
        font = QtGui.QFont()
        font.setFamily("Orbitron")
        font.setPointSize(21)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Title.setFont(font)
        self.Title.setToolTip("")
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.log = QtWidgets.QTextBrowser(self.centralwidget)
        self.log.setGeometry(QtCore.QRect(50, 300, 901, 191))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log.sizePolicy().hasHeightForWidth())
        self.log.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.log.setFont(font)
        self.log.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.log.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.log.setObjectName("log")
        self.saving_progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.saving_progressBar.setEnabled(True)
        self.saving_progressBar.setGeometry(QtCore.QRect(50, 520, 931, 21))
        self.saving_progressBar.setProperty("value", 0)
        self.saving_progressBar.setTextVisible(True)
        self.saving_progressBar.setInvertedAppearance(False)
        self.saving_progressBar.setObjectName("saving_progressBar")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 80, 961, 211))
        self.layoutWidget.setObjectName("layoutWidget")
        self.button_grid = QtWidgets.QGridLayout(self.layoutWidget)
        self.button_grid.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.button_grid.setContentsMargins(0, 0, 0, 0)
        self.button_grid.setObjectName("button_grid")
        spacerItem = QtWidgets.QSpacerItem(
            375, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.button_grid.addItem(spacerItem, 3, 0, 1, 1)
        self.fetch_spinBox = QtWidgets.QSpinBox(self.layoutWidget)
        self.fetch_spinBox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.fetch_spinBox.setMinimum(1)
        self.fetch_spinBox.setMaximum(1000)
        self.fetch_spinBox.setObjectName("fetch_spinBox")
        self.button_grid.addWidget(self.fetch_spinBox, 6, 3, 1, 1)
        self.collectBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.collectBtn.setObjectName("collectBtn")
        self.button_grid.addWidget(self.collectBtn, 7, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.button_grid.addItem(spacerItem1, 5, 4, 1, 1)
        self.fetch_label = QtWidgets.QLabel(self.layoutWidget)
        self.fetch_label.setObjectName("fetch_label")
        self.button_grid.addWidget(self.fetch_label, 6, 2, 1, 1)
        self.redditor = QtWidgets.QTextEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.redditor.sizePolicy().hasHeightForWidth())
        self.redditor.setSizePolicy(sizePolicy)
        self.redditor.setMaximumSize(QtCore.QSize(350, 23))
        self.redditor.setAcceptDrops(True)
        self.redditor.setToolTip("")
        self.redditor.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.redditor.setStyleSheet("")
        self.redditor.setObjectName("redditor")
        self.button_grid.addWidget(self.redditor, 2, 4, 1, 1)
        self.redditor_label = QtWidgets.QLabel(self.layoutWidget)
        self.redditor_label.setObjectName("redditor_label")
        self.button_grid.addWidget(self.redditor_label, 2, 2, 1, 1)
        self.install_location_label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.install_location_label.sizePolicy().hasHeightForWidth())
        self.install_location_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setItalic(True)
        self.install_location_label.setFont(font)
        self.install_location_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.install_location_label.setIndent(-20)
        self.install_location_label.setObjectName("install_location_label")
        self.button_grid.addWidget(self.install_location_label, 1, 4, 1, 1)
        self.fetchMax_checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.fetchMax_checkBox.setChecked(False)
        self.fetchMax_checkBox.setTristate(False)
        self.fetchMax_checkBox.setObjectName("fetchMax_checkBox")
        self.button_grid.addWidget(self.fetchMax_checkBox, 6, 4, 1, 1)
        self.seachSubs_checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.seachSubs_checkBox.setObjectName("seachSubs_checkBox")
        self.button_grid.addWidget(self.seachSubs_checkBox, 4, 4, 1, 1)
        self.history_checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.history_checkBox.setTristate(False)
        self.history_checkBox.setObjectName("history_checkBox")
        self.button_grid.addWidget(self.history_checkBox, 3, 4, 1, 1)
        main_win.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_win)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        main_win.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_win)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        main_win.setStatusBar(self.statusbar)
        self.actionChange_Install_Location = QtWidgets.QAction(main_win)
        self.actionChange_Install_Location.setObjectName(
            "actionChange_Install_Location")
        self.actionDelete_User_Data = QtWidgets.QAction(main_win)
        self.actionDelete_User_Data.setObjectName("actionDelete_User_Data")
        self.actionOpen_User = QtWidgets.QAction(main_win)
        self.actionOpen_User.setObjectName("actionOpen_User")
        self.actionAdd_Taks_to_Windows_Scheduler = QtWidgets.QAction(main_win)
        self.actionAdd_Taks_to_Windows_Scheduler.setObjectName(
            "actionAdd_Taks_to_Windows_Scheduler")
        self.menuFile.addAction(self.actionChange_Install_Location)
        self.menuFile.addAction(self.actionAdd_Taks_to_Windows_Scheduler)
        self.menuEdit.addAction(self.actionDelete_User_Data)
        self.menuView.addAction(self.actionOpen_User)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(main_win)
        self.fetchMax_checkBox.toggled['bool'].connect(
            self.fetch_spinBox.setDisabled)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(main_win)

    def retranslateUi(self, main_win):
        _translate = QtCore.QCoreApplication.translate
        main_win.setWindowTitle(_translate("main_win", "RedditScraperV2"))
        self.Title.setText(_translate("main_win", "Reddit Scraper - V2"))
        self.fetch_spinBox.setToolTip(_translate(
            "main_win", "<html><head/><body><p>Limit of posts to fetch from user and subsequent subreddits</p></body></html>"))
        self.collectBtn.setText(_translate("main_win", "Collect!"))
        self.fetch_label.setText(_translate("main_win", "Fetch Limit:"))
        self.redditor_label.setText(_translate("main_win", "Redditor:"))
        self.install_location_label.setText(
            _translate("main_win", "InstallLocation"))
        self.fetchMax_checkBox.setToolTip(_translate(
            "main_win", "<html><head/><body><p>Enable the max amount of fetched items</p></body></html>"))
        self.fetchMax_checkBox.setText(_translate("main_win", "Max"))
        self.seachSubs_checkBox.setText(
            _translate("main_win", "Search Subreddits"))
        self.history_checkBox.setText(_translate("main_win", "Load History"))
        self.menuFile.setTitle(_translate("main_win", "File"))
        self.menuEdit.setTitle(_translate("main_win", "Edit"))
        self.menuView.setTitle(_translate("main_win", "View"))
        self.actionChange_Install_Location.setText(
            _translate("main_win", "Change Install Location"))
        self.actionDelete_User_Data.setText(
            _translate("main_win", "Delete User Data"))
        self.actionOpen_User.setText(_translate("main_win", "Open User Data"))
        self.actionAdd_Taks_to_Windows_Scheduler.setText(
            _translate("main_win", "Add Taks to Windows Scheduler"))
