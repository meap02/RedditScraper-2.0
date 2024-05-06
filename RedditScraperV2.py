from RSV2_UI import Ui_main_win
from PyQt5 import QtCore, QtWidgets
import sys
from collector import collectUsr, save, collectSub
import configparser
import os.path
import os
import tkinter
from tkinter import filedialog
import json


class sQThread(QtCore.QThread):
    def __init__(self, method):
        super(sQThread, self).__init__()
        self.method = method
        self.threadactive = True

    def run(self):
        self.method()

    def stop(self):
        self.threadactive = False
        self.wait()


class attatchedUI(Ui_main_win, QtCore.QObject):
    manager = []
    usr_list = []
    sub_list = []
    update = QtCore.pyqtSignal(str)
    save_update = QtCore.pyqtSignal(int, int)
    disable = QtCore.pyqtSignal(bool)

    blank_config = """[APP]
grab_limit =
load_history =
search_subreddits =
input_plainTextEdit =
[SETUP]
install_location = """
    blank_prawini = """[DEFAULT]
client_id=
client_secret=
user_agent=
check_for_updates = False
comment_kind = t1
message_kind = t4
redditor_kind = t2
submission_kind = t3
subreddit_kind = t5
trophy_kind = t6
oauth_url = https://oauth.reddit.com
reddit_url = https://www.reddit.com
short_url =  https://redd.it
ratelimit_seconds = 5
timeout = 16"""

    def __init__(self, window):
        print("Setting up attatched UI...")
        QtCore.QObject.__init__(self)
        self.setupUi(window)
        if os.path.isfile("settings.ini"):
            self.config = None
            with open("settings.ini", "r") as f:
                self.config = configparser.ConfigParser()
                self.config.read_file(f)
            self.install_location_label.setText(
                self.config["SETUP"]["install_location"]
            )
            self.input_plainTextEdit.setPlainText(self.config["APP"]["input"])
            self.history_checkBox.setChecked(
                eval(self.config["APP"]["load_history"])
            )
            self.seachSubs_checkBox.setChecked(
                eval(self.config["APP"]["search_subreddits"])
            )
            self.fetch_spinBox.setValue(int(self.config["APP"]["grab_limit"]))
            self.content_comboBox.setCurrentIndex(
                int(self.config["APP"]["content_index"])
            )
            if self.config["APP"]["content_index"] == "1":
                self.seachSubs_checkBox.hide()
                self.fetchtype_comboBox.show()
            else:
                self.seachSubs_checkBox.show()
                self.fetchtype_comboBox.hide()
        else:
            self.install_location_label.setText(os.getcwd())
        if not os.path.isfile("praw.ini"):
            try:
                with open("praw.ini", "x") as f:
                    f.write(self.blank_prawini)
            except:
                pass
            ###############
        for name in os.listdir(
            self.config["SETUP"]["install_location"] + "\\Redditors"
        ):
            self.usr_list.append(name)
        for name in os.listdir(
            self.config["SETUP"]["install_location"] + "\\Subreddits"
        ):
            self.sub_list.append(name)
        if self.content_comboBox.currentIndex() == 1:  # When Subreddit
            self.input_comboBox.addItems(self.sub_list)
        else:  # When Redditor
            self.input_comboBox.addItems(self.usr_list)

        ############# EVENT CONNECTIONS ############################
        app.aboutToQuit.connect(self.closeEvent)
        self.save_update.connect(self.set_progressbar)
        self.update.connect(self.update_out)
        self.disable.connect(self.disable_ui)
        self.content_comboBox.currentIndexChanged["int"].connect(
            self.content_change
        )
        self.collectBtn.clicked.connect(self.safe_collect)
        self.actionChange_Reddit_Token_Credentials.triggered.connect(
            self.cred_subwindow
        )
        self.actionChange_Install_Location.triggered.connect(
            self.change_install
        )
        self.actionAdd_Taks_to_Windows_Scheduler.triggered.connect(
            self.auto_subwindow
        )
        main_win.show()

    def content_change(self, item):
        if item == 1:  # When Subreddit is chosen
            self.seachSubs_checkBox.hide()
            self.fetchtype_comboBox.show()
            self.input_comboBox.clear()
            self.input_comboBox.addItems(self.sub_list)
        else:  # When Redditor is chosen
            self.seachSubs_checkBox.show()
            self.fetchtype_comboBox.hide()
            self.input_comboBox.clear()
            self.input_comboBox.addItems(self.usr_list)

    def safe_collect(self):
        self.disable.emit(True)
        thread = sQThread(self.collect)
        self.manager.append(thread)
        thread.start()

    def collect(self):
        self.save_update.emit(0, 0)
        collection = []
        if self.input_tabWidget.currentIndex() == 1:
            input = self.input_comboBox.currentText()
        else:
            input = str(self.input_plainTextEdit.toPlainText())

        if self.content_comboBox.currentIndex() == 1:
            for y in collectSub(
                input,
                (
                    1000
                    if self.fetchMax_checkBox.isChecked()
                    else self.fetch_spinBox.value()
                ),
                self.history_checkBox.isChecked(),
                self.fetchtype_comboBox.currentIndex(),
                self.install_location_label.text(),
                collection,
            ):
                self.update.emit(y)
                content = "Subreddits"
        else:
            for y in collectUsr(
                input,
                (
                    1000
                    if self.fetchMax_checkBox.isChecked()
                    else self.fetch_spinBox.value()
                ),
                self.history_checkBox.isChecked(),
                self.seachSubs_checkBox.isChecked(),
                self.install_location_label.text(),
                collection,
            ):
                self.update.emit(y)
                content = "Redditors"

        max = len(collection)
        self.save_update.emit(0, max)
        for i, post in zip(range(0, max), collection):
            for y in save(
                post, input, self.install_location_label.text(), content
            ):
                self.update.emit(y)
            self.save_update.emit(i, max)
        self.save_update.emit(0, 1)
        self.update.emit("Done!")
        self.disable.emit(False)
        print("Done!")

    def set_progressbar(self, value, max):
        if value > max:
            self.saving_progressBar.reset()
            return
        if self.saving_progressBar.maximum() != max:
            self.saving_progressBar.setRange(0, max)
        self.saving_progressBar.setValue(value)

    def change_install(self):
        Droot = tkinter.Tk()
        Droot.withdraw()
        new = filedialog.askdirectory()
        self.install_location_label.setText(new)
        self.config.set("SETUP", "install_location", new)
        with open("settings.ini", "w") as f:
            self.config.write(f)

    def update_out(self, out):
        self.log.append(out)

    def disable_ui(self, boolean):
        self.collectBtn.setDisabled(boolean)
        self.input_plainTextEdit.setDisabled(boolean)
        self.fetch_spinBox.setDisabled(boolean)
        self.fetchMax_checkBox.setDisabled(boolean)
        self.history_checkBox.setDisabled(boolean)
        self.seachSubs_checkBox.setDisabled(boolean)
        self.input_tabWidget.setDisabled(boolean)
        self.content_comboBox.setDisabled(boolean)
        self.fetch_label.setDisabled(boolean)
        # self.button_grid.setEnabled(boolean)

    ####SUBWINOWS####################

    def cred_subwindow(self):
        with open("praw.ini", "r") as f:
            prawini = configparser.ConfigParser()
            prawini.read_file(f)
        self.cred_sw = subwindow()
        self.cred_sw.createWindow(374, 254)
        self.cred_sw.setObjectName("cred_sw")
        self.cred_sw.setMinimumSize(QtCore.QSize(374, 205))
        self.cred_sw.setMaximumSize(QtCore.QSize(500, 500))
        self.create_pushButton = QtWidgets.QPushButton(self.cred_sw)
        self.create_pushButton.setGeometry(QtCore.QRect(150, 210, 75, 23))
        self.create_pushButton.setFlat(False)
        self.create_pushButton.setObjectName("create_pushButton")
        self.widget = QtWidgets.QWidget(self.cred_sw)
        self.widget.setGeometry(QtCore.QRect(30, 10, 311, 179))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.useragent_label = QtWidgets.QLabel(self.widget)
        self.useragent_label.setObjectName("useragent_label")
        self.gridLayout.addWidget(self.useragent_label, 2, 0, 1, 1)
        self.useragent_plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.useragent_plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 23))
        self.useragent_plainTextEdit.setObjectName("useragent_plainTextEdit")
        self.useragent_plainTextEdit.setPlainText(
            prawini["DEFAULT"]["user_agent"]
        )
        self.gridLayout.addWidget(self.useragent_plainTextEdit, 2, 1, 1, 1)
        self.clientid_plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.clientid_plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 23))
        self.clientid_plainTextEdit.setObjectName("clientid_plainTextEdit")
        self.clientid_plainTextEdit.setPlainText(
            prawini["DEFAULT"]["client_id"]
        )
        self.gridLayout.addWidget(self.clientid_plainTextEdit, 0, 1, 1, 1)
        self.clientsecret_plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.clientsecret_plainTextEdit.setMaximumSize(
            QtCore.QSize(16777215, 23)
        )
        self.clientsecret_plainTextEdit.setObjectName(
            "clientsecret_plainTextEdit"
        )
        self.clientsecret_plainTextEdit.setPlainText(
            prawini["DEFAULT"]["client_secret"]
        )
        self.gridLayout.addWidget(self.clientsecret_plainTextEdit, 1, 1, 1, 1)
        self.clientsecret_label = QtWidgets.QLabel(self.widget)
        self.clientsecret_label.setObjectName("clientsecret_label")
        self.gridLayout.addWidget(self.clientsecret_label, 1, 0, 1, 1)
        self.clientid_label = QtWidgets.QLabel(self.widget)
        self.clientid_label.setObjectName("clientid_label")
        self.gridLayout.addWidget(self.clientid_label, 0, 0, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.cred_sw.setWindowTitle(
            _translate("cred_sw", "Reddit App Credentials")
        )
        self.create_pushButton.setText(_translate("cred_sw", "Create"))
        self.useragent_label.setText(_translate("cred_sw", "User Agent:"))
        self.clientsecret_label.setText(
            _translate("cred_sw", "Client Secret:")
        )
        self.clientid_label.setText(_translate("cred_sw", "Client ID:"))
        self.create_pushButton.clicked.connect(self.create_prawini)
        QtCore.QMetaObject.connectSlotsByName(self.cred_sw)
        ### Add information from existing praw.ini if availible ######
        self.cred_sw.show()

    def auto_subwindow(self):
        self.auto_sw = subwindow()
        self.auto_sw.createWindow(266, 182)
        self.auto_sw.setObjectName("self.auto_sw")
        self.auto_sw.setMinimumSize(QtCore.QSize(266, 182))
        self.auto_sw.setMaximumSize(QtCore.QSize(266, 182))
        self.target_comboBox = QtWidgets.QComboBox(self.auto_sw)
        self.target_comboBox.setGeometry(QtCore.QRect(20, 20, 231, 22))
        self.target_comboBox.setObjectName("target_comboBox")
        self.target_comboBox.addItem("")
        self.target_comboBox.addItem("")
        self.freqency_tabWidget = QtWidgets.QTabWidget(self.auto_sw)
        self.freqency_tabWidget.setGeometry(QtCore.QRect(20, 50, 231, 91))
        self.freqency_tabWidget.setObjectName("freqency_tabWidget")
        self.hourly_tab = QtWidgets.QWidget()
        self.hourly_tab.setObjectName("hourly_tab")
        self.hourly_spinBox = QtWidgets.QSpinBox(self.hourly_tab)
        self.hourly_spinBox.setGeometry(QtCore.QRect(110, 20, 42, 22))
        self.hourly_spinBox.setMaximum(59)
        self.hourly_spinBox.setObjectName("hourly_spinBox")
        self.hourly_label = QtWidgets.QLabel(self.hourly_tab)
        self.hourly_label.setGeometry(QtCore.QRect(10, 20, 101, 20))
        self.hourly_label.setObjectName("hourly_label")
        self.freqency_tabWidget.addTab(self.hourly_tab, "")
        self.daily_tab = QtWidgets.QWidget()
        self.daily_tab.setObjectName("daily_tab")
        self.daily_timeEdit = QtWidgets.QTimeEdit(self.daily_tab)
        self.daily_timeEdit.setGeometry(QtCore.QRect(100, 20, 111, 22))
        self.daily_timeEdit.setObjectName("daily_timeEdit")
        self.daily_label = QtWidgets.QLabel(self.daily_tab)
        self.daily_label.setGeometry(QtCore.QRect(10, 20, 91, 16))
        self.daily_label.setObjectName("daily_label")
        self.freqency_tabWidget.addTab(self.daily_tab, "")
        self.weekly_tab = QtWidgets.QWidget()
        self.weekly_tab.setObjectName("weekly_tab")
        self.weekly_comboBox = QtWidgets.QComboBox(self.weekly_tab)
        self.weekly_comboBox.setGeometry(QtCore.QRect(100, 10, 69, 22))
        self.weekly_comboBox.setObjectName("weekly_comboBox")
        self.weekly_comboBox.addItem("")
        self.weekly_comboBox.addItem("")
        self.weekly_comboBox.addItem("")
        self.weekly_comboBox.addItem("")
        self.weekly_comboBox.addItem("")
        self.weekly_comboBox.addItem("")
        self.weekly_comboBox.addItem("")
        self.weekly_day_label = QtWidgets.QLabel(self.weekly_tab)
        self.weekly_day_label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.weekly_day_label.setObjectName("weekly_day_label")
        self.weekly_timeEdit = QtWidgets.QTimeEdit(self.weekly_tab)
        self.weekly_timeEdit.setGeometry(QtCore.QRect(100, 40, 111, 22))
        self.weekly_timeEdit.setObjectName("weekly_timeEdit")
        self.weekly_time_label = QtWidgets.QLabel(self.weekly_tab)
        self.weekly_time_label.setGeometry(QtCore.QRect(10, 40, 91, 16))
        self.weekly_time_label.setObjectName("weekly_time_label")
        self.freqency_tabWidget.addTab(self.weekly_tab, "")
        self.monthly_tab = QtWidgets.QWidget()
        self.monthly_tab.setObjectName("monthly_tab")
        self.monthly_day_label = QtWidgets.QLabel(self.monthly_tab)
        self.monthly_day_label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.monthly_day_label.setObjectName("monthly_day_label")
        self.monthly_spinBox = QtWidgets.QSpinBox(self.monthly_tab)
        self.monthly_spinBox.setGeometry(QtCore.QRect(110, 10, 42, 22))
        self.monthly_spinBox.setMinimum(1)
        self.monthly_spinBox.setMaximum(29)
        self.monthly_spinBox.setObjectName("monthly_spinBox")
        self.monthly_timeEdit = QtWidgets.QTimeEdit(self.monthly_tab)
        self.monthly_timeEdit.setGeometry(QtCore.QRect(110, 40, 101, 22))
        self.monthly_timeEdit.setObjectName("monthly_timeEdit")
        self.monthly_time_label = QtWidgets.QLabel(self.monthly_tab)
        self.monthly_time_label.setGeometry(QtCore.QRect(10, 40, 91, 16))
        self.monthly_time_label.setObjectName("monthly_time_label")
        self.freqency_tabWidget.addTab(self.monthly_tab, "")
        self.createauto_pushButton = QtWidgets.QPushButton(self.auto_sw)
        self.createauto_pushButton.setGeometry(QtCore.QRect(180, 150, 75, 23))
        self.createauto_pushButton.setObjectName("createauto_pushButton")
        _translate = QtCore.QCoreApplication.translate
        self.auto_sw.setWindowTitle(
            _translate("self.auto_sw", "Auto-Collector Setup")
        )
        self.target_comboBox.setItemText(
            0, _translate("self.auto_sw", "user1")
        )
        self.target_comboBox.setItemText(
            1, _translate("self.auto_sw", "user2")
        )
        self.hourly_label.setText(
            _translate("self.auto_sw", "Minute on the hour:")
        )
        self.freqency_tabWidget.setTabText(
            self.freqency_tabWidget.indexOf(self.hourly_tab),
            _translate("self.auto_sw", "Hourly"),
        )
        self.daily_label.setText(
            _translate("self.auto_sw", "Time on the day:")
        )
        self.freqency_tabWidget.setTabText(
            self.freqency_tabWidget.indexOf(self.daily_tab),
            _translate("self.auto_sw", "Daily"),
        )
        self.weekly_comboBox.setItemText(
            0, _translate("self.auto_sw", "Sunday")
        )
        self.weekly_comboBox.setItemText(
            1, _translate("self.auto_sw", "Monday")
        )
        self.weekly_comboBox.setItemText(
            2, _translate("self.auto_sw", "Tuesday")
        )
        self.weekly_comboBox.setItemText(
            3, _translate("self.auto_sw", "Wednesday")
        )
        self.weekly_comboBox.setItemText(
            4, _translate("self.auto_sw", "Thursday")
        )
        self.weekly_comboBox.setItemText(
            5, _translate("self.auto_sw", "Friday")
        )
        self.weekly_comboBox.setItemText(
            6, _translate("self.auto_sw", "Saturday")
        )
        self.weekly_day_label.setText(
            _translate("self.auto_sw", "Day of the week:")
        )
        self.weekly_time_label.setText(
            _translate("self.auto_sw", "Time on the day:")
        )
        self.freqency_tabWidget.setTabText(
            self.freqency_tabWidget.indexOf(self.weekly_tab),
            _translate("self.auto_sw", "Weekly"),
        )
        self.monthly_day_label.setText(
            _translate("self.auto_sw", "Day of the month:")
        )
        self.monthly_time_label.setText(
            _translate("self.auto_sw", "Time on the day:")
        )
        self.freqency_tabWidget.setTabText(
            self.freqency_tabWidget.indexOf(self.monthly_tab),
            _translate("self.auto_sw", "Monthly"),
        )
        self.createauto_pushButton.setText(
            _translate("self.auto_sw", "Create")
        )
        self.freqency_tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(self.auto_sw)
        ## YOU ARE HERE CREATE TASK SCEDULAER INTEGRATION
        self.auto_sw.show()

    def create_prawini(self):
        try:
            with open(
                self.install_location_label.text() + "\\praw.ini", "x"
            ) as f:
                f.write(self.blank_prawini)
        except OSError:
            print("praw.ini already exists!")
            pass
        with open("praw.ini", "r") as f:
            prawini = configparser.ConfigParser()
            prawini.read_file(f)
            prawini.set(
                "DEFAULT",
                "client_id",
                self.clientid_plainTextEdit.toPlainText(),
            )
            prawini.set(
                "DEFAULT",
                "client_secret",
                self.clientsecret_plainTextEdit.toPlainText(),
            )
            prawini.set(
                "DEFAULT",
                "user_agent",
                self.useragent_plainTextEdit.toPlainText(),
            )
        with open("praw.ini", "w") as f:
            prawini.write(f)
        self.cred_sw.close()

    def closeEvent(self):
        try:
            with open(
                self.install_location_label.text() + "\\settings.ini", "x"
            ) as f:
                f.write(self.blank_config)
            with open("settings.ini", "r") as f:
                self.config = configparser.ConfigParser()
                self.config.read_file(f)
        except OSError:
            pass
        self.config.set("APP", "grab_limit", str(self.fetch_spinBox.value()))
        self.config.set(
            "APP", "load_history", str(self.history_checkBox.isChecked())
        )
        self.config.set(
            "APP",
            "search_subreddits",
            str(self.seachSubs_checkBox.isChecked()),
        )
        self.config.set("APP", "input", input)
        self.config.set(
            "APP", "content_index", str(self.content_comboBox.currentIndex())
        )
        self.config.set(
            "SETUP", "install_location", self.install_location_label.text()
        )
        with open("settings.ini", "w") as f:
            self.config.write(f)
        with open("list.json", "w") as f:
            json.dump([self.usr_list, self.sub_list], f)
        for thread in self.manager:
            thread.stop()
        print("Close button pressed")

    #    sys.exit(0)


class subwindow(QtWidgets.QWidget):
    def createWindow(self, WindowWidth, WindowHeight):
        parent = None
        super(subwindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(WindowWidth, WindowHeight)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_win = QtWidgets.QMainWindow()
    ui = attatchedUI(main_win)
    sys.exit(app.exec_())
