from sys import argv
import os


def main():
    """Makes a test format file for python scripts"""
    assert len(argv) > 1, "ERROR: Missing file path"
    fp = argv[1]
    assert os.path.isfile(fp) and fp[-3:] == ".py", f"ERROR: No .py file found at {fp}"

    if len(argv) > 2:
        out = argv[2]
        assert os.path.isdir(out), f"ERROR: No (empty) directory found at {out}"
    else:
        out = os.path.dirname(fp)

    file_in_name = os.path.basename(fp)
    filename = "test_" + file_in_name
    output = os.path.join(out, filename)

    out_file_exists = os.path.exists(output)

    with open(fp, "r") as infile:
        function_lines = filter(lambda x: x.startswith("def"), infile.readlines())
        extracted_names = map(lambda x: x[3:].split("(")[0].strip(), function_lines)
        if out_file_exists:
            with open(output, "r") as outread:
                test_lines = filter(lambda x: x.startswith("def"), outread.readlines())
                extracted_tests = map(lambda x: x[9:].split("(")[0].strip(), test_lines)
                extracted_names = filter(lambda x: x not in extracted_tests, extracted_names)

        with open(output, "a+") as outfile:
            if not out_file_exists:
                if len(argv) > 2:
                    outfile.write("import os\n")
                    outfile.write(f"os.path.append(r\"{os.path.dirname(fp)}\")\n")
                outfile.write(f"import {file_in_name[:-3]}\n")
                outfile.write("import pytest")

            for func in extracted_names:
                outfile.write(f"\n\n\ndef test_{func}():\n")
                outfile.write(f"    \"\"\"Tests {file_in_name}.{func}.\"\"\"\n")
                outfile.write("    assert False")

            outfile.write("\n")


if __name__ == "__main__":
    main()
