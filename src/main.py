def main(input_file_name = "testcase.txt", output_file_name = "output.txt"):
    input_file = open(input_file_name, "r")

    line = input_file.readline()
    print(line)

    output_file = open(output_file_name, "w")
    output_file.write(line)
    output_file.close()