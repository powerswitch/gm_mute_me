#!/usr/bin/env python3

import threading

from PyQt5.QtCore import pyqtSlot, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QAction,
    qApp)

import muteme.icons_rc
from muteme.network import AsyncTcpServer
import muteme.mixer

app = None


class MuteEvent(QEvent):
    EVENT_TYPE = QEvent.Type(QEvent.registerEventType())

    def __init__(self, mute):
        super().__init__(self.EVENT_TYPE)
        self.mute = mute

class NetworkThread(threading.Thread):
    def __init__(self, mute_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tcp_server = AsyncTcpServer(mute_callback)

    def run(self):
        self.tcp_server.run_standalone()


class TrayIcon(QSystemTrayIcon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setIcon(QIcon(":/icons/logo_256x256.png"))

        quit_action = QAction("Exit", self)
        self.mute_action = QAction("Mute microphone", self)
        self.unmute_action = QAction("Unmute microphone", self)

        quit_action.triggered.connect(self.on_quit)
        self.mute_action.triggered.connect(self.on_mute)
        self.unmute_action.triggered.connect(self.on_unmute)
        self.unmute_action.setVisible(False)  #TODO: Actually determine mute state

        tray_menu = QMenu()
        tray_menu.addAction(self.mute_action)
        tray_menu.addAction(self.unmute_action)
        tray_menu.addAction(quit_action)
        self.setContextMenu(tray_menu)

        self.mixer = muteme.mixer.Mixer()
        self.setup_tcp_server()

    def setup_tcp_server(self):
        self.thread = NetworkThread(self.mute_callback)
        self.thread.start()

    def mute_callback(self, mute):
        QApplication.postEvent(self, MuteEvent(mute))

    def customEvent(self, event):
        if isinstance(event, MuteEvent):
            if event.mute:
                self.on_mute()
            else:
                self.un_unmute()

    @pyqtSlot(bool)
    def on_quit(self):
        self.thread.tcp_server.event_loop.call_soon_threadsafe(self.thread.tcp_server.event_loop.stop)
        self.thread.join()
        self.mixer.mute(False)
        qApp.quit()

    @pyqtSlot(bool)
    def on_mute(self):
        self.unmute_action.setVisible(True)
        self.mute_action.setVisible(False)
        self.mixer.mute(True)

    @pyqtSlot(bool)
    def on_unmute(self):
        self.unmute_action.setVisible(False)
        self.mute_action.setVisible(True)
        self.mixer.mute(False)



def main():
    global app # see http://pyqt.sourceforge.net/Docs/PyQt5/gotchas.html
    app = QApplication(sys.argv)
    mw = TrayIcon()
    mw.show()
    return app.exec()


if __name__ == "__main__":
    import sys
    sys.exit(main())
