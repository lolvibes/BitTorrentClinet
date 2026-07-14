with open("test_file.bin", "rb") as f1, open("test_file_n.bin", "rb") as f2:
    data1 = f1.read()
    data2 = f2.read()

if data1 == data2:
    print("Files are identical.")
else:
    print("Files differ.")