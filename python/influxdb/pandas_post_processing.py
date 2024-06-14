#!/usr/bin/env python3

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

sns.set_context("paper")
# Get the list of all ".csv.xz" files in the current directory
file_list = [f for f in os.listdir('.') if f.endswith('.csv.xz')]

for filename in file_list:
    print(f"Processing {filename}")

    # Extract year and month from filename
    prefix = filename.split('_')[0]
    year = filename.split('_')[1].split('-')[0].split('.')[0]
    month = filename.split('_')[1].split('-')[1].split('.')[0]

    df = pd.read_csv(
        f'{prefix}_{year}-{month}.csv.xz',
        compression='xz',
        skiprows=3,
        header=0,
        usecols=[
            "_time",
            "_value",
            "_field",
            "_measurement",
            "device_id",
            #"device_type",
            #"unit",
            #"zone_name"
        ],
        #parse_dates=["_time"]
    )

    df = df.rename(columns={
            "_time": "time",
            "_value": "value",
            #"_field": "field",
            "_measurement": "measurement",
            "device_id": "device"
        })

    # Drop rows with _field != 'value'
    df = df.loc[df._field == 'value']
    df = df.drop(columns=["_field"])

    df['time'] = pd.to_datetime(df['time'], format=r'%Y-%m-%dT%H:%M:%S.%fZ')

    df["value"] = pd.to_numeric(df["value"], errors='coerce')

    df['measurement_device'] = df['measurement'] + '_' + df['device']

    for measurement in ('co2', 'humidity', 'is_open', 'light', 'motion', 'power', 'schneider_heating_setpoint', 'temperature'):
        df_measurement = df[df.measurement == measurement]
        df_measurement = df_measurement.pivot(index='time', columns='measurement_device', values='value')
        df_measurement = df_measurement.resample('30min').mean()

        # Save to a csv file
        df_measurement.to_csv(f"boulogne_{year}-{month}_{measurement}.csv.xz", index=True, compression='xz')

        try:
            # Save plot to a png file
            df_measurement.plot(title=f"{year}-{month} {measurement}", legend=False, figsize=(16, 8))
            #plt.savefig(f"boulogne_{year}-{month}_{measurement}.png")
            plt.savefig(f"boulogne_{year}-{month}_{measurement}.pdf")
            #plt.savefig(f"boulogne_{year}-{month}_{measurement}.svg")
            plt.close()
        except Exception as e:
            print(f"Error while plotting {year}-{month} {measurement}: {e}", file=sys.stderr)
