# created on 1/31/2026 WSUN
# this navigates a folder and maps every nested subfolder and file
import os

class FolderTreeMapper:
    @staticmethod
    def generate_tree(startpath, indent=""):
        """
        Recursively generate folder/file tree as a list of strings.
        Returns a list of strings representing the tree.
        """
        tree_lines = []
        try:
            items = sorted(os.listdir(startpath))
        except PermissionError:
            return tree_lines  # skip folders we can't access
        for index, item in enumerate(items):
            path = os.path.join(startpath, item)
            connector = "└─ " if index == len(items) - 1 else "├─ "
            if os.path.isdir(path):
                tree_lines.append(f"{indent}{connector}{item}/")
                extension = "   " if index == len(items) - 1 else "│  "
                tree_lines.extend(FolderTreeMapper.generate_tree(path, indent + extension))
            else:
                tree_lines.append(f"{indent}{connector}{item}")
        return tree_lines

    @staticmethod
    def save_folder_structure(root_path, output_file=None):
        """
        Save the folder structure of root_path to a text file.
        If output_file is None, generates one based on folder name.
        Returns the output file path.
        """
        folder_name = os.path.basename(root_path.rstrip("\\/"))
        if output_file is None:
            output_file = f"{folder_name}_folder_structure.txt"

        tree = [f"{folder_name}/"]
        tree.extend(FolderTreeMapper.generate_tree(root_path))

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(tree))

        return output_file

    @staticmethod
    def get_folder_structure_as_string(root_path):
        """
        Return the folder structure as a single string (no file saved).
        """
        folder_name = os.path.basename(root_path.rstrip("\\/"))
        tree = [f"{folder_name}/"]
        tree.extend(FolderTreeMapper.generate_tree(root_path))
        return "\n".join(tree)
