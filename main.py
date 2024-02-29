import csv
import os
import pandas as pd
from fuzzywuzzy import process
import streamlit as st

# from fuzzywuzzy import fuzzy
import difflib

BACKGROUND_COLOR='#009bc9'
def read_mapping_table(mapping_file):
    mapping_df = pd.read_csv(mapping_file, header=None)
    mapping = dict(zip(mapping_df[1], mapping_df[0]))
    return mapping

def generate_html_table(mapping, folder, test_file, output_file):
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

    print(rows.columns)
    rows=rows.drop(columns=['fname', 'Team', 'A', 'Unnamed: 5', 'B','Unnamed: 7'])
    
    rows=rows.rename(columns={'TOT': 'Points'})
    print(rows.columns)

    html_table = pd.DataFrame(rows).to_html(index=False, escape=False, 
                                            table_id='test_table', 
                                            classes='table', 
                                            header=True, 
                                            justify='left')

    html_content = fhtml_content = f'''
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
                color: white;
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
    test_file = 'techscore.csv'
    output_html_file = 'output_table.shtml'

    mapping = read_mapping_table(mapping_table_file)
    html_table=generate_html_table(mapping, folder_with_images, test_file, output_html_file)
    print("output file:",output_html_file)


     # Upload test.csv file
    uploaded_file = st.file_uploader("Upload Test CSV", type=["csv"])
    if uploaded_file is not None:
        test_df = pd.read_csv(uploaded_file, header=None)

        # Select background color
        background_color = st.selectbox("Select Background Color", ["white", "lightgray", "lightblue", "lightgreen"])

        mapping = read_mapping_table(mapping_table_file)
        html_table = generate_html_table(mapping, folder_with_images, test_df, background_color)

        # Display HTML table
        st.markdown(html_table, unsafe_allow_html=True)