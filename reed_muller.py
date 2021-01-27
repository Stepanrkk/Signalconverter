# -*- coding: utf-8 -*-
"""Reed-Muller.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N20-ysz_aS5nAAw-dvcaHlLdI3veG3Zi
"""

# Вводится 5-ти значное двоичное число - сообщение

import numpy as np
from scipy.linalg import hadamard

# Полученное сообщение кодируется кодом RM(1, 4)

def coding(mes):
  G = np.matrix([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1], 
              [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1], 
              [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1], 
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]], dtype = bool)
  
  recieved = [True, True, True, True, True]
  for j in range(5) :
    if (mes[j] == '0') :
      recieved[j] = False
  coded_message = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype = bool)
  
  for i in range(16) :
    x = np.logical_xor(np.logical_and(recieved[0], G[0, i]), np.logical_and(recieved[1], G[1, i]))
    for j in range(2, 5) :
      x = np.logical_xor(x, np.logical_and(recieved[j], G[j, i]))
    coded_message[i] = x
  
  coded = '0000000000000000'
  for i in range(16) :
    if(coded_message[i] == True) :
      coded = coded[:i] + '1' + coded[i + 1 :]

  print('Закодированное сообщение:', coded)
  return coded

# Вводится помеха в одном случайном бите

def breaking(mes):
  broken = mes
  z = np.random.randint(0, 15)
  print('Помеха в ', z + 1, '-м бите') 
  if (broken[z] == '0') :
    broken = broken[:z] + '1' + broken[z + 1 :]
  else :
    broken = broken[:z] + '0' + broken[z + 1 :]
  
  print('Закодированное сообщение после передачи:', broken)
  return broken

# Исправление ошибки

def fix_and_decoding(mes) :
  coded_message = mes

  Y = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
  for i in range(16):
    if (coded_message[i] == '0') :
      Y[i] = -1
  
  YH = np.matmul(Y, hadamard(16))
  max = YH[0]
  imax = 0
  for i in range(1, 16) : 
    if (abs(YH[i]) > abs(max)) : 
      max = YH[i]
      imax = i

  fixed_message = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype = bool)

  if (max > 0) :
    Am = (np.ones((16,16)) + hadamard(16)) / 2
    for i in range(16) :
      fixed_message[i] = Am[imax, i]
  else :
    Not_Am = np.ones((16,16)) - (np.ones((16,16)) + hadamard(16)) / 2
    for i in range(16) :
      fixed_message[i] = Not_Am[imax, i]

  print('Восстановленное сообщение:', fixed_message*1)

  decoded_message = ''
  decoded_message += str(int(fixed_message[0]))
  decoded_message += str(int(np.logical_xor(fixed_message[0], fixed_message[8])))
  decoded_message += str(int(np.logical_xor(fixed_message[0], fixed_message[4])))
  decoded_message += str(int(np.logical_xor(fixed_message[0], fixed_message[2])))
  decoded_message += str(int(np.logical_xor(fixed_message[0], fixed_message[1])))
  print('Декодированное сообщение:', decoded_message)




f = False
while f == False :
  message = input('Введите сообщение в виде 5 двоичных знаков: ')
  if (len(message) == 5) : 
    checknum = 0
    for i in range(5) :
      if (message[i] == '0') or (message[i] == '1') : 
        checknum += 1
    if (checknum == 5) :
            f = True

print(message)

coded = coding(message)
broken = breaking(coded)
fix_and_decoding(broken)
