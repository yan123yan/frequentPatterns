import matplotlib.pyplot as pl

line_2_A = [0,33,27,27,31,21,19,19]
for i in range(len(line_2_A)):
    line_2_A[i] = int(line_2_A[i] / 2)

line_2_F = [73,17,14,14,13,11,10,10]

x = [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

line_3_A = [157,32,28,26,26,20,20,20]
for j in range(len(line_3_A)):
    line_3_A[j] = int(line_3_A[j] / 2)
line_3_F = [42,16,14,13,13,10,10,10]

line_4_A = [0,28,26,26,26,20,20,20]
for q in range(len(line_4_A)):
    line_4_A[q] = int(line_4_A[q] / 2)
line_4_F = [21,14,13,13,13,10,10,10]

def kto2():
    pl.title("Compared Results when K = 2")
    pl.plot(x,line_2_A,color='red',label="Apriori Algorithm")
    pl.plot(x,line_2_F,color='blue',label="FP-Growth Algorithm")
    pl.legend()
    pl.xlabel("Similarity Threshold")
    pl.ylabel("Numbers of Algorithm Result")
    pl.show()

def kto3():
    pl.title("Compared Results when K = 3")
    pl.plot(x,line_3_A,color='red',label="Apriori Algorithm")
    pl.plot(x,line_3_F,color='blue',label="FP-Growth Algorithm")
    pl.legend()
    pl.xlabel("Similarity Threshold")
    pl.ylabel("Numbers of Algorithm Result")
    pl.show()

def kto4():
    pl.title("Compared Results when K = 4")
    pl.plot(x,line_4_A,color='red',label="Apriori Algorithm")
    pl.plot(x,line_4_F,color='blue',label="FP-Growth Algorithm")
    pl.legend()
    pl.xlabel("Similarity Threshold")
    pl.ylabel("Numbers of Algorithm Result")
    pl.show()

def allk():
    pl.title("Compared Results")
    pl.plot(x, line_2_A, color='red', linestyle=":", label="Apriori Algorithm K=2")
    pl.plot(x, line_2_F, color='red', label="FP-Growth Algorithm K=2")
    pl.plot(x, line_3_A, color='blue', linestyle=":", label="Apriori Algorithm K=3")
    pl.plot(x, line_3_F, color='blue', label="FP-Growth Algorithm K=3")
    pl.plot(x, line_4_A, color='green', linestyle=":", label="Apriori Algorithm K=4")
    pl.plot(x, line_4_F, color='green', label="FP-Growth Algorithm K=4")
    pl.legend()
    pl.xlabel("Similarity Threshold")
    pl.ylabel("Numbers of Algorithm Result")
    pl.show()

kto2()
kto3()
kto4()
allk()