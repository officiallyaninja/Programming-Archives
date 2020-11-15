from matrices import transpose, polynomial
import matplotlib.pyplot as plt
import numpy as np

print("-hello and welcome to the polynomials grapher. credits - Arjun Pratap")
print('-this is a program wherein you input some points, and get the plot of a polynomial that intersects the points you give')
print('-please input points is one of the forms given below')
print("  x,y")
print(" (x,y)")
print(" [x,y]")
print('-once you are done entering points, simply type in "DONE" or press enter without typing anyhthing to view your plot')
print('-the title of the plot will be the equation of the polynomial being plotted')
print("")


p_mat, p, e = [], [], ""
while True:
    try:
        e = eval(input("enter a point: "))
    except:
        break
    p.append(e)
for point in p:
    p_mat.append(list(point))


p_mat = sorted(p_mat)
margin = (p_mat[-1][0] - p_mat[0][0]) / 3
# setting the x - coordinates
x = np.arange(p_mat[0][0] - margin, p_mat[-1][0] + margin, 0.001)
# setting the corresponding y - coordinates
co_efs = polynomial(p_mat)
y = 0
for i in range(0, len(co_efs)):
    y += co_efs[i] * x ** i

# plotting the points
plt.plot(x, y)
plt.scatter(transpose(p_mat)[0], transpose(p_mat)[1])

text = ''
for i in range(0, len(co_efs)):
    text += (str(round(co_efs[i], 2)) + "x" * (i != 0) + "^" * (i != 0 and i != 1) +
             str(i) * (i != 1) + '+' * (i != len(co_efs) - 1))


plt.suptitle(text)
# function to show the plot
plt.show()
