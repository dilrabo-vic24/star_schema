import os
import sys
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src import create_dimensions
from src import create_facts
from src import config
from src import create_schema_diagram

def extract():
    df_raw = pd.read_excel(config.RAW_DATA_PATH)

    #all dimensions
    dimensions = create_dimensions.create_dimension_tables(df_raw)

    #all facts and bridges 
    facts = create_facts.create_fact_bridge_tables(df_raw, dimensions)

    with pd.ExcelWriter(config.OUTPUT_EXCEL_PATH) as f:
        for name, df in dimensions.items():
            df.to_excel(f, sheet_name = name, index = False)

        for name, df in facts.items():
            df.to_excel(f, sheet_name = name, index = False)  

    create_schema_diagram.generate_schema_diagram(
        dimensions, 
        facts, 
        config.OUTPUT_DIAGRAM_PATH
    )

    print("Process finished successfully")

if __name__ == "__main__":
    extract()