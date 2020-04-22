from sys import argv
import os


def split_class_def(iter_):
    """Splits into class or def lines."""
    iter_ = iter_.strip()
    if iter_.startswith("def"):
        iter_ = iter_[3:]
    # elif iter_.startswith("class"):
    #     x = iter_[6:-2]

    return iter_

class LazyTester:
    def __init__(self, fp, out=None):

        assert os.path.isfile(fp) and fp[-3:] == ".py", f"ERROR: No .py file found at {fp}"
        self.fp = fp
        if out:
            assert os.path.isdir(out), f"ERROR: No (empty) directory found at {out}"
            self.out = out
        else:
            self.out = os.path.dirname(fp)

        self.file_in_name = os.path.basename(fp)
        self.filename = "test_" + self.file_in_name
        self.output = os.path.join(self.out, self.filename)

        self.out_file_exists = os.path.exists(self.output)

    def makeLazy(self):
        """Makes a lazytest file."""
        with open(self.fp, "r") as infile:
            function_lines = filter(lambda x: x.strip().startswith(("def ", "class ")), infile.readlines())
            extracted_names = map(split_class_def, function_lines)
            if self.out_file_exists:
                extracted_names = self.filter_functions(extracted_names)

            with open(self.output, "a+") as outfile:
                if not self.out_file_exists:
                    self.header(outfile)
                self.write_functions(outfile, extracted_names)

                outfile.write("\n")

    def filter_functions(self, funcs):
        """Filters functions that are already in test file."""
        with open(self.output, "r") as outread:
            test_lines = filter(lambda x: x.startswith("def"), outread.readlines())
            extracted_tests = map(lambda x: x[9:].split("(")[0].strip(), test_lines)
            extracted_names = filter(lambda x: x not in extracted_tests, funcs)
        return extracted_names

    def header(self, outfile):
        """Header lines."""
        if len(argv) > 2:
            outfile.write("import os\n")
            outfile.write(f"os.path.append(r\"{os.path.dirname(self.fp)}\")\n")
        outfile.write(f"import {self.file_in_name[:-3]}\n")
        outfile.write("import pytest")

    def write_functions(self, outfile, funcs):
        """Writes functions to outfile."""
        classname = None
        for func in funcs:
            if func.startswith("class "):
                classname = func[6:-1].strip()
            else:
                class_method = "self" in func
                func = func.split("(")[0].strip()
                if class_method:
                    func = f"{classname}_{func}"
                outfile.write(f"\n\n\ndef test_{func}():\n")
                outfile.write(f"    \"\"\"Tests {self.file_in_name}.{func}.\"\"\"\n")
                outfile.write("    assert False")


def main():
    """Makes a test format file for python scripts."""
    assert len(argv) > 1, "ERROR: Missing file path"
    fp = argv[1]
    if len(argv) > 2:
        out = argv[2]
    else:
        out = None
        
    LazyTester(fp, out=out).makeLazy()


if __name__ == "__main__":
    main()
