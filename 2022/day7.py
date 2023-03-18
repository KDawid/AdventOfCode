from typing import Dict, List

from dataclasses import dataclass

_INPUT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


@dataclass(frozen=True)
class File:
    name: str
    size: int


class Folder:
    def __init__(self, name: str):
        self.name: str = name
        self.parent_folder: Folder = None
        self.child_folders: Dict[str, Folder] = dict()
        self.files: List[File] = []

    def get_total_size(self) -> int:
        result = 0
        result += sum([file.size for file in self.files])
        for child_folder in self.child_folders.values():
            result += child_folder.get_total_size()
        return result

    def add_parent(self, parent_folder):
        self.parent_folder: Folder = parent_folder

    def __str__(self):
        return f"{self.name}\t{self.files}\t{[str(folder) for folder in self.child_folders.values()]}"


def _read_file_system(lines: List[str]) -> (Folder, List[Folder]):
    file_system = Folder("/")
    all_folders = [file_system]
    current_folder = file_system
    for line in lines:
        # print(line)
        if line == "$ cd /":
            print("Go to the root")
            current_folder = file_system
        elif line == "$ ls":
            print("Listing starting")
        elif line == "$ cd ..":
            print("Go to parent")
            current_folder = current_folder.parent_folder
        elif line.startswith("$ cd "):
            folder_name = line[5:]
            print(f"Go to child {folder_name}")
            if folder_name not in current_folder.child_folders:
                raise ValueError(f"No child named {folder_name} in {current_folder}")
            current_folder = current_folder.child_folders[folder_name]
        else:
            if line.startswith("dir"):
                folder_name = line.split(" ")[1]
                print(f"\tFolder: {folder_name}")
                new_folder = Folder(name=folder_name)
                new_folder.parent_folder = current_folder
                current_folder.child_folders[folder_name] = new_folder
                all_folders.append(new_folder)
            else:
                file_size, file_name = line.split(" ")
                print(f"\tFile: {file_name}")
                current_folder.files.append(File(name=file_name, size=int(file_size)))
    return file_system, all_folders


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")

    file_system, all_folders = _read_file_system(lines)
    size_max = 100000
    needed_space = 30000000 - (70000000 - file_system.get_total_size())

    sum_of_small_file_sizes = 0
    smallest_big_enough_size = 70000000
    for folder_size in [folder.get_total_size() for folder in all_folders]:
        if folder_size <= size_max:
            sum_of_small_file_sizes += folder_size
        if needed_space <= folder_size < smallest_big_enough_size:
            smallest_big_enough_size = folder_size

    print()
    print(sum_of_small_file_sizes)
    print(smallest_big_enough_size)


