#ifdef Q_OS_WIN32
#include "mixer/windowsmixer.h"
#else
#include "mixer/defaultmixer.h"
#endif

#include "mainwindow.h"
#include "mynetwork.h"

#include <QApplication>
#include <QSystemTrayIcon>
#include <QMenu>
#include <QAction>

int main(int argc, char *argv[])
{
    QSystemTrayIcon* t;

    QApplication a(argc, argv);

    Mixer mixer;

    MyNetwork network;
    network.start();
    //QObject::connect(&network, SIGNAL(gotMute()), &mixer, SLOT(mute()));
    //QObject::connect(&network, SIGNAL(gotUnmute()), &mixer, SLOT(unmute()));
    QObject::connect(&network, &MyNetwork::gotMute, &mixer, &Mixer::mute);
    QObject::connect(&network, &MyNetwork::gotUnmute, &mixer, &Mixer::unmute);

    if (QSystemTrayIcon::isSystemTrayAvailable())
    {
#ifdef Q_OS_WIN32
        QIcon icon = QIcon(":/icons/logo_16x16.png");
#else
        QIcon icon = QIcon(":/icons/logo.svg");
#endif
        t = new QSystemTrayIcon(icon);
        QMenu* menu = new QMenu();
        QAction *action = new QAction(QString("Quit"), menu);
        QObject::connect(menu, &QMenu::triggered, &a, &QApplication::quit);
        //TODO es wird fuer jedes element in dem Menue der quit Slot ausgefuehrt!
        menu->addAction(action);
        t->setContextMenu(menu);
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
