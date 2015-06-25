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
LIBS:raspberry
LIBS:blink_led-cache
EELAYER 27 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "25 jun 2015"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L LED D1
U 1 1 5444DB38
P 2600 2700
F 0 "D1" H 2600 2800 50  0000 C CNN
F 1 "LED" H 2600 2600 50  0000 C CNN
F 2 "~" H 2600 2700 60  0000 C CNN
F 3 "~" H 2600 2700 60  0000 C CNN
	1    2600 2700
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 5444DB4E
P 2650 3450
F 0 "R1" V 2730 3450 40  0000 C CNN
F 1 "1k" V 2657 3451 40  0000 C CNN
F 2 "~" V 2580 3450 30  0000 C CNN
F 3 "~" H 2650 3450 30  0000 C CNN
	1    2650 3450
	0    -1   -1   0   
$EndComp
$Comp
L RASPBERRY_IO RPi
U 1 1 5444DDA8
P 3650 3550
F 0 "RPi model B" H 3650 4250 60  0000 C CNN
F 1 "RASPBERRY_IO" V 3650 3550 50  0000 C CNN
F 2 "" H 3650 3550 60  0000 C CNN
F 3 "" H 3650 3550 60  0000 C CNN
	1    3650 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 3450 2900 3450
NoConn ~ 3250 3250
NoConn ~ 3250 3150
NoConn ~ 3250 3050
NoConn ~ 3250 2950
NoConn ~ 3250 3550
NoConn ~ 3250 3650
NoConn ~ 3250 3750
NoConn ~ 3250 3850
NoConn ~ 3250 3950
NoConn ~ 3250 4050
NoConn ~ 3250 4150
NoConn ~ 4050 4150
NoConn ~ 4050 4050
NoConn ~ 4050 3950
NoConn ~ 4050 3850
NoConn ~ 4050 3750
NoConn ~ 4050 3650
NoConn ~ 4050 3550
NoConn ~ 4050 3450
NoConn ~ 4050 3350
NoConn ~ 4050 3250
NoConn ~ 4050 3050
NoConn ~ 4050 2950
Wire Wire Line
	2800 2700 4300 2700
Wire Wire Line
	4300 2700 4300 3150
Wire Wire Line
	4300 3150 4050 3150
NoConn ~ 3250 3350
Wire Wire Line
	2400 3450 2250 3450
Wire Wire Line
	2250 3450 2250 2700
Wire Wire Line
	2250 2700 2400 2700
$EndSCHEMATC
