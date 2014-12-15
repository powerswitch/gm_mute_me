#ifndef TRAYICON_H
#define TRAYICON_H

#include <QSystemTrayIcon>

class TrayIcon : public QSystemTrayIcon
{
    Q_OBJECT
public:
    explicit TrayIcon(QObject *parent = 0);
    ~TrayIcon();

signals:

public slots:

private:
    QIcon& getIcon();

};

#endif // TRAYICON_H
