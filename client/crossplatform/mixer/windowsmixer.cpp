#include "windowsmixer.h"

#include <mmdeviceapi.h>
#include <endpointvolume.h>

WindowsMixer::WindowsMixer()
{
    HRESULT hr;
    IMMDeviceEnumerator *pEnumerator;
    IMMDevice *pDevice;
    g_guidMyContext = GUID_NULL;

#warning second parameter might be wrong
    hr = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
    if (FAILED(hr)) {
        MessageBox(NULL, TEXT("Failed to initialize COM library."), TEXT("CoInititalizeEx"), MB_OK & MB_ICONERROR);
        goto exit;
    }

    // Create Guid
    hr = CoCreateGuid(&g_guidMyContext);
    if (FAILED(hr)) {
        MessageBox(NULL, TEXT("Failed to create GUID."), TEXT("CoCreateGuid"), MB_OK & MB_ICONERROR);
        goto exit_coinitialized;
    }

    // Create Instance of MMDeviceEnumerator
    hr = CoCreateInstance(__uuidof(MMDeviceEnumerator),
        NULL, CLSCTX_INPROC_SERVER,
        __uuidof(IMMDeviceEnumerator),
        (void**)&pEnumerator);
    if (FAILED(hr)) {
        MessageBox(NULL, TEXT("Failed to instance of MMDeviceEnumerator."), TEXT("CoCreateInstance"), MB_OK & MB_ICONERROR);
        goto exit_penum_release;
    }

    // get the default capture device
    hr = pEnumerator->GetDefaultAudioEndpoint(eCapture, eConsole, &pDevice);
    if (FAILED(hr)) {
        MessageBox(NULL, TEXT("Failed to get default capture device."), TEXT("GetDefaultAudioEndpoint"), MB_OK & MB_ICONERROR);
        goto exit_pdevice_release;
    }

    // access audio endpoint volume
    hr = pDevice->Activate(__uuidof(IAudioEndpointVolume), CLSCTX_ALL, NULL, (void**)&g_pEndptVol);
    if (FAILED(hr)) {
        MessageBox(NULL, TEXT("Can't access audio endpoint volume."), TEXT("Activate"), MB_OK & MB_ICONERROR);
        goto exit_endptvol_release;
    }

    return;

    exit_endptvol_release:
        if (g_pEndptVol != NULL) {
            g_pEndptVol->Release();
            g_pEndptVol = NULL;
        }
    exit_pdevice_release:
        if (pDevice != NULL) {
            pDevice->Release();
            pDevice = NULL;
        }
    exit_penum_release:
        if (pEnumerator != NULL) {
            pEnumerator->Release();
            pEnumerator = NULL;
        }
    exit_coinitialized: /* after CoInitializeEx */
        CoUninitialize();
    exit:
        throw 0;
}

bool WindowsMixer::mute() {
    HRESULT hr = g_pEndptVol->SetMute(TRUE, &g_guidMyContext);
    if (FAILED(hr)) {
        MessageBox(NULL, TEXT("Could not unmute microphone."), TEXT("SetMute"), MB_OK & MB_ICONERROR);
        return false;
    }
    return true;
}

bool WindowsMixer::unmute() {
    HRESULT hr = g_pEndptVol->SetMute(FALSE, &g_guidMyContext);
    if (FAILED(hr)) {
        MessageBox(NULL, TEXT("Could not unmute microphone."), TEXT("SetMute"), MB_OK & MB_ICONERROR);
        return false;
    }
    return true;
}

WindowsMixer::~WindowsMixer() {
    mute();
}
