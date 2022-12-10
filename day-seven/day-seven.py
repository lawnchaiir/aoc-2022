from collections import namedtuple

File = namedtuple("File", "name size")

class Directory(object):
    NEEDED_FREE_SPACE = 0

    def __init__(self, name):
        self._name = name
        self._files = []
        self._dirs = {}
        self._parent = None
        self._total_size = 0

    def set_parent_dir(self, dir):
        self._parent = dir

    def get_parent_dir(self):
        return self._parent

    def get_child_dir(self, name):
        if name in self._dirs:
            return self._dirs[name]

    def add_child_dir(self, name):
        if name not in self._dirs:
            dir = Directory(name)
            dir.set_parent_dir(self)
            self._dirs[name] = dir

    def add_file(self, name, size):
        file = File(name, int(size))
        self._files.append(file)

    def cache_total_sizes(self):
        size = 0
        for file in self._files:
            size += file.size

        for dir_name in self._dirs:
            sub_dir = self._dirs[dir_name]
            size += sub_dir.cache_total_sizes()

        self._total_size = size
        return size

    def part1(self):
        sum = 0
        if self._total_size < 100000:
            sum += self._total_size

        for dir_name in self._dirs:
            sub_dir = self._dirs[dir_name]
            sum += sub_dir.part1()

        return sum

    def part2(self):
        candidate_dir = self
        for dir_name in self._dirs:
            sub_dir = self._dirs[dir_name]

            if sub_dir._total_size < self.NEEDED_FREE_SPACE:
                continue

            new_candidate = sub_dir.part2()
            if new_candidate._total_size < candidate_dir._total_size:
                candidate_dir = new_candidate
        return candidate_dir

    def print_tree(self, depth=0):
        indent = " " * depth * 2
        print(indent + f"- {self._name} (dir) | total size {self._total_size}")
        for sub_dir_name in self._dirs:
            sub_dir = self._dirs[sub_dir_name]
            sub_dir.print_tree(depth + 1)

        indent += "  "
        for file in self._files:
            print(indent + f"- {file.name} (file, size={file.size})")


with open("input.txt") as f:
    # skip first line since it's just creating the root
    input = f.read().splitlines()[1:]


root = Directory("/")
current_dir = root

parsing_ls_command = False
for line in input:
    if line.startswith("$ "):
        parsing_ls_command = False
        if line.endswith("ls"):
            parsing_ls_command = True
            continue
        elif line.find("cd", len("$ "), len("$ ") + len("cd")) != -1:
            dir_name = line[len("$ cd "):]
            if dir_name == "..":
                current_dir = current_dir.get_parent_dir()
            else:
                current_dir = current_dir.get_child_dir(dir_name)
    elif parsing_ls_command:
        if line.startswith("dir "):
            dir_name = line[len("dir "):]
            current_dir.add_child_dir(dir_name)
        else:
            size, name = line.split(" ")
            current_dir.add_file(name, size)


root.cache_total_sizes()
# root.print_tree()

print("Part 1", root.part1())

FILE_SYSTEM_SIZE = 70000000
UPDATE_SIZE = 30000000
Directory.NEEDED_FREE_SPACE = UPDATE_SIZE - (FILE_SYSTEM_SIZE - root._total_size)

dir = root.part2()
print("Part 2", dir._total_size)

