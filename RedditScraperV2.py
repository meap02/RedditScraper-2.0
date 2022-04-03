from RSV2_UI import Ui_main_win
from PyQt5 import QtCore, QtWidgets
import sys
from collector import collectUser, save
import configparser
import os.path
import os
import tkinter
from tkinter import filedialog


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
    update = QtCore.pyqtSignal(str)
    save_update = QtCore.pyqtSignal(int, int)
    disable = QtCore.pyqtSignal(bool)

    blank_config = """[APP]
grab_limit =
load_history =
search_subreddits =
redditor =
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
        if(os.path.isfile("settings.ini")):
            self.config = None
            with open("settings.ini", 'r') as f:
                self.config = configparser.ConfigParser()
                self.config.read_file(f)
            self.install_location_label.setText(
                self.config["SETUP"]["install_location"])
            self.redditor.setText(self.config["APP"]["redditor"])
            self.history_checkBox.setChecked(
                eval(self.config["APP"]["load_history"]))
            self.seachSubs_checkBox.setChecked(
                eval(self.config["APP"]["search_subreddits"]))
            self.fetch_spinBox.setValue(int(self.config["APP"]["grab_limit"]))
        else:
            self.install_location_label.setText(os.getcwd())
        if not os.path.isfile("praw.ini"):
            try:
                with open("praw.ini", 'x') as f:
                    f.write(self.blank_prawini)
            except:
                pass
        ############# EVENT CONNECTIONS ############################
        app.aboutToQuit.connect(self.closeEvent)
        self.save_update.connect(self.set_progressbar)
        self.update.connect(self.update_out)
        self.disable.connect(self.disable_ui)
        self.collectBtn.clicked.connect(self.safe_collect)
        self.actionChange_Reddit_Token_Credentials.triggered.connect(
            self.cred_subwindow)
        self.actionChange_Install_Location.triggered.connect(
            self.change_install)
        main_win.show()

    def safe_collect(self):
        self.disable.emit(True)
        thread = sQThread(self.collect)
        self.manager.append(thread)
        thread.start()

    def collect(self):
        self.save_update.emit(0, 0)
        collection = []
        for y in collectUser(self.redditor.toPlainText(),
                             1000 if self.fetchMax_checkBox.isChecked() else
                             self.fetch_spinBox.value(),
                             self.history_checkBox.isChecked(),
                             self.seachSubs_checkBox.isChecked(),
                             self.install_location_label.text(),
                             collection):
            self.update.emit(y)

        print("Saving has begun at "
              + self.install_location_label.text()
              + "/Redditors/" + self.redditor.toPlainText() + "/")
        max = len(collection)
        self.save_update.emit(0, max)
        for i, post in zip(range(0, max), collection):
            for y in save(post,
                          self.redditor.toPlainText(),
                          self.install_location_label.text()):
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
        if(self.saving_progressBar.maximum() != max):
            self.saving_progressBar.setRange(0, max)
        self.saving_progressBar.setValue(value)

    def change_install(self):
        Droot = tkinter.Tk()
        Droot.withdraw()
        new = filedialog.askdirectory()
        self.install_location_label.setText(new)
        self.config.set("SETUP", "install_location", new)
        with open('settings.ini', 'w') as f:
            self.config.write(f)

    def update_out(self, out):
        self.log.append(out)

    def disable_ui(self, boolean):
        self.collectBtn.setDisabled(boolean)
        self.redditor.setDisabled(boolean)
        self.fetch_spinBox.setDisabled(boolean)
        self.fetchMax_checkBox.setDisabled(boolean)
        self.history_checkBox.setDisabled(boolean)
        self.seachSubs_checkBox.setDisabled(boolean)

    def cred_subwindow(self):
        with open("praw.ini", 'r') as f:
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
            prawini["DEFAULT"]["user_agent"])
        self.gridLayout.addWidget(self.useragent_plainTextEdit, 2, 1, 1, 1)
        self.clientid_plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.clientid_plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 23))
        self.clientid_plainTextEdit.setObjectName("clientid_plainTextEdit")
        self.clientid_plainTextEdit.setPlainText(
            prawini["DEFAULT"]["client_id"])
        self.gridLayout.addWidget(self.clientid_plainTextEdit, 0, 1, 1, 1)
        self.clientsecret_plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.clientsecret_plainTextEdit.setMaximumSize(
            QtCore.QSize(16777215, 23))
        self.clientsecret_plainTextEdit.setObjectName(
            "clientsecret_plainTextEdit")
        self.clientsecret_plainTextEdit.setPlainText(
            prawini["DEFAULT"]["client_secret"])
        self.gridLayout.addWidget(self.clientsecret_plainTextEdit, 1, 1, 1, 1)
        self.clientsecret_label = QtWidgets.QLabel(self.widget)
        self.clientsecret_label.setObjectName("clientsecret_label")
        self.gridLayout.addWidget(self.clientsecret_label, 1, 0, 1, 1)
        self.clientid_label = QtWidgets.QLabel(self.widget)
        self.clientid_label.setObjectName("clientid_label")
        self.gridLayout.addWidget(self.clientid_label, 0, 0, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.cred_sw.setWindowTitle(_translate(
            "cred_sw", "Reddit App Credentials"))
        self.create_pushButton.setText(_translate("cred_sw", "Create"))
        self.useragent_label.setText(_translate("cred_sw", "User Agent:"))
        self.clientsecret_label.setText(
            _translate("cred_sw", "Client Secret:"))
        self.clientid_label.setText(_translate("cred_sw", "Client ID:"))
        self.create_pushButton.clicked.connect(self.create_prawini)
        QtCore.QMetaObject.connectSlotsByName(self.cred_sw)
        ### Add information from existing praw.ini if availible ######
        self.cred_sw.show()

    def create_prawini(self):
        try:
            with open(self.install_location_label.text()
                      + "\\praw.ini", "x") as f:
                f.write(self.blank_prawini)
        except OSError:
            print("praw.ini already exists!")
            pass
        with open("praw.ini", 'r') as f:
            prawini = configparser.ConfigParser()
            prawini.read_file(f)
            prawini.set("DEFAULT", "client_id",
                        self.clientid_plainTextEdit.toPlainText())
            prawini.set("DEFAULT", "client_secret",
                        self.clientsecret_plainTextEdit.toPlainText())
            prawini.set("DEFAULT", "user_agent",
                        self.useragent_plainTextEdit.toPlainText())
        with open('praw.ini', 'w') as f:
            prawini.write(f)
        self.cred_sw.close()

    def closeEvent(self):
        try:
            with open(self.install_location_label.text()
                      + "\\settings.ini", "x") as f:
                f.write(self.blank_config)
            with open("settings.ini", 'r') as f:
                self.config = configparser.ConfigParser()
                self.config.read_file(f)
        except OSError:
            pass
        self.config.set("APP", "grab_limit", str(self.fetch_spinBox.value()))
        self.config.set("APP", "load_history",
                        str(self.history_checkBox.isChecked()))
        self.config.set("APP", "search_subreddits",
                        str(self.seachSubs_checkBox.isChecked()))
        self.config.set("APP", "redditor",
                        self.redditor.toPlainText())
        self.config.set("SETUP", "install_location",
                        self.install_location_label.text())
        with open('settings.ini', 'w') as f:
            self.config.write(f)
        for thread in self.manager:
            thread.stop()
        print('Close button pressed')
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
