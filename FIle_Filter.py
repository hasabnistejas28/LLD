from abc import ABC, abstractmethod
from typing import List

# ---------------------------
# File System Simulation
# ---------------------------

class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.extension = name.split('.')[-1] if '.' in name else None

    def __repr__(self):
        return f"File(name={self.name}, size={self.size} bytes)"


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.files: List[File] = []
        self.subdirs: List['Directory'] = []

    def add_file(self, file: File):
        self.files.append(file)

    def add_directory(self, directory: 'Directory'):
        self.subdirs.append(directory)


# ---------------------------
# Strategy Pattern
# ---------------------------

class SearchStrategy(ABC):
    @abstractmethod
    def match(self, file: File) -> bool:
        pass


class SizeStrategy(SearchStrategy):
    """Strategy to find files based on their size using a comparison operator."""
    def __init__(self, size: int, op: str):
        self.size = size
        valid_ops = ['>', '<', '==', '>=', '<=']
        if op not in valid_ops:
            raise ValueError(f"Invalid operator '{op}'. Use one of {valid_ops}")
        self.op_string = op

    def match(self, file: File) -> bool:
        if self.op_string == '>':
            return file.size > self.size
        elif self.op_string == '<':
            return file.size < self.size
        elif self.op_string == '==':
            return file.size == self.size
        elif self.op_string == '>=':
            return file.size >= self.size
        elif self.op_string == '<=':
            return file.size <= self.size
        return False


class ExtensionStrategy(SearchStrategy):
    def __init__(self, extension: str):
        self.extension = extension

    def match(self, file: File) -> bool:
        return file.extension == self.extension


class NameContainsStrategy(SearchStrategy):
    def __init__(self, substring: str):
        self.substring = substring

    def match(self, file: File) -> bool:
        return self.substring in file.name


# ---------------------------
# Boolean Composition
# ---------------------------

class AndStrategy(SearchStrategy):
    def __init__(self, left: SearchStrategy, right: SearchStrategy):
        self.left = left
        self.right = right

    def match(self, file: File) -> bool:
        return self.left.match(file) and self.right.match(file)


class OrStrategy(SearchStrategy):
    def __init__(self, left: SearchStrategy, right: SearchStrategy):
        self.left = left
        self.right = right

    def match(self, file: File) -> bool:
        return self.left.match(file) or self.right.match(file)


class NotStrategy(SearchStrategy):
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def match(self, file: File) -> bool:
        return not self.strategy.match(file)


# ---------------------------
# Find Function
# ---------------------------

def find(directory: Directory, strategy: SearchStrategy) -> List[File]:
    """Recursively search all files in directory (and subdirectories) that match strategy."""
    matched_files = []

    # Check files in current directory
    for file in directory.files:
        if strategy.match(file):
            matched_files.append(file)

    # Recurse into subdirectories
    for subdir in directory.subdirs:
        matched_files.extend(find(subdir, strategy))

    return matched_files


# ---------------------------
# Demo
# ---------------------------

if __name__ == "__main__":
    # Build directory structure
    root = Directory("root")
    root.add_file(File("report.pdf", 1500))          # ~1.5 KB
    root.add_file(File("photo.jpg", 3_000_000))      # 3 MB
    root.add_file(File("notes.txt", 500))            # 0.5 KB

    subdir = Directory("subdir")
    subdir.add_file(File("slides.pdf", 1000))        # 1 KB
    subdir.add_file(File("bigdata.csv", 5_000_000))  # 5 MB
    root.add_directory(subdir)

    # Example 1: Files < 2MB
    print("Files < 2MB:")
    print(find(root, SizeStrategy(2 * 1024 * 1024, "<")))

    # Example 2: Files >= 5MB
    print("\nFiles >= 5MB:")
    print(find(root, SizeStrategy(5 * 1024 * 1024, ">=")))

    # Example 3: All .pdf files
    print("\nFiles with .pdf extension:")
    print(find(root, ExtensionStrategy("pdf")))

    # Example 4: Large JPGs (>2MB AND extension .jpg)
    print("\nFiles >2MB AND extension .jpg:")
    print(find(root, AndStrategy(SizeStrategy(2 * 1024 * 1024, ">"),
                                 ExtensionStrategy("jpg"))))

    # Example 5: All files NOT .txt
    print("\nFiles that are NOT .txt:")
    print(find(root, NotStrategy(ExtensionStrategy("txt"))))
