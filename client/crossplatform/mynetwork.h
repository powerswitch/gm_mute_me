#ifndef MYNETWORK_H
#define MYNETWORK_H

#include <QObject>
//#include <QtNetwork>
#include <QTcpServer>
#include <QTcpSocket>

class MyNetwork : public QObject
{
    Q_OBJECT
public:
    explicit MyNetwork(QObject *parent = 0);
    void start();

signals:
    void gotMute();
    void gotUnmute();

private:
    QTcpServer *tcpServer;
    QTcpSocket *tcpServerConnection;

private slots:
    void acceptConnection();
    void readFromClient();
    void clientDisconnect();
};

#endif // MYNETWORK_H
