#include "defaultmixer.h"

Mixer::Mixer()
{
}

bool Mixer::mute() {
  qDebug("mute()");
  return true;
}

bool Mixer::unmute() {
  qDebug("unmute()");
  return true;
}

Mixer::~Mixer() {
  mute();
}
