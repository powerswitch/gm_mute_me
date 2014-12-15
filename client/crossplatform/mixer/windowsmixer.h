#ifndef WINDOWSMIXER_H
#define WINDOWSMIXER_H

#include "mixer.h"
#include <endpointvolume.h>

class WindowsMixer : public Mixer
{
private:
    IAudioEndpointVolume *g_pEndptVol;
    GUID g_guidMyContext;

public:
    WindowsMixer();
    ~WindowsMixer();

public slots:
    bool mute();
    bool unmute();

};

#endif // WINDOWSMIXER_H
