import csv
import os
import pandas as pd
from fuzzywuzzy import process


def read_mapping_table(mapping_file):
    mapping_df = pd.read_csv(mapping_file, header=None)
    mapping = dict(zip(mapping_df[0], mapping_df[1]))
    return mapping

def generate_html_table(mapping, folder, test_file, output_file):
    test_df = pd.read_csv(test_file, header=None)
    rows = []
    for string in test_df[0]:
        matched_string, score = process.extractOne(string, mapping.keys())
        if score >= 90:  # You can adjust the threshold as needed
            image_file = mapping[matched_string]
            image_path = os.path.join(folder, image_file)
            if os.path.exists(image_path):
                rows.append({'String': string, 'Image': '<img src="{}" alt="{}" width="100">'.format(image_path, string)})
            else:
                print(f"Image file {image_file} not found for string: {string}")

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
                width: 100%;
            }}
            .table th, .table td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
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

if __name__ == "__main__":
    mapping_table_file = 'file_name_mappings.csv'
    folder_with_images = 'Team Burgees'
    test_file = 'test.csv'
    output_html_file = 'output_table.shtml'

    mapping = read_mapping_table(mapping_table_file)
    generate_html_table(mapping, folder_with_images, test_file, output_html_file)
    print("output file:",output_html_file)