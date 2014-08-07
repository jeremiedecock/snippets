#!/bin/sh

#avrdude -p ?
#avrdude -c ?

#AVRDUDE_MCU_ID=t85
AVRDUDE_MCU_ID=m328p
#AVRDUDE_MCU_ID=

#AVRDUDE_PROGRAMMER_ID=avrisp
#AVRDUDE_PROGRAMMER_ID=avrispv2
#AVRDUDE_PROGRAMMER_ID=usbtiny
AVRDUDE_PROGRAMMER_ID=usbasp

# WARNING: for m328, use m328p avrdude ID and edit signature in /etc/avrdude.conf 

PROGRAM=no
DEBUG=yes

OPTION=

#if [ ${AVRDUDE_MCU_ID} = "m328" ]
#then
#	echo "ATMega328"
#	AVRDUDE_MCU_ID=m328p
#	OPTION="${OPTION} -F "
#fi

# -e = erase flash before

if [ ${AVRDUDE_PROGRAMMER_ID} = avrispv2 ]
then
    echo "Pololu ISP programmer"

    # PROGRAM ###############

    if [ ${PROGRAM} = "yes" ]
    then
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -e -U flash:w:blink_led.hex
    fi

    # DEBUG #################
    
    if [ ${DEBUG} = "yes" ]
    then
        # DUMP FLASH
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U flash:r:dump_flash.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U flash:r:dump_flash.motorola:s
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U flash:r:dump_flash.raw:r
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U flash:r:dump_flash.hex:h
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U flash:r:dump_flash.oct:o
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U flash:r:dump_flash.bin:b

        # DUMP EEPROM
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U eeprom:r:dump_eeprom.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U eeprom:r:dump_eeprom.motorola:s
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U eeprom:r:dump_eeprom.raw:r
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U eeprom:r:dump_eeprom.hex:h
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U eeprom:r:dump_eeprom.oct:o
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U eeprom:r:dump_eeprom.bin:b

        # DUMP FUSES
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lfuse:r:dump_lfuse.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U hfuse:r:dump_hfuse.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U efuse:r:dump_efuse.ihex:i

        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lfuse:r:-:r -U hfuse:r:-:r -U efuse:r:-:r > dump_fuses_lhe.raw
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lfuse:r:-:h -U hfuse:r:-:h -U efuse:r:-:h > dump_fuses_lhe.hex
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lfuse:r:-:b -U hfuse:r:-:b -U efuse:r:-:b > dump_fuses_lhe.bin

        # DUMP LOCK
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lock:r:dump_lock.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lock:r:dump_lock.raw:r 
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lock:r:dump_lock.hex:h 
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U lock:r:dump_lock.bin:b 

        # DUMP SIGNATURE
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U signature:r:dump_signature.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U signature:r:dump_signature.raw:r 
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U signature:r:dump_signature.hex:h 
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -P /dev/ttyACM1 -U signature:r:dump_signature.bin:b 
    fi

else
    echo "USBasp or USBTiny"

    # PROGRAM ###############

    if [ ${PROGRAM} = "yes" ]
    then
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -e -U flash:w:blink_led.hex
    fi

    # DEBUG #################

    if [ ${DEBUG} = "yes" ]
    then
        # DUMP FLASH
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U flash:r:dump_flash.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U flash:r:dump_flash.motorola:s
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U flash:r:dump_flash.raw:r
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U flash:r:dump_flash.hex:h
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U flash:r:dump_flash.oct:o
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U flash:r:dump_flash.bin:b

        # DUMP EEPROM
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U eeprom:r:dump_eeprom.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U eeprom:r:dump_eeprom.motorola:s
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U eeprom:r:dump_eeprom.raw:r
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U eeprom:r:dump_eeprom.hex:h
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U eeprom:r:dump_eeprom.oct:o
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U eeprom:r:dump_eeprom.bin:b

        # DUMP FUSES
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lfuse:r:dump_lfuse.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U hfuse:r:dump_hfuse.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U efuse:r:dump_efuse.ihex:i

        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lfuse:r:-:r -U hfuse:r:-:r -U efuse:r:-:r > dump_fuses_lhe.raw
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lfuse:r:-:h -U hfuse:r:-:h -U efuse:r:-:h > dump_fuses_lhe.hex
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lfuse:r:-:b -U hfuse:r:-:b -U efuse:r:-:b > dump_fuses_lhe.bin

        # DUMP LOCK
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lock:r:dump_lock.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lock:r:dump_lock.raw:r 
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lock:r:dump_lock.hex:h 
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U lock:r:dump_lock.bin:b 

        # DUMP SIGNATURE
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U signature:r:dump_signature.ihex:i
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U signature:r:dump_signature.raw:r 
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U signature:r:dump_signature.hex:h 
        avrdude -c ${AVRDUDE_PROGRAMMER_ID} -p ${AVRDUDE_MCU_ID} ${OPTION} -U signature:r:dump_signature.bin:b 
    fi
fi

