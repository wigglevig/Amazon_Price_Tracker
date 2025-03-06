def count(file):
    with open(f"{file}",'r') as file1:
        a=file1.read()
    digits=0
    alphabets=0
    for i in a:
            if i.isalpha():
                digits+=1
            elif i.isnumeric():
                alphabets+=1
            else:
                pass
    print(digits , alphabets)         
            
count("abc.txt")
