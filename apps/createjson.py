import pandas as pd
import json
import os


def createjson(Pump_Data, Pump_Info, filename):
    df_pump_data = Pump_Data
    df_pump_info = Pump_Info

    impeller_diameter = df_pump_info.iat[0, 1]
    impeller_diameter_unit = df_pump_info.iat[0, 2]
    revolutions = df_pump_info.iat[1, 1]
    name = df_pump_info.iat[2, 1]
    description = df_pump_info.iat[3, 1]

    # Capture the units from the first row, which contains the units for each variable
    units = df_pump_data.iloc[0]

    # Estrutura base para o arquivo JSON conforme o novo formato
    data_template = {
        "Name": name,
        "Description": description,
        "ImpellerDiameter": impeller_diameter,
        "ImpellerSpeed": revolutions,
        "ImpellerDiameterUnit": impeller_diameter_unit,
        "CurveHead": {"X": [], "Y": [], "Enabled": True, "Name": "HEAD", "ID": "", "CvType": 0, "yunit": units['Head'],
                      "xunit": units['Flow Rate']},
        "CurvePower": {"X": [], "Y": [], "Enabled": True, "Name": "POWER", "ID": "", "CvType": 1,
                       "yunit": units['Power'], "xunit": units['Flow Rate']},
        "CurveEfficiency": {"X": [], "Y": [], "Enabled": True, "Name": "EFF", "ID": "", "CvType": 3,
                            "yunit": units['Efficciency'], "xunit": units['Flow Rate']},
        "CurveNPSHr": {"X": [], "Y": [], "Enabled": True, "Name": "NPSH", "ID": "", "CvType": 2,
                       "yunit": units['Required NPSH'], "xunit": units['Flow Rate']}
    }

    # Populate the template with data from the Excel sheet, checking for null values
    for _, row in df_pump_data.iloc[1:].iterrows():
        flow_rate = row['Flow Rate']
        npsh = row['Required NPSH']
        head = row['Head']
        power = row['Power']
        efficiency = row['Efficciency']

        if pd.notnull(flow_rate):
            if pd.notnull(npsh):
                data_template["CurveNPSHr"]["X"].append(flow_rate)
                data_template["CurveNPSHr"]["Y"].append(npsh)
            if pd.notnull(head):
                data_template["CurveHead"]["X"].append(flow_rate)
                data_template["CurveHead"]["Y"].append(head)
            if pd.notnull(power):
                data_template["CurvePower"]["X"].append(flow_rate)
                data_template["CurvePower"]["Y"].append(power)
            if pd.notnull(efficiency):
                data_template["CurveEfficiency"]["X"].append(flow_rate)
                data_template["CurveEfficiency"]["Y"].append(efficiency)

    # Convert the populated template to JSON format
    json_data = json.dumps(data_template, indent=4)

    # Specify the output JSON file path
    file_dir = 'DWSIM Pump Curves/'
    partes = filename.rsplit('.', 1)
    nome_base = partes[0] if len(partes) > 1 else filename
    # Write the JSON data to a file
    with open(file_dir + nome_base + '.json', 'w') as json_file:
        json_file.write(json_data)

