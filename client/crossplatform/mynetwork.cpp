#include "mynetwork.h"

#include <QtNetwork>
#include <iostream>

#define LISTEN QHostAddress::LocalHost
#define PORT 8264

MyNetwork::MyNetwork(QObject *parent) :
    QObject(parent)
{
    tcpServer = new QTcpServer();
    connect(tcpServer, SIGNAL(newConnection()),
            this, SLOT(acceptConnection()));
}

void MyNetwork::start() {
    while (!tcpServer->isListening() && !tcpServer->listen(LISTEN, PORT)) {
        std::cout << "Failed to listen" << std::endl;
        /*QMessageBox::StandardButton ret = QMessageBox::critical(this,
                                        tr("Loopback"),
                                        tr("Unable to start the test: %1.")
                                        .arg(tcpServer.errorString()),
                                        QMessageBox::Retry
                                        | QMessageBox::Cancel);
        if (ret == QMessageBox::Cancel)
            return;*/
        return;
    }

}

void MyNetwork::acceptConnection()
{
    std::cout << "Got connection" << std::endl;
    tcpServerConnection = tcpServer->nextPendingConnection();
    connect(tcpServerConnection, SIGNAL(readyRead()),
            this, SLOT(readFromClient()));
    //connect(tcpServerConnection, SIGNAL(error(QAbstractSocket::SocketError)),
    //        this, SLOT(displayError(QAbstractSocket::SocketError)));
    tcpServer->close();
}

void MyNetwork::readFromClient() {
    QByteArray data = tcpServerConnection->readLine(1024);
    std::cout << "Data: '" << data.data() << "'" << std::endl;
    if (data.isEmpty())
        return;

    if (data.contains("SPEAK")) {
        emit gotUnmute();
        std::cout << "Unmute" << std::endl;
    }
    else if (data.contains("MUTE")) {
        emit gotMute();
        std::cout << "Mute" << std::endl;
    }
    else {
        std::cout << "Invalid Data" << std::endl;
    }
}
