import os
import re


def _get_root_dir_name():
    current_directory = os.getcwd()

    if os.name == "nt":  # Windows
        drive, path = os.path.splitdrive(os.path.abspath(current_directory))
        root_dir_name = os.path.basename(drive + os.path.sep)
    else:  # Unix-like systems (Linux, macOS)
        root_dir_name = os.path.basename(os.path.abspath(os.path.sep))

    return root_dir_name


def _find_root_folder_or_root_file(max_parent_elevation: int):
    current_path = os.path.abspath(os.path.curdir)
    current_iteration = 0
    while (
        current_iteration < max_parent_elevation
        and current_path != _get_root_dir_name()
    ):  # Stop when reaching the root directory
        target_git_path = os.path.join(current_path, ".git")
        if os.path.exists(target_git_path) and os.path.isdir(target_git_path):
            return os.path.join(current_path)

        # Stop when reaching the root.txt file
        target_root_file_path = os.path.join(current_path, "root.txt")
        if os.path.exists(target_root_file_path) and os.path.isfile(
            target_root_file_path
        ):
            print(f"{os.path.dirname(target_root_file_path)=}")
            return os.path.dirname(target_root_file_path)

        current_path = os.path.dirname(current_path)
        current_iteration += 1

    return None  # Return None if the folder is not found


def _step_out_one_folder(current_path: str):
    return os.path.abspath(os.path.join(current_path, os.pardir))


def _get_file_extension(file_path: str):
    match = re.search(r"\.([^.]+)$", file_path)
    return str(match.group(1)) if match else None


def _find_repo_root(max_parent_elevation: int):
    root_dir = _find_root_folder_or_root_file(max_parent_elevation)
    return None if root_dir is None else root_dir


def _resolve_path(path_to_resolve: str, max_parent_elevation: int):
    repo_root = _find_repo_root(max_parent_elevation)
    if repo_root is None:
        return path_to_resolve
    return os.path.abspath(re.sub(r"^~", repo_root, path_to_resolve))


def resolved_path_to_repo_root(path_to_resolve: str, max_parent_elevation=3):
    resolved_path = _resolve_path(path_to_resolve, max_parent_elevation)
    resolved_path_to_repo_root_extension = _get_file_extension(
        resolved_path
    )
    if (
        resolved_path_to_repo_root_extension is None
        and os.path.exists(resolved_path) is False
    ):
        os.makedirs(resolved_path, exist_ok=True)
    else:
        os.makedirs(_step_out_one_folder(resolved_path), exist_ok=True)

    return resolved_path


if __name__ == "__main__":
    assert resolved_path_to_repo_root("~/") == "/workspaces/analytics_lab"
    assert resolved_path_to_repo_root("~/..") == "/workspaces"
    assert resolved_path_to_repo_root("/path/~") == "/path/~"

