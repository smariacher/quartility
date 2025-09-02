import os


def convert_to_project_path(rel_path : str, file_for_absolute = "_quarto.yml"):
    
    """
    Converts a relative path to an absolute project path based on the location of a specified project file (default: '_quarto.yml').
    The function starts from the current working directory and traverses up the directory tree to locate the directory containing the specified file.
    If the file is found, the absolute path is constructed by joining that directory with the given relative path.
    If the file is not found, the absolute path is constructed by joining the current working directory with the relative path.
    

    Args:
        rel_path (str): The relative path to convert.
        file_for_absolute (str, optional): The filename to search for in parent directories. Defaults to '_quarto.yml'.
    Returns:
        str: The normalized absolute path within the project directory.
    """
    path = os.getcwd()
    while True:
        if os.path.exists(os.path.join(path, file_for_absolute)):
            return os.path.normpath(os.path.join(path, rel_path))
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    return os.path.normpath(os.path.join(path, rel_path))
