# Star Schema Design and Implementation for Meeting Data

## Project Objective

This project aims to design and implement a Star Schema for meeting-related data. The primary goal is to transform raw, denormalized data from an Excel file (`raw_data.xlsx`) into a structured dimensional model. This model, consisting of fact and dimension tables, is optimized for analytical queries and business intelligence reporting.

The entire process, from data extraction to final output, is automated through a Python pipeline. The project also includes functionality to automatically generate a visual diagram of the resulting schema.

## Key Features

- **ETL Pipeline:** A complete Extract, Transform, and Load (ETL) process built with Python and Pandas.
- **Star Schema Model:** Creates a classic star schema with a central fact table and surrounding dimension tables.
- **Surrogate Keys:** Generates unique, stable surrogate keys (UUIDs) for dimension tables to ensure data integrity.
- **Automated Schema Visualization:** Automatically generates a PNG diagram of the schema using the `Graphviz` library.
- **Modular Architecture:** The code is organized into logical modules for configuration, utilities, and data processing, making it clean, maintainable, and scalable.
- **Reproducibility:** All dependencies are listed in `requirements.txt` for easy setup and execution in any environment.

---

## Project Architecture

The project follows a modular structure to separate concerns and improve code readability.