#include "mixer/windowsmixer.h"
#include "mainwindow.h"
#include "trayicon.h"
#include "mynetwork.h"

#include <QApplication>
#include <QSystemTrayIcon>

int main(int argc, char *argv[])
{
    TrayIcon* t;
    QApplication a(argc, argv);

    WindowsMixer mixer;

    MyNetwork network;
    network.start();
    //QObject::connect(&network, SIGNAL(gotMute()), &mixer, SLOT(mute()));
    //QObject::connect(&network, SIGNAL(gotUnmute()), &mixer, SLOT(unmute()));
    QObject::connect(&network, &MyNetwork::gotMute, &mixer, &WindowsMixer::mute);
    QObject::connect(&network, &MyNetwork::gotUnmute, &mixer, &WindowsMixer::unmute);

    if (QSystemTrayIcon::isSystemTrayAvailable()) {
        t = new TrayIcon();
        t->show();
    } else {
        MainWindow w;
        w.show();
    }

    /*
     * mixer auswählen
     * mute/unmute testen
     * listen address: local network/localhost/global
     * port
     * anzeigen, ob ein client verbunden ist
     * deaktivieren/aktivieren
     *
     */

    return a.exec();
}
