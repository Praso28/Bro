def main(input_file_name = "testcase.txt", output_file_name = "output.txt"):
    input_file = open(input_file_name, "r")
    first_line = input_file.readline().strip()
    output_file = open(output_file_name, "w")
    first_line = first_line.split(";")
    output_file.write(f"{first_line[0]}={first_line[1]}/{1}/{1}\n")
    output_file.close()
    input_file.close()

if __name__ == "__main__":
    main()