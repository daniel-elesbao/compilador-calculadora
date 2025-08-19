Compilador Calculadora
=====================

Este compilador está escrito em python e para rodar basta executar o arquivo `.py` diretamente.

## Exemplos de Uso da Calculadora

## Exemplo 1: Operações básicas

x = 10

y = 20

soma = x + y

imprima(soma)

imprima(x * y - 50)

## Exemplo 2: Expressões complexas
a = 2

b = 3

c = 4

resultado = a + b * c ^ 2 - (a + b) / c

imprima(resultado)

## Exemplo 3: Números decimais
pi = 3.14159

raio = 5.5

area = pi * raio ^ 2

imprima(area)

## Exemplo 4: Entrada do usuário
imprima(10 + 20)

leia(numero)

dobro = numero * 2

imprima(dobro)

## Exemplo 5: Programa completo

# Calculadora de equação do segundo grau (discriminante)

leia(a)

leia(b) 

leia(c)

discriminante = b ^ 2 - 4 * a * c

imprima(discriminante)

## Exemplo de uso interativo:

calc> x = 10
x = 10.0

calc> y = x + 5
y = 15.0

calc> imprima(x * y)
150.0

calc> leia(z)
Digite o valor para z: 7.5
z = 7.5

calc> resultado = (x + y) / z
resultado = 3.3333333333333335

calc> imprima(resultado)
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
