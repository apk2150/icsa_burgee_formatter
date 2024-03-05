import streamlit as st


def main():

    #replace img source with any image in a folder (folder will be in same directory as debug.py)
    html_table = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Table</title>
    </head>
    <body>
    <tbody>
        <td><img src="Team Burgees/Stanford.png" alt="Stanford burgee" width="50"></td>
      <td>Stanford University</td>
      <td>1</td>
      </tbody>
    </body>
    </html>
    '''
        
    # Streamlit app to run
    st.title("Test Table")
    st.components.v1.html(html_table, height=800, scrolling=True)


if __name__ == "__main__":
    main()
