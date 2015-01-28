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
    basicmixer.cpp \
    mynetwork.cpp

HEADERS  += mainwindow.h \
    basicmixer.h \
    mynetwork.h

FORMS    += mainwindow.ui

RESOURCES += \
    icons.qrc

OTHER_FILES +=


win32 {
    SOURCES += mixer/windowsmixer.cpp
    HEADERS += mixer/windowsmixer.h
}

unix {
    SOURCES += mixer/defaultmixer.cpp
    HEADERS += mixer/defaultmixer.h
}
