Created 1/31/2026 WSUN

Folder Tree Mapper - Instructions

How to run:

Open Command Prompt and navigate to the project folder:

cd "C:\Users\sunwi\python dev\etl_toolkit\FolderTools"


Run the Streamlit app:
python -m pip install -r requirements.txt
python -m streamlit run folder_toolbox.py


Usage in the app:

Folder Path: Enter the folder to map.

Output File Path (optional): Enter full path including filename, or leave blank to save in FolderTreeMapperOutput.

Generate Folder Structure: Click the button.

Saves the folder tree as a .txt file.

Displays a preview in the app.

Shows folder statistics (folders, files, file counts by extension).

Provides a clickable link to the output file.

Notes:

If the output file exists, a timestamp is added to avoid overwriting.

If the specified path is not writable, the app saves automatically in FolderTreeMapperOutput.