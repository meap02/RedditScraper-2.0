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
        ############# EVENT CONNECTIONS ############################
        app.aboutToQuit.connect(self.closeEvent)
        self.save_update.connect(self.set_progressbar)
        self.update.connect(self.update_out)
        self.disable.connect(self.disable_ui)
        self.collectBtn.clicked.connect(self.safe_collect)
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_win = QtWidgets.QMainWindow()
    ui = attatchedUI(main_win)
    sys.exit(app.exec_())
