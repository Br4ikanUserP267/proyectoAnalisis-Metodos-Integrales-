from sympy import symbols, integrate

# Definir el símbolo de la variable
x = symbols('x')

# Definir la función a integrar
f = 5*x +6*6**2 -1
# Calcular la integral indefinida
integral = integrate(f, x)

# Imprimir el resultado
print("La integral indefinida de f(x) =", integral)
