#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QCheckBox, QSystemTrayIcon, \
    QMenu, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, QThread, pyqtSlot

import muteme.icons_rc
import muteme.cli

class TcpServer(QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        muteme.cli.setup_mixer()

    #mute_event = QtCore.pyqtSignal(bool)

    @pyqtSlot()
    def serve(self):
        muteme.cli.run_tcp_server()


class TrayIcon(QSystemTrayIcon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setIcon(QIcon(":/icons/logo_256x256.png"))

        quit_action = QAction("Exit", self)
        #show_action = QAction("Show", self)
        #hide_action = QAction("Hide", self)
        quit_action.triggered.connect(self.on_quit)
        #show_action.triggered.connect(self.show)
        #hide_action.triggered.connect(self.hide)

        tray_menu = QMenu()
        tray_menu.addAction(quit_action)
        #tray_menu.addAction(show_action)
        #tray_menu.addAction(hide_action)
        self.setContextMenu(tray_menu)

        self.setup_tcp_server()

    def setup_tcp_server(self):
        self.tcp_server = TcpServer()
        self.network_thread = QThread(self)
        #self.tcp_server.mute_event.connect(self.on_mute_event)
        self.tcp_server.moveToThread(self.network_thread)
        self.network_thread.started.connect(self.tcp_server.serve)
        self.network_thread.start()

    @pyqtSlot(bool)
    def on_quit(self):
        self.network_thread.quit() # does not work
        qApp.quit()

    #@pyqtSlot(bool)
    #def on_mute_event(self, val):
        #self.mixer.mute(val)

def main():
    global app # see http://pyqt.sourceforge.net/Docs/PyQt5/gotchas.html
    app = QApplication(sys.argv)
    mw = TrayIcon()
    mw.show()

    return app.exec()


if __name__ == "__main__":
    import sys
    sys.exit(main())
