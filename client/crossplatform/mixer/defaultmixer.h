#ifndef DEFAULTMIXER_H
#define DEFAULTMIXER_H

#include "basicmixer.h"

class Mixer : public BasicMixer
{
private:
    //IAudioEndpointVolume *g_pEndptVol;
    //GUID g_guidMyContext;

public:
    Mixer();
    ~Mixer();

public slots:
    bool mute();
    bool unmute();

};

#endif // DEFAULTMIXER_H
