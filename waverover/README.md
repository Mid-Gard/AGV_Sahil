# Waveshare Wave Rover - Raspberry Pi Integration

## Overview

This repository provides scripts and instructions for integrating the Waveshare Wave Rover with a Raspberry Pi using UART communication. The provided scripts include basic commands such as forward, reverse, 360 turn, etc.

## Hardware Setup

1. Connect the EaveshaRE Wave Rover to the Raspberry Pi using UART communication:
   - Connect Wave Rover TX to Raspberry Pi RX.
   - Connect Wave Rover RX to Raspberry Pi TX.
   - Connect VCC and GND appropriately.

## Files

### 1. `forward.py`

This script commands the Wave Rover to move forward.

```bash
python3 forward.py
```

### 2. `reverse.py`

This script commands the Wave Rover to move reverse.

```bash
python3 reverse.py
```

### 3. `360.py`

This script commands the Wave Rover to move 360.

```bash
python3 360.py
```

# Usage

- Connect the EaveshaRE Wave Rover to the Raspberry Pi as described in the hardware setup.
- Ensure the UART communication is configured properly.
- Run the desired script according to the movement you want:
  - For forward motion: python3 forward.py
  - For reverse motion: python3 reverse.py
  - For a 360-degree turn: python3 turn_360.py

# Important Notes

- Make sure the UART communication is properly configured.
- Ensure the correct GPIO pins are used for UART communication (TX to RX, RX to TX).
- Check the power supply to the Wave Rover to avoid issues with motor control.
- Stop the script execution using Ctrl+C when you want to halt the movement.

# Troubleshooting

- If you encounter issues:

  - Double-check the hardware connections.
  - Verify the UART settings on the Raspberry Pi.
  - Ensure the Wave Rover is powered and responsive.

# Contributors

Sahil Shaikh
