#-------------------------------------------------
#
# Project created by QtCreator 2014-12-13T20:42:51
#
#-------------------------------------------------

QT       += core gui network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = MuteMe
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    trayicon.cpp \
    mixer.cpp \
    mixer/windowsmixer.cpp \
    mynetwork.cpp

HEADERS  += mainwindow.h \
    trayicon.h \
    mixer.h \
    mixer/windowsmixer.h \
    mynetwork.h

FORMS    += mainwindow.ui

RESOURCES += \
    icons.qrc

OTHER_FILES +=
