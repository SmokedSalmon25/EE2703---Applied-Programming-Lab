def matmul(A, B):
    m = len(A)   #to store number of rows in A
    o = len(B)   #to store number of rows in B
    flag = 0    #to check which row we are in 
    row_len = 0
    for row in A:
        if flag == 0:
            flag += 1
            row_len  = len(row)     #storing the length of the first row to compare with the rest
        if not hasattr(row, '__iter__'):       
            raise TypeError     #in case each row is not iterable through
        if (len(row) != row_len):
            raise ValueError        #in case the rows differ in length
        for element in row:
            if not isinstance(element, (int, float)):
                raise TypeError     #in case any element is not an integer or a float
    #performing identical operations for matrix B
    for row in B:
        if flag == 1:
            flag += 1
            row_len  = len(row)
        if not hasattr(row, '__iter__'):
            raise TypeError
        if (len(row) != row_len):
            raise ValueError
        for element in row:
            if not isinstance(element, (int, float)):
                raise TypeError
    n = len (A[0])      #number of columns in A
    p = len (B[0])      #number of columns in B
    if (n != o):        #checking if the sizes match
        raise ValueError
    else:
        mat = []        #creating an empty matrix to store the output
        for row_no in range (m):
            final_row = []      #creating an empty list to store each row
            for column_no in range (p):
                sum1 = 0
                for index in range (n):
                    sum1 += A[row_no][index] * B[index][column_no]      #multiplying each row with the corresponding column to get the sum
                final_row.append(sum1)
            mat.append(final_row)
        return mat



