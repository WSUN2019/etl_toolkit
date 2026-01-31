# created on 1/31/2026 WSUN
# this is a simple portal in python streamlit to access various helper tool files
# first one is FolderTreeMapper.py
import os
import streamlit as st
import pandas as pd
from datetime import datetime
from collections import defaultdict
from FolderTreeMapper.FolderTreeMapper import FolderTreeMapper

st.set_page_config(page_title="Folder Tree Mapper", layout="wide")
st.title("📂 Folder Tree Generator")

st.markdown("""
This app generates a visual folder/file structure of any folder you provide.
It saves the structure to a `.txt` file, shows a preview, and outputs statistics.
""")

# Input folder path
folder_path = st.text_input(
    "Enter folder path to map:",
    # r"C:\Users\[username]\app-folder\"
)

# Input optional output path
output_path = st.text_input(
    "Optional: Enter full output file path (including filename):",
    ""
)

# Default output folder
default_output_folder = os.path.join(os.getcwd(), "FolderTreeMapperOutput")
os.makedirs(default_output_folder, exist_ok=True)

def get_folder_stats(root_path):
    """Return folder stats: file count, folder count, counts by extension."""
    file_count = 0
    folder_count = 0
    ext_count = defaultdict(int)

    for dirpath, dirnames, filenames in os.walk(root_path):
        folder_count += len(dirnames)
        file_count += len(filenames)
        for f in filenames:
            ext = os.path.splitext(f)[1].lower() or "<no_extension>"
            ext_count[ext] += 1

    return file_count, folder_count, dict(ext_count)


if st.button("Generate Folder Structure"):
    if not os.path.isdir(folder_path):
        st.error("❌ Invalid folder path. Please check the folder path and try again.")
    else:
        # --- Determine output file path ---
        if output_path.strip():
            final_output_path = output_path
        else:
            folder_name = os.path.basename(folder_path.rstrip("\\/"))
            final_output_path = os.path.join(default_output_folder, f"{folder_name}_folder_structure.txt")

        # --- Save folder structure safely ---
        try:
            # Append timestamp if file exists
            if os.path.exists(final_output_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base, ext = os.path.splitext(final_output_path)
                final_output_path = f"{base}_{timestamp}{ext}"

            FolderTreeMapper.save_folder_structure(folder_path, final_output_path)
            st.success(f"✅ Folder structure saved to `{final_output_path}`")
            st.markdown(f"[Open file](file:///{final_output_path.replace(os.sep, '/')})")

        except PermissionError:
            # Permission denied → fallback to default folder
            folder_name = os.path.basename(folder_path.rstrip("\\/"))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_output_path = os.path.join(
                default_output_folder, f"{folder_name}_folder_structure_{timestamp}.txt"
            )
            FolderTreeMapper.save_folder_structure(folder_path, final_output_path)
            st.warning(f"⚠️ Could not write to specified path. Saved to default folder instead: `{final_output_path}`")
            st.markdown(f"[Open file](file:///{final_output_path.replace(os.sep, '/')})")

        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

        # --- Display statistics ---
        file_count, folder_count, ext_count = get_folder_stats(folder_path)
        st.subheader("📊 Folder Statistics")

        # Summary numbers
        st.markdown(f"**Total folders:** {folder_count}  \n**Total files:** {file_count}")

        # Files by extension as table
        if ext_count:
            df_ext = pd.DataFrame(
                sorted(ext_count.items(), key=lambda x: -x[1]), columns=["Extension", "Count"]
            )
            st.table(df_ext)  # Nice static table
        else:
            st.write("No files found in this folder.")

        # --- Display folder structure ---
        folder_tree_str = FolderTreeMapper.get_folder_structure_as_string(folder_path)
        st.text_area("Folder Structure Preview:", folder_tree_str, height=600)
