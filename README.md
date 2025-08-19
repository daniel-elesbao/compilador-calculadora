Compilador Calculadora
=====================

Este compilador está escrito em python e para rodar basta executar o arquivo `.py` diretamente.

## Exemplos de Uso da Calculadora

## Exemplo 1: Operações básicas

x = 10

y = 20

soma = x + y

print(soma)

print(x * y - 50)

## Exemplo 2: Expressões complexas
a = 2

b = 3

c = 4

resultado = a + b * c ^ 2 - (a + b) / c

print(resultado)

## Exemplo 3: Números decimais
pi = 3.14159

raio = 5.5

area = pi * raio ^ 2

print(area)

## Exemplo 4: Entrada do usuário
print(10 + 20)

read(numero)

dobro = numero * 2

print(dobro)

## Exemplo 5: Programa completo

# Calculadora de equação do segundo grau (discriminante)
print("Digite os valores de a, b e c:")

read(a)

read(b) 

read(c)

discriminante = b ^ 2 - 4 * a * c

print(discriminante)

## Exemplo de uso interativo:

calc> x = 10
x = 10.0

calc> y = x + 5
y = 15.0

calc> print(x * y)
150.0

calc> read(z)
Digite o valor para z: 7.5
z = 7.5

calc> resultado = (x + y) / z
resultado = 3.3333333333333335

calc> print(resultado)
3.3333333333333335
```

## Como executar:

### Modo interativo:
python calculadora.py

### Executar arquivo:
python calculadora.py exemplo1.calc

### Precedência de operadores (da maior para menor):
1. ^ (potenciação) - associativa à direita
2. * / (multiplicação e divisão) - associativa à esquerda  
3. + - (adição e subtração) - associativa à esquerda
4. Operadores unários + e - têm precedência máxima
