#include "trayicon.h"

#include <QMenu>
#include <QIcon>

TrayIcon::TrayIcon(QObject *parent) :
    QSystemTrayIcon(getIcon(), parent)
{

    QMenu* menu = new QMenu();
    menu->addAction("Test");
    setContextMenu(menu);
}

QIcon &TrayIcon::getIcon() {
    //QIcon* icon = new QIcon("/usr/share/icons/hicolor/256x256/apps/cournal.png");
#ifdef WIN32
    QIcon* icon = new QIcon("logo_16x16.png");
#else
    QIcon* icon = new QIcon("logo.svg");
#endif
    return *icon;
}

TrayIcon::~TrayIcon()
{
}
