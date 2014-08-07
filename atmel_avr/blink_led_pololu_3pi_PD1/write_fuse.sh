#!/bin/sh

#avrdude -p ?
#avrdude -c ?

LFUSE="$1"  # 0xHH
HFUSE="$2"  # 0xHH
EFUSE="$3"  # 0xHH

#AVRDUDE_MCU_ID=t85
#AVRDUDE_MCU_ID=m328
AVRDUDE_MCU_ID=m328p
#AVRDUDE_MCU_ID=

#AVRDUDE_PROGRAMMER_ID=avrisp
#AVRDUDE_PROGRAMMER_ID=avrispv2
#AVRDUDE_PROGRAMMER_ID=usbtiny
AVRDUDE_PROGRAMMER_ID=usbasp

OPTION=

echo -n "Write \"${LFUSE}:${HFUSE}:${EFUSE}\" (y/n) ? "
read ANSWER

if [ ${ANSWER} = "y" ]
then
    if [ ${AVRDUDE_PROGRAMMER_ID} = avrispv2 ]
    then
        echo "Pololu ISP programmer"
        echo "avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lfuse:w:${LFUSE}:m  -U hfuse:w:${HFUSE}:m  -U efuse:w:${EFUSE}:m"
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lfuse:w:${LFUSE}:m  -U hfuse:w:${HFUSE}:m  -U efuse:w:${EFUSE}:m
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lfuse:r:-:h -U hfuse:r:-:h -U efuse:r:-:h
    else
        echo "USBasp or USBTiny"
        echo "avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lfuse:w:${LFUSE}:m  -U hfuse:w:${HFUSE}:m  -U efuse:w:${EFUSE}:m"
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lfuse:w:${LFUSE}:m  -U hfuse:w:${HFUSE}:m  -U efuse:w:${EFUSE}:m
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lfuse:r:-:h -U hfuse:r:-:h -U efuse:r:-:h
    fi
fi

