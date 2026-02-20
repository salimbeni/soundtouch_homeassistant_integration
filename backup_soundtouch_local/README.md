# Bose SoundTouch Local Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

This integration provides local control for Bose SoundTouch speakers in Home Assistant. It is designed to work even after Bose shuts down its cloud services in May 2026.

## Features

- **Local Network Support**: No cloud connection required for basic operations.
- **Media Player Control**: Play, Pause, Stop, Previous/Next track.
- **Volume Management**: Precise volume control and Muting.
- **Power Control**: Turn on/off directly from Home Assistant.
- **Presets**: Automatically fetches and allows selection of your SoundTouch presets.
- **Discovery**: Automatic discovery of devices on your network via Zeroconf.

## Installation via HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed.
2. In Home Assistant, go to **HACS > Integrations**.
3. Click the three dots in the top right corner and select **Custom repositories**.
4. Paste the URL of this repository: `https://github.com/salimbeni/soundtouch_homeassistant_integration`
5. Select **Integration** as the category and click **Add**.
6. Find **Bose SoundTouch Local** in HACS and click **Download**.
7. Restart Home Assistant.

## Configuration

1. Go to **Settings > Devices & Services**.
2. Click **Add Integration** and search for **Bose SoundTouch Local**.
3. If discovered, click **Configure**. Otherwise, enter the IP address of your SoundTouch device.

## Credits

This integration uses the [bosesoundtouchapi](https://github.com/thlucas1/bosesoundtouchapi) library.
