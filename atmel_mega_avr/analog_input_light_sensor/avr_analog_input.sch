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
LIBS:photoresistor
EELAYER 27 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "23 jun 2015"
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
NoConn ~ 5300 2400
NoConn ~ 5300 2500
NoConn ~ 5300 2600
NoConn ~ 5300 2700
NoConn ~ 5300 4700
NoConn ~ 5300 4600
NoConn ~ 5300 4500
NoConn ~ 5300 4400
NoConn ~ 5300 4300
NoConn ~ 5300 4200
NoConn ~ 5300 3850
NoConn ~ 5300 3750
NoConn ~ 5300 3650
NoConn ~ 5300 3550
NoConn ~ 5300 3450
NoConn ~ 5300 3350
NoConn ~ 5300 3100
NoConn ~ 5300 3000
NoConn ~ 5300 2800
Wire Wire Line
	3200 4600 3200 5050
Wire Wire Line
	3200 5050 3200 5200
Wire Wire Line
	3200 4600 3400 4600
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
	3100 2400 3250 2400
Wire Wire Line
	3250 2400 3400 2400
$Comp
L DB9 RS232
U 1 1 55881DAB
P 6400 3950
F 0 "RS232" H 6400 4500 70  0000 C CNN
F 1 "DB9" H 6400 3400 70  0000 C CNN
F 2 "" H 6400 3950 60  0000 C CNN
F 3 "" H 6400 3950 60  0000 C CNN
	1    6400 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 3550 5800 3550
Wire Wire Line
	5800 3550 5800 3250
Wire Wire Line
	5800 3250 7000 3250
Wire Wire Line
	5950 3950 5450 3950
Wire Wire Line
	5450 3950 5450 4000
Wire Wire Line
	5450 4000 5300 4000
Wire Wire Line
	5450 4150 5950 4150
Wire Wire Line
	5450 4150 5450 4100
Wire Wire Line
	5450 4100 5300 4100
$Comp
L PHOTORESISTOR2 U1
U 1 1 55893F77
P 4550 2100
F 0 "U1" H 4500 2100 70  0000 C CNN
F 1 "PHOTORESISTOR" V 4950 2150 70  0000 C CNN
F 2 "~" H 4550 2100 60  0000 C CNN
F 3 "~" H 4550 2100 60  0000 C CNN
	1    4550 2100
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5300 3250 5500 3250
Wire Wire Line
	5500 3250 5500 1950
Wire Wire Line
	3250 1950 3250 2400
Wire Wire Line
	3250 2400 3250 2700
Wire Wire Line
	3250 1950 4100 1950
Connection ~ 3250 2400
Wire Wire Line
	4850 1950 5500 1950
Wire Wire Line
	5500 1950 6000 1950
Wire Wire Line
	3250 2700 3400 2700
$Comp
L R R1
U 1 1 55894D80
P 6250 1950
F 0 "R1" V 6330 1950 40  0000 C CNN
F 1 "10k" V 6257 1951 40  0000 C CNN
F 2 "~" V 6180 1950 30  0000 C CNN
F 3 "~" H 6250 1950 30  0000 C CNN
	1    6250 1950
	0    -1   -1   0   
$EndComp
Connection ~ 5500 1950
Wire Wire Line
	6500 1950 7000 1950
Wire Wire Line
	7000 1950 7000 5050
Wire Wire Line
	3200 5050 7000 5050
NoConn ~ 5300 2900
NoConn ~ 5950 3650
NoConn ~ 5950 3750
NoConn ~ 5950 3850
NoConn ~ 5950 4050
NoConn ~ 5950 4250
NoConn ~ 5950 4350
$EndSCHEMATC
