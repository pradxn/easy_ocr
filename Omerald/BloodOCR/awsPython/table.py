import json

test = {
    "table_7c5e398b4c894e66aab4b7e02f697521": [
        [
            "Lab Code",
            ":CPC-AP-113"
        ],
        [
            "Sample Drawn Date",
            ":2022-04-26 09:22"
        ],
        [
            "Registration Date",
            "2022-04-26 09:23"
        ],
        [
            "Approved Date",
            ":2022-04-26 09:56"
        ]
    ],
    "table_65b8b4440c4c4dcd8ccdc7440912e7bb": [
        [
            "Sample ID",
            ":1524952 NaF Fasting"
        ],
        [
            "Patient ID",
            ":641523"
        ],
        [
            "Ref. Doctor :",
            " "
        ],
        [
            "Ref. Customer :",
            " "
        ]
    ],
    "table_38887c7a36b0430e8b9cd820ae99d6aa": [
        [
            "CLINICAL",
            "BIOCHEMISTRY",
            " ",
            " "
        ],
        [
            "Test Description",
            "Result",
            "Units",
            "Biological Reference Ranges"
        ],
        [
            "Glucose-Fasting (FBS) (Method Spectrophotometry)",
            "198",
            "mg/dL",
            "70 100 Normal 100 126 Pre Diabetic > 126 Diabetic"
        ]
    ]
}

'''def print_table(data):
            for key, values in data.items():
                print("\n")
                for value in values:
                    row = "|".join([str(x).ljust(20) for x in value])
                    print(row)
'''

def print_table(data):
    for key, values in data.items():
        headers = []
        for value in values:
            if "Test Description" in value:
                headers = value
                break
        if not headers: # ignore tables without headers
            continue
        print("|".join([str(x).ljust(20) for x in headers[0:3]]))
        print("-"*80)
        for value in values:
            if "Test Description" not in value:
                print("|".join([str(x).ljust(20) for x in value[0:3]]))

output_table = print_table(test)

def output1(params):
    return params

output1(output_table)


print(type(test))

print("-------------------------------------------------------------------------------------------")
'''
data = json.loads(test)

row_to_extract = input("Enter the row to extract: ")

for table in data.values():
    for row in table:
        if row_to_extract.lower() in row[0].lower():
            test_description = row[0]
            result = row[1]
            units = row[2]
            reference_ranges = row[3]
            break

# Print the extracted data
print(f"Test Description: {test_description}")
print(f"Result: {result}")
print(f"Units: {units}")
print(f"Reference Ranges: {reference_ranges}")
'''

{'table_d6f308bdab4449279574c05618fb5f2c': 
 [['Lab Code', ':CPC-AP-113'], 
  ['Sample Drawn Date', ':2022-04-26 09:22'], 
  ['Registration Date', '2022-04-26 09:23'], 
  ['Approved Date', ':2022-04-26 09:56']], 
  
  'table_6455aa6bcf1e4cd9abfa67e000b289a7': 
  [['Sample ID', ':1524952 NaF Fasting'], 
   ['Patient ID', ':641523'], 
   ['Ref. Doctor :', ' '], 
   ['Ref. Customer :', ' ']], 
   
   'table_382eb1d728ff470a91aeb6a375b4ddc9': 
   [['CLINICAL', 'BIOCHEMISTRY', ' ', ' '], 
    ['Test Description', 'Result', 'Units', 'Biological Reference Ranges'], 
    ['Glucose-Fasting (FBS) (Method Spectrophotometry)', '198', 'mg/dL', '70 100 Normal 100 126 Pre Diabetic > 126 Diabetic']]}

[[['CLINICAL', 'BIOCHEMISTRY', ' ', ' '], 
  ['Test Description', 'Result', 'Units', 'Biological Reference Ranges'], 
  ['Glucose-Fasting (FBS) (Method Spectrophotometry)', '198', 'mg/dL', '70 100 Normal 100 126 Pre Diabetic > 126 Diabetic']]]

{
    ['CLINICAL', 'BIOCHEMISTRY', ' ', ' '],
    ['Test Description', ['Glucose-Fasting (FBS) (Method Spectrophotometry)']],
    ['Units', ['198']], 'Biological Reference Ranges' 
}

[{' ': [' ', ' ', ' ', ' '], 'Test Description': ['Test Description', 'Result', 'Units', 'Biological Reference Ranges'], 'Complete Blood Count (CBC) (Method: Coulter)': ['Complete Blood Count (CBC) (Method: Coulter)', ' ', ' ', ' '], 'Hemoglobin': ['Hemoglobin', '14.3', 'g/dL', '13.0-17.0'], 'RBC COUNT': ['RBC COUNT', '4.95', 'mil/uL', '4.5 5.5'], 'Hematocrit (HCT)': ['Hematocrit (HCT)', '41.9', '%', '40-54'], 'Platelet': ['Platelet', '2.22', 'lakh/Cumm1.50', '- 4.50'], 'MCV': ['MCV', '84.8', 'fl', '83 101'], 'MCH': ['MCH', '28.8', 'pg', '27-32'], 'MCHC': ['MCHC', '34.0', 'g/dL', '31.5 34.5'], 'RDW CV': ['RDW CV', '12.2', '%', '11.5 14.5'], 'Total WBC Count': ['Total WBC Count', '8130', 'cells/Cumm4000', '- 11000'], 'Neutrophils': ['Neutrophils', '65', '%', '40 75'], 'Lymphocytes': ['Lymphocytes', '26', '%', '20 40'], 'Eosinophils': ['Eosinophils', '04', '%', '0 6'], 'Monocytes': ['Monocytes', '05', '%', '2 10'], 'Basophils': ['Basophils', '00', '%', '0 1']}]

in this code, get Name: Hemoglobin, Result: 14.3, Units: g/dL, Ranges: 13.0-17.0 when pushed to mongodb