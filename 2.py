#Q1
#list
#int
#9
#8, 15
"""
Line1: name a list temperature
Line5: define a function which check if the temp in temperatures higher than threshold
line12: define a function which do basic same as last one but save the temp higher into a list indices
"""

#Q2
def matrix_count(column, row):    #give a function
    matrix = [[column for column in range(column)] for row in range(row)]  #define column and row in matrix
    cunt, i = 0, 0    #set two variable
    for length in matrix:   #set a length of matrix
        cunt += matrix[i][i]  # find the every number of matrix
        i += 1  # make the number of column and row increase until the maximum
    return matrix  # end

#Q3
def common_elements(list1, list2):   #give a function
    fin = []  # define a list
    for i in list2: # i and j reduce 1 because in forloop, the number is begin form 1, if j-1 and i-1 is equal, which is means this number is a common elements
        for j in list1:
            if list1[j-1] == list2[i-1]:
                fin.append(list1[j-1])
    return fin  #end

#Q4
def is_palindrome(word):  # give a function
    if word[0] == word[-1]:  # it means the first number and the last number is common.
        print("Palindrome")
    else:
        print("Not Palindrome")

#Q5