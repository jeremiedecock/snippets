EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
EELAYER 27 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "22 jun 2015"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L ATMEGA168-P IC1
U 1 1 54594EEF
P 4400 3550
F 0 "IC1" H 3550 4850 40  0000 L BNN
F 1 "ATMEGA168-P" H 4750 2200 40  0000 L BNN
F 2 "DIL28" H 4400 3550 30  0000 C CIN
F 3 "" H 4400 3550 60  0000 C CNN
	1    4400 3550
	1    0    0    -1  
$EndComp
$Comp
L LED D1
U 1 1 54594F2C
P 5750 2900
F 0 "D1" H 5750 3000 50  0000 C CNN
F 1 "LED" H 5750 2800 50  0000 C CNN
F 2 "~" H 5750 2900 60  0000 C CNN
F 3 "~" H 5750 2900 60  0000 C CNN
	1    5750 2900
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 54594F3B
P 6100 3900
F 0 "R1" V 6180 3900 40  0000 C CNN
F 1 "1k" V 6107 3901 40  0000 C CNN
F 2 "~" V 6030 3900 30  0000 C CNN
F 3 "~" H 6100 3900 30  0000 C CNN
	1    6100 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 2900 6100 2900
Wire Wire Line
	6100 2900 6100 3650
NoConn ~ 5300 2400
NoConn ~ 5300 2500
NoConn ~ 5300 2600
NoConn ~ 5300 2700
NoConn ~ 5300 4700
NoConn ~ 5300 4600
NoConn ~ 5300 4500
NoConn ~ 5300 4400
NoConn ~ 5300 4300
NoConn ~ 5300 4100
NoConn ~ 5300 4000
NoConn ~ 5300 3850
NoConn ~ 5300 3750
NoConn ~ 5300 3650
NoConn ~ 5300 3550
NoConn ~ 5300 3450
NoConn ~ 5300 3350
NoConn ~ 5300 3250
NoConn ~ 5300 3100
NoConn ~ 5300 3000
NoConn ~ 5300 2800
Wire Wire Line
	3200 5050 6100 5050
Wire Wire Line
	6100 5050 6100 4150
Wire Wire Line
	3200 4600 3200 5200
Wire Wire Line
	3200 4600 3400 4600
NoConn ~ 3400 2700
NoConn ~ 3400 3000
$Comp
L GND #PWR2
U 1 1 545951D6
P 3300 4850
F 0 "#PWR2" H 3300 4850 30  0001 C CNN
F 1 "GND" H 3300 4780 30  0001 C CNN
F 2 "" H 3300 4850 60  0000 C CNN
F 3 "" H 3300 4850 60  0000 C CNN
	1    3300 4850
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR1
U 1 1 545951E5
P 3200 5200
F 0 "#PWR1" H 3200 5200 30  0001 C CNN
F 1 "GND" H 3200 5130 30  0001 C CNN
F 2 "" H 3200 5200 60  0000 C CNN
F 3 "" H 3200 5200 60  0000 C CNN
	1    3200 5200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3400 4700 3300 4700
Wire Wire Line
	3300 4700 3300 4850
Connection ~ 3200 5050
$Comp
L PWR_FLAG #FLG1
U 1 1 54595256
P 3400 2400
F 0 "#FLG1" H 3400 2495 30  0001 C CNN
F 1 "PWR_FLAG" H 3400 2580 30  0000 C CNN
F 2 "" H 3400 2400 60  0000 C CNN
F 3 "" H 3400 2400 60  0000 C CNN
	1    3400 2400
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG2
U 1 1 54595265
P 3400 4600
F 0 "#FLG2" H 3400 4695 30  0001 C CNN
F 1 "PWR_FLAG" H 3400 4780 30  0000 C CNN
F 2 "" H 3400 4600 60  0000 C CNN
F 3 "" H 3400 4600 60  0000 C CNN
	1    3400 4600
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 5459529E
P 3100 2400
F 0 "#PWR?" H 3100 2490 20  0001 C CNN
F 1 "+5V" H 3100 2490 30  0000 C CNN
F 2 "" H 3100 2400 60  0000 C CNN
F 3 "" H 3100 2400 60  0000 C CNN
	1    3100 2400
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 2400 3400 2400
Wire Wire Line
	5300 2900 5550 2900
$Comp
L SW_PUSH Button
U 1 1 55888875
P 5650 4500
F 0 "Button" H 5800 4610 50  0000 C CNN
F 1 "SW_PUSH" H 5650 4420 50  0000 C CNN
F 2 "~" H 5650 4500 60  0000 C CNN
F 3 "~" H 5650 4500 60  0000 C CNN
	1    5650 4500
	0    1    1    0   
$EndComp
Wire Wire Line
	5300 4200 5650 4200
Wire Wire Line
	5650 4800 5650 5050
Connection ~ 5650 5050
$EndSCHEMATC
