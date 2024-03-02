import csv
import os
import pandas as pd
from fuzzywuzzy import process
import streamlit as st

# from fuzzywuzzy import fuzzy
import difflib

BACKGROUND_COLOR='#009bc9'
TEXT_COLOR='#ffffff'
def read_mapping_table(mapping_file):
    """ 
    Read mapping table from CSV file and return a dictionary mapping from the second column to the first column.
    :param mapping_file: Path to the CSV file containing the mapping table.
    :return: Dictionary mapping from the second column to the first column.
    """
    print(f"Reading mapping table from {mapping_file}")
    mapping_df = pd.read_csv(mapping_file, header=None)
    mapping = dict(zip(mapping_df[1], mapping_df[0]))
    return mapping

def generate_html_table(mapping, folder, test_file, output_file,background_color):
    """
    Generate an HTML table from a mapping dictionary and write it to a file.
    :param mapping: Dictionary mapping from the second column to the first column.
    :param folder: Path to the folder containing the images.
    :param test_file: Path to the CSV file containing the test data.
    :param output_file: Path to the output HTML file.
    :param background_color: Background color of the table.
    """

    test_df = pd.read_csv(test_file)
    # print(test_df.columns)
    rows = []
    for string in test_df['school']:
        # print((string))
        # print((mapping.values()))
        matched_string = process.extractOne(string, mapping.keys())
        if matched_string:
            matched_string = matched_string[0]
            image_file = mapping[matched_string]
            image_path = os.path.join(folder, image_file)
            if os.path.exists(image_path):
                rows.append({'': '<img src="{}" alt="{}" width="50">'.format(image_path, string), 'school': string})
        else:
            print(f"Image file {image_file} not found for string: {string}")
    # print(rows)
    # print(pd.DataFrame(rows))
    rows=pd.DataFrame(rows).merge(test_df)
    # rows=test_df.merge(pd.DataFrame(rows),left_on='school', right_on='School')

    # print(rows.columns)
    # rows=rows.drop(columns=['fname', 'Team', 'A', 'Unnamed: 5', 'B','Unnamed: 7'])
    
    # rows=rows.rename(columns={'TOT': 'Points'})
    # print(rows.columns)

    html_table = pd.DataFrame(rows).to_html(index=False, escape=False, 
                                            table_id='test_table', 
                                            classes='table', 
                                            header=True, 
                                            justify='left')

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Table</title>
        <style>
            body {{
                font-family: 'Lemon milk', sans-serif;
            }}
            .table {{
                border-collapse: collapse;
                width: 300;
            }}
            .table th, .table td {{
                padding: 8px;
                text-align: left;
                border:0px;
                border-top: 3px solid white;
                border-bottom: 3px solid white;
                background-color: {BACKGROUND_COLOR};
                color: {TEXT_COLOR};
            }}
            .table img {{
                vertical-align: middle;
            }}
        </style>
    </head>
    <body>
        {html_table}
    </body>
    </html>
    '''


    with open(output_file, 'w') as html_file:
        html_file.write(html_content)
    return html_content



if __name__ == "__main__":
    mapping_table_file = 'file_names_mappingcompetitive.csv'
    folder_with_images = 'Team Burgees'
    test_file = 'test.csv'
    output_html_file = 'output_table.html'

    background_color = st.selectbox("Select Background Color", ["#009bc9", "white", "#0039a4", "lightgreen"])
    print(background_color)

    mapping = read_mapping_table(mapping_table_file)
    html_table=generate_html_table(mapping, folder_with_images, test_file, output_html_file, background_color)
    
    
    # Streamlit app to run
    st.title("Test Table")
    st.markdown(html_table, unsafe_allow_html=True)
