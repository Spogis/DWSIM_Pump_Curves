import pandas as pd
import json
import os


def createjson(dataframe, filename):
    df_pump_data = dataframe

    # Capture the units from the first row, which contains the units for each variable
    units = df_pump_data.iloc[0]

    # Define a template for JSON structure
    data_template = {
        "NPSH": {
            "Enabled": True,
            "Name": "NPSH",
            "ID": "2707b32d-cc35-483d-a167-8eafb289d17c",
            "CvType": 2,
            "yunit": units['Required NPSH'],
            "xunit": units['Flow Rate'],
            "y": [],
            "x": []
        },
        "HEAD": {
            "Enabled": True,
            "Name": "HEAD",
            "ID": "d68f2dc3-c36c-4a8f-a1be-ff1b9396df9a",
            "CvType": 0,
            "yunit": units['Head'],
            "xunit": units['Flow Rate'],
            "y": [],
            "x": []
        },
        "EFF": {
            "Enabled": True,
            "Name": "EFF",
            "ID": "81ab7901-d048-4bd1-a2b9-3ebf317e6ed6",
            "CvType": 3,
            "yunit": units['Efficciency'],
            "xunit": units['Flow Rate'],
            "y": [],
            "x": []
        },
        "POWER": {
            "Enabled": True,
            "Name": "POWER",
            "ID": "bc43f67d-85f0-49b4-b37f-4698b33373e8",
            "CvType": 1,
            "yunit": units['Power'],
            "xunit": units['Flow Rate'],
            "y": [],
            "x": []
        },
        "SYSTEM": {
            "Enabled": False,
            "Name": "SYSTEM",
            "ID": "8ef1595f-6ba8-441b-8117-98018965957b",
            "CvType": 4,
            "yunit": "",
            "xunit": "",
            "y": [],
            "x": []
        }
    }

    # Populate the template with data from the Excel sheet, checking for null values
    for _, row in df_pump_data.iloc[1:].iterrows():
        flow_rate = row['Flow Rate']

        if pd.notnull(row['Required NPSH']):
            data_template["NPSH"]["x"].append(flow_rate)
            data_template["NPSH"]["y"].append(row['Required NPSH'])

        if pd.notnull(row['Head']):
            data_template["HEAD"]["x"].append(flow_rate)
            data_template["HEAD"]["y"].append(row['Head'])

        if pd.notnull(row['Efficciency']):
            data_template["EFF"]["x"].append(flow_rate)
            data_template["EFF"]["y"].append(row['Efficciency'])

        if pd.notnull(row['Power']):
            data_template["POWER"]["x"].append(flow_rate)
            data_template["POWER"]["y"].append(row['Power'])

    # Convert the populated template to JSON format
    json_data = json.dumps(data_template, indent=4)

    # Specify the output JSON file path
    file_dir = 'DWSIM Pump Curves/'
    partes = filename.rsplit('.', 1)
    nome_base = partes[0] if len(partes) > 1 else filename
    # Write the JSON data to a file
    with open(file_dir + nome_base + '.json', 'w') as json_file:
        json_file.write(json_data)

