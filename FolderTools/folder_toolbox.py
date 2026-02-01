# created on 1/31/2026 WSUN
# Simple Streamlit portal to access various helper tool files
# First tool: FolderTreeMapper.py

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
    r"C:\Users\username\folder-to-map"
)

# Input optional output path
output_path = st.text_input(
    "Optional: Enter full output file path (including filename or folder):",
    r"C:\Users\username\output-tree-map"
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


def generate_output_path(folder_path, output_path_input):
    """Return a safe output file path with .txt and timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # If user provided nothing → use default folder
    if not output_path_input.strip():
        folder_name = os.path.basename(folder_path.rstrip("\\/"))
        return os.path.join(default_output_folder, f"{folder_name}_folder_structure_{timestamp}.txt")

    # If path exists and is a folder → create file inside it
    if os.path.isdir(output_path_input):
        folder_name = os.path.basename(folder_path.rstrip("\\/"))
        return os.path.join(output_path_input, f"{folder_name}_folder_structure_{timestamp}.txt")

    # If path is a file name → append .txt if missing
    final_path = output_path_input
    if not final_path.lower().endswith(".txt"):
        final_path += ".txt"

    # Ensure timestamp is in the filename
    base, ext = os.path.splitext(final_path)
    final_path = f"{base}_{timestamp}{ext}"
    return final_path


if st.button("Generate Folder Structure"):
    if not os.path.isdir(folder_path):
        st.error("❌ Invalid folder path. Please check the folder path and try again.")
    else:
        final_output_path = generate_output_path(folder_path, output_path)

        try:
            FolderTreeMapper.save_folder_structure(folder_path, final_output_path)
            st.success(f"✅ Folder structure saved to `{final_output_path}`")

        except PermissionError:
            fallback_path = os.path.join(default_output_folder, f"folder_structure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            FolderTreeMapper.save_folder_structure(folder_path, fallback_path)
            st.warning(f"⚠️ Could not write to specified path. Saved to default folder instead: `{fallback_path}`")

        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

        # --- Display statistics ---
        file_count, folder_count, ext_count = get_folder_stats(folder_path)
        st.subheader("📊 Folder Statistics")
        st.markdown(f"**Total folders:** {folder_count}  \n**Total files:** {file_count}")

        if ext_count:
            df_ext = pd.DataFrame(
                sorted(ext_count.items(), key=lambda x: -x[1]), columns=["Extension", "Count"]
            )
            st.table(df_ext)
        else:
            st.write("No files found in this folder.")

        # --- Display folder structure ---
        folder_tree_str = FolderTreeMapper.get_folder_structure_as_string(folder_path)
        st.text_area("Folder Structure Preview:", folder_tree_str, height=600)
