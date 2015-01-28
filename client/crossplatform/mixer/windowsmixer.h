#ifndef WINDOWSMIXER_H
#define WINDOWSMIXER_H

#include "basicmixer.h"
#include <endpointvolume.h>

class Mixer : public BasicMixer
{
private:
    IAudioEndpointVolume *g_pEndptVol;
    GUID g_guidMyContext;

public:
    Mixer();
    ~Mixer();

public slots:
    bool mute();
    bool unmute();

};

#endif // WINDOWSMIXER_H
