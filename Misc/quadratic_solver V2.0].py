a = int(input("enter coeffients of x^2: "))
b = int(input("enter coeffients of x: "))
c = int(input("enter coeffients of 1: "))
discriminant = (b**2) - (4 * a * c)
if discriminant >= 0:
    D = (abs(discriminant))**0.5
    x1 = ((-b) + (D)) / (2 * a)
    x2 = ((-b) - (D)) / (2 * a)
else:
    D = (abs(discriminant))**0.5
    real = str(-b / (2 * a))
    imag = str(D / (2 * a))
    x1 = real + '+' + imag + "i"
    x2 = real + '-' + imag + "i"
print(x1, x2, sep=", ")
