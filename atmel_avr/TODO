- AVR:
  - blink_led
  - digital input (push button)
  - AVR basics:
    sem1:
    - [ok] fuses
    - [ok] logical operators for bits manipulation in C
    - [  ] registers
    - [  ] digital output
    - [  ] digital input
    - [  ] pull-up/pull-down resistors
    - [  ] tester blinkled sur pololu 3pi
    sem2:
    - serial (UART) in/out
    - debug
    sem3:
    - interuptions
    - timers
    sem4:
    - analog output (PWM)
    - analog input
  - howto (remotely) debug with GDB ???
  - motors (DC, servomotors, stepmotors)
  - basic sensors (digital and analog: light, temperature, proximity, ...)
  - AVR ASM basics
  - Bus: I2C, SPI, UART
  - breackout sensors (I2C/UART sensors like GPS, ...)
  - basic LCD display
  - stockage de données sur une carte SD externe
  - xbee/zigbee
  - floating point numbers and maths functions (useful for neural networks, ...)
  - 3pi/assuro (télécommandé + ajouter des senseurs, caméras, ... et un contrôleur de haut niveau)
  - module RTC (real time clock)
- RPi:
  - blink_led
  - AVR basics: GPIO, ...
  - PWM, motors (DC, servomotors, stepmotors)
  - sensors...
  - Bus: I2C, SPI, UART, TTL (?), ...
  - basic LCD display
  - xbee/zigbee
  - module RTC (real time clock)
- communication AVR-RPi
- premier robot (3pi like):
  - tester le montage et le programme sur une breadboard
  - designer et fabriquer le PCB (gEDA ou autre EDA)
  - designer et fabriquer le support et la coque (OpenSCAD)
  - documentation:
    pourquoi une architecture bi-niveau (avr + rpi) ?
    Pourquoi le RPi ?
    (RPi = brain)
    1. ça permet d'utiliser des bibliothèques trop "lourdes" pour l'AVR (GSL,
       eigen, boost, opencv, numpy, GLPK, COIN-OR, ...)
    2. ça permet d'écrire des contrôleurs et d'utiliser des bibliothèques écrites
       dans d'autres langages que le C (ex de bbl.: boost, eigen, numpy, etc.).
       Les langages qui m'intéressent le plus sont le (vrai) C++ et Python.
    3. ça permet d'utiliser des senseurs trop "lourd" pour l'AVR (ex. caméra).
    4. les contrôleur "évolués" (adaptatifs, etc.) disposent de plus de
       puissance de calcul, plus de mémoire, plus d'espace de stockage,
       des flotants 64bits, etc.
    5. ça permet d'ajouter facilement des périphériques externes (USB,
       bluetooth, wifi, ethernet, son, caméra, ...)
    Pourquoi l'AVR ?
    (MCU = backbone)
    1. plus d'entrées sorties (on peut multiplier les IO en utilisant 
       plusieurs AVR.
    2. contrôle en "vrai temps réel" (PWM, ...)
    3. permet un contrôle "reflex" à haute fréquence et faible latence
       en attendant les ordres de haut niveau.

