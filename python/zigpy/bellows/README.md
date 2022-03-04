Project page: https://github.com/zigpy/bellows

"Docs" to read:
- [ ] https://community.matrix.one/t/first-zigbee-tests-with-python-bellows-forming-a-network-controller/1579
- [ ] https://github.com/zigpy/bellows/issues/166
- [ ] https://github.com/zigpy/bellows/issues/40


```
apt install python3-pip

# Install bellows
pip install bellows

# "create" device database
mkdir -p ~/.config/bellows
touch ~/.config/bellows/app.db

# Export UART DEVICE
export EZSP_DEVICE=/dev/ttyUSB0

# run once: forming a zigbee network controller on the creator
bellows -b 115200 -d /dev/ttyUSB0 --flow-control software form

# Ctrl-C

# list known devices
bellows -b 115200 -d /dev/ttyUSB0 --flow-control software devices

		Device:
		  NWK: 0x0000
		  IEEE: 84:fd:27:ff:fe:82:38:d6
		  Endpoints:
			1: profile=0x104, device_type=DeviceType.undefined_0xbeef

# permit joining of network device
bellows -b 115200 -d /dev/ttyUSB0 --flow-control software permit

# Appairer le device...
# Attendre qu'il affiche "done"
# puis Ctrl-C

# list known devices
bellows -b 115200 -d /dev/ttyUSB0 --flow-control software devices

		Device:
		  NWK: 0x0000
		  IEEE: 84:fd:27:ff:fe:82:38:d6
		  Endpoints:
			1: profile=0x104, device_type=DeviceType.undefined_0xbeef
		Device:
		  NWK: 0x6a98
		  IEEE: 00:12:4b:00:25:1c:d2:1b
		  Endpoints:
			1: profile=0x104, device_type=DeviceType.TEMPERATURE_SENSOR
			  Input Clusters:
				Basic (0)
				Power Configuration (1)
				Identify (3)
				Temperature Measurement (1026)
				Relative Humidity Measurement (1029)
			  Output Clusters:
				Identify (3)


bellows -b 115200 -d /dev/ttyUSB0 --flow-control software devices
		Device:
		  NWK: 0x0000
		  IEEE: 84:fd:27:ff:fe:82:38:d6
		  Endpoints:
			1: profile=0x104, device_type=DeviceType.undefined_0xbeef
		Device:
		  NWK: 0x2af6
		  IEEE: 00:12:4b:00:25:13:10:cc
		  Endpoints:
			1: profile=0x104, device_type=DeviceType.IAS_ZONE
			  Input Clusters:
				Basic (0)
				Power Configuration (1)
				Identify (3)
				IAS Zone (1280)
			  Output Clusters:
				Identify (3)



# Ctrl-C


# bellows zcl NODE ENDPOINT_CLUSTER read-attribute --help

bellows -b 115200 -d /dev/ttyUSB0 --flow-control software zcl 00:12:4b:00:25:1c:d2:1b 1 3 commands
identify
identify_query
ezmode_invoke
update_commission_state
trigger_effect




# Dump
# ----

## Arguments
bellows -b 115200 -d /dev/ttyUSB0 --flow-control software dump --help
	Usage: bellows dump [OPTIONS]

	  Capture frames on CHANNEL and write to FILE in tcpdump format

	Options:
	  -c, --channel CHANNEL  [11<=x<=26; required]
	  -w FILE                [required]
	  --help                 Show this message and exit

## Get channel
bellows -b 115200 -d /dev/ttyUSB0 --flow-control software info
	[84:fd:27:ff:fe:82:38:d6]
	[0x0000]
	[<EmberNetworkStatus.JOINED_NETWORK: 2>]
	[<EmberStatus.SUCCESS: 0>, <EmberNodeType.COORDINATOR: 1>, EmberNetworkParameters(extendedPanId=98:25:19:6a:aa:da:de:32, panId=0x994d, radioTxPower=8, radioChannel=15, joinMethod=<EmberJoinMethod.USE_MAC_ASSOCIATION: 0>, nwkManagerId=0x0000, nwkUpdateId=0, channels=<Channels.ALL_CHANNELS: 134215680>)]
	[<EmberStatus.SUCCESS: 0>, EmberCurrentSecurityState(bitmask=<EmberCurrentSecurityBitmask.TRUST_CENTER_USES_HASHED_LINK_KEY|64|32|HAVE_TRUST_CENTER_LINK_KEY|GLOBAL_LINK_KEY: 244>, trustCenterLongAddress=84:fd:27:ff:fe:82:38:d6)]
	Manufacturer: Elelabs
	Board name: ELU013
	EmberZNet version: 6.10.0.0 build 169

## Dump
bellows -b 115200 -d /dev/ttyUSB0 --flow-control software dump -c 15 -w dump.dat

# Open the dump.dat file with wireshark


# Leave
# -----

## Leave
bellows -b 115200 -d /dev/ttyUSB0 --flow-control software zdo 00:12:4b:00:25:1c:d2:1b leave

## Check
bellows -b 115200 -d /dev/ttyUSB0 --flow-control software devices
...
```


Source code:
- ./env/bin/bellows
- ./env/lib/python3.8/site-packages/bellows/cli/main.py


My configuration:
- Dongle: [POPP ZB-Stick](https://www.domadoo.fr/fr/interface-domotique/5431-popp-dongle-usb-zigbee-zb-stick-chipset-efr32mg13-4251295701554.html) (chip EFR32MG13)
- Hardware: Raspberry Pi 4
- OS: RaspbianOS (2022-01-28-raspios-bullseye-arm64-lite)
- Python:
  - python 3.9.2
  - bellows 0.29.0

# Additional information

My dongle is well recognized in Home Assistant (haos rpi4-64 v7.4) and I can use my zigbee devices with it.
But now, I would like to control zigbee devices directly from Python scripts using zigpy/bellows.
As this dongle worked well in Home Assistant, I guess I don't have to flash its firmware to use it with zigpy/bellows. 
![bellows_question](https://user-images.githubusercontent.com/12746943/156762665-789886b2-82ba-4856-b4e7-bba43b20a92f.png)

I followed this procedure to install ZHA : https://koti.sk/wp-content/uploads/2021/01/POPP_ZB-Stick_with_HA.pdf (pages 6 and 7)
- Radio type: EZSP (Silicon Labs EmberZNet protocol)
- Serial: /dev/ttyUSB0 at 115200 bps
