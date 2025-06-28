import os

#main folder
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#data folder
DATA_FOLDER = os.path.join(BASE_FOLDER, 'data')
RAW_DATA_PATH = os.path.join(DATA_FOLDER, 'raw_data.xlsx')

# outputs folder
OUTPUT_FOLDER = os.path.join(BASE_FOLDER, 'outputs')
OUTPUT_EXCEL_PATH = os.path.join(OUTPUT_FOLDER, 'final_data.xlsx')
OUTPUT_DIAGRAM_PATH = os.path.join(OUTPUT_FOLDER, 'star_schema_diagram.png')