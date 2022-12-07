#!/usr/bin/env python3
# coding:utf-8

with open("input.txt", 'r+', encoding="UTF-8") as input_file:
    raw_input = input_file.readlines()


class File:
    def __init__(self, name, size__):
        self.name = name
        self.size = size__

    def __repr__(self):
        return f"(file {self.name}, size:{self.size})"


class Folder:
    def __init__(self, name, parent):
        self.name = name
        self.files_and_dirs = {}
        self.parent = parent
        self.size = 0

    def add_file_or_dir(self, file_or_dir):
        self.files_and_dirs[file_or_dir.name] = file_or_dir

    def compute_total_size(self):
        self.size = 0
        for e in self.files_and_dirs.keys():
            if isinstance(self.files_and_dirs[e], File):
                self.size += self.files_and_dirs[e].size
                # print(e, self.files_and_dirs[e].size)
            else:
                self.size += self.files_and_dirs[e].compute_total_size()
                # print(e, self.files_and_dirs[e].compute_total_size())
        return self.size

    def find_dir_size_at_most(self, at_most):
        # self.compute_total_size()
        res = []
        for e in self.files_and_dirs.keys():
            dir_ = self.files_and_dirs[e]
            if not isinstance(dir_, File):
                if dir_.size <= at_most:
                    res.append(dir_)
                res.extend(dir_.find_dir_size_at_most(at_most))
                # print(dir_.name, dir_.size)
        return res

    def list_dir_size_greater_than(self, size__):
        res = []
        for e in self.files_and_dirs.keys():
            dir_ = self.files_and_dirs[e]
            if not isinstance(dir_, File):
                if dir_.size >= size__:
                    res.append([dir_.size, dir_])
                res.extend(dir_.list_dir_size_greater_than(size__))
        return res

    def cd(self, dir_name_):
        return self.files_and_dirs[dir_name_]

    def __repr__(self):
        return f"[dir {self.name} (parent {self.parent}) that contains {self.files_and_dirs}]"


class FileSystem(Folder):
    def __init__(self):
        super().__init__('/', None)


file_system = actual_dir = FileSystem()
list_ = False
for line in raw_input:
    line = line.replace("\n", "")
    if line.startswith('$'):
        list_ = False
        if line.startswith("$ cd"):
            dir_name = line[5:]
            if dir_name == '/':
                continue
            elif dir_name != '..':
                actual_dir = actual_dir.cd(dir_name)
            else:
                actual_dir = actual_dir.parent
            # print(f"cd {dir_name}, actual_dir is {actual_dir}")
        elif line == "$ ls":
            list_ = True
    elif list_:
        if line.startswith("dir"):
            new_dir = Folder(name=line[4:], parent=actual_dir)
            actual_dir.add_file_or_dir(new_dir)
            # print(f"dir {line[4:]}")
        else:
            line_split = line.split()
            size_ = line_split[0]
            name_ = line_split[1]
            new_file = File(name_, int(size_))
            actual_dir.add_file_or_dir(new_file)

file_system_total_size = file_system.compute_total_size()
print(file_system_total_size)
sum_ = 0
for folder in file_system.find_dir_size_at_most(100000):
    # print(folder)
    sum_ += folder.size
print(sum_)


disk_space = 70000000
at_least_required = 30000000
unused_space = disk_space - file_system_total_size
need_to_delete = at_least_required - unused_space

candidates_to_deletion = file_system.list_dir_size_greater_than(need_to_delete)
min_size = candidates_to_deletion[0][0]
for size, folder in candidates_to_deletion:
    if size < min_size:
        min_size = size
print(min_size)
