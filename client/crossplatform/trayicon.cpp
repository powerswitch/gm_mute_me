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
    QIcon* icon = new QIcon("/home/flyser/Gmodlogo_5r.svg");
    return *icon;
}

TrayIcon::~TrayIcon()
{
}
