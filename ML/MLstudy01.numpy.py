# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Numpy (Numerical Python)

# ## 개요

import numpy as np

# * ndarray

# +
array1 = np.array([1, 2, 3])
print('array1 type:', type(array1))
print('array1 array 형태:', array1.shape)

array2 = np.array([[1, 2, 3],
                   [2, 3, 4]])
print('array2 type:', type(array2))
print('array2 array 형태:', array2.shape)

array3 = np.array([[1, 2, 3]])
print('array3 type:', type(array3))
print('array3 array 형태:', array3.shape)
# -

print('array : {:0}차원, array2: {:1}차원, array3: {:2}차원'.format(array1.ndim,
                                                                 array2.ndim, array3.ndim))

# * ndarray내의 데이터 타입은 같은 데이터 타입만 가능

list1 = [1, 2, 3]
print(type(list1))
array1 = np.array(list1)
print(type(array1))
print(array1, array1.dtype)

#     * 만약 다른 데이터 유형이 섞여있는 리스트를 ndarray로 변경하면 데이터 크기가 더 큰 데이터 타입으로 형 변환을 일괄 적용함

# +
list2 = [1, 2, 'test']
array2 = np.array(list2)
print(array2, array2.dtype) # <U21의 의미는 유니코드 문자열을 뜻한다.

list3 = [1, 2, 3.0]
array3 = np.array(list3)
print(array3, array3.dtype) 
# -

# * astype() : ndarray 내 데이터값의 타입 변경

# +
array_int = np.array([1, 2, 3])
array_float = array_int.astype('float64')
print(array_float, array_float.dtype)

array_int1 = array_int.astype('int32')
print(array_int1, array_int1.dtype)

array_float1 = np.array([1.1, 2.1, 3.1])
array_int2= array_float1.astype('int32')
print(array_int2, array_int2.dtype)
# -

# ## ndarray를 편리하게 생성하기 - arange, zeros, ones

# * arange : 0부터 함수 인자 값 -1까지의 값을 순차적으로 ndarray의 데이터값으로 변환
# * zeros : 튜플 형태의 shape 값을 입력하면 모든 값을 0으로 채운 해당 shape를 가진 ndarray를 반환
# * ones : 튜플 형태의 shape 값을 입력하면 모든 값을 1로 채운 해당 shape를 가진 ndarray를 반환
#     - dtype를 정해주지 않으면 default로 float64 형의 데이터로 ndarray를 채움

sequence_array = np.arange(10)
print(sequence_array)
print(sequence_array.dtype, sequence_array.shape)

# +
zero_array = np.zeros((3,2),dtype='int32')
print(zero_array)
print(zero_array.dtype, zero_array.shape)

one_array = np.ones((3,2))
print(one_array)
print(one_array.dtype, one_array.shape)
# -

# ## ndarray의 차원과 크기를 변경하는 reshape()

# +
array1 = np.arange(10)
print('array1:\n', array1)

array2 = array1.reshape(2,5)
print('array2:\n',array2)

array3 = array1.reshape(5,2)
print('array3:\n',array3)
# -

# * 지정된 사이즈로 변경이 불가능하면 오류

array1.reshape(4,3) 

# * -1을 인자로 사용하면 원래 ndarray와 호환되는 새로운 shape로 변환

# +
array1 = np.arange(10)
print(array1)

array2 = array1.reshape(-1,5)
print('array2 shape:',array2.shape)

array3 = array1.reshape(5,-1)
print('array3 shape:',array3.shape)
# -

# * -1을 사용하더라도 호환될 수 없는 형태는 변환할 수 없음

array1 = np.arange(10)
array4 = array1.reshape(-1,4)

# * reshape(-1, 1) : 여러개의 로우를 가지되 반드시 1개의 칼럼을 가진 ndarray로 변화됨

# +
array1 = np.arange(8)
array3d = array1.reshape((2,2,2))
print('array3d:\n',array3d.tolist())

# 3차원 ndarray를 2차원 ndarray로 변환
array5 = array3d.reshape(-1,1)
print('array5:\n',array5.tolist())
print('array5 shape:',array5.shape)

# 1차원 ndarray를 2차원 ndarray로 변환
array6 = array1.reshape(-1,1)
print('array6:\n',array6.tolist())
print('array6 shape:',array6.shape)
# -

# ## 넘파이의 ndarray의 데이터 세트 선택하기 - 인덱싱 (indexing)

# 1. 특정한 데이터만 추출 : 원하는 위치의 인덱스 값을 지정하면 해당 위치의 데이터가 반환됨.
# 2. 슬라이싱(Slicing) 
# 3. 팬시 인덱싱(Fancy Indexing) : 일정한 인덱싱 집합을 리스트 또는 ndarray 형태로 지정해 해당 위치에 있는 데이터의 ndarray를 반환
# 4. 불린 인덱싱(Boolean Indexing) : 특정 조건에 해당하는지 여뷰인 True/False 값 인덱싱 집합을 기반으로 True에 해당하는 인덱스 위치에 있는 데이터의 ndarray를 반환

# ### 단일 값 추출

array1 = np.arange(start=1, stop=10)
print('array1:',array1)
value = array1[2]
print('value:',value)
print(type(value))

print('맨 뒤의 값:',array1[-1], ', 맨 뒤에서 두번째 값:',array1[-2])

array1[0] = 9
array1[8] = 0
print('array1:',array1)

# * axis 0 : row 방향 축
# * axis 1 : col 방향 축
# * 축 기반 연산에서 axis가 생략되면 axis 0 을 의미

# +
array1d = np.arange(start=1, stop=10)
array2d = array1d.reshape(3,3)
print(array2d)

print('(row=0,col=0) index 가리키는 값:', array2d[0,0] )
print('(row=0,col=1) index 가리키는 값:', array2d[0,1] )
print('(row=1,col=0) index 가리키는 값:', array2d[1,0] )
print('(row=2,col=2) index 가리키는 값:', array2d[2,2] )
# -
# ### 슬라이싱(Slicing)


# * 단일 데이터값 추출을 제외하고 슬라이싱, 팬시 인덱싱, 불린 인덱싱으로 추출된 데이터 세트는 모두 ndarray타입.

# 1. ':'기호 앞에 시작 인덱스를 생략하면 자동으로 맨 처음 인덱스인 0으로 간주합니다.
# 2. ':'기호 뒤에 종료 인덱스를 생략하면 자동으로 맨 마지막 인덱스로 간주합니다.
# 3. ':'기호 앞/뒤에 시작/종료 인덱스를 생략하면 자동으로 맨 처음/맨 마지막 인덱스로 간주합니다.

array1 = np.arange(start=1, stop=10)
array3 = array1[0:3]
print(array3)
print(type(array3))

# +
array1 = np.arange(start=1, stop=10)
array4 = array1[:3]
print(array4)

array5 = array1[3:]
print(array5)

array6 = array1[:]
print(array6)

# +
array1d = np.arange(start=1, stop=10)
array2d = array1d.reshape(3,3)
print('array2d:\n',array2d)

print('array2d[0:2, 0:2] \n', array2d[0:2, 0:2])
print('array2d[1:3, 0:3] \n', array2d[1:3, 0:3])
print('array2d[1:3, :] \n', array2d[1:3, :])
print('array2d[:, :] \n', array2d[:, :])
print('array2d[:2, 1:] \n', array2d[:2, 1:])
print('array2d[:2, 0] \n', array2d[:2, 0])
# -

# * 2차원 ndarray 뒤에 오는 인덱스를 없애면 1차원 ndarray를 반환함.

print(array2d[0]) # 첫 번째 로우 ndarray를 반환
print(array2d[1])
print('array2d[0] shape:', array2d[0].shape, 'array2d[1] shape:', array2d[1].shape )

# ### 팬시 인덱싱 (Fancy Indexing)

# * 리스트나 ndarray로 인덱스 집합을 지정하면 해당 위치의 인덱스에 해당하는 ndarray를 반환하는 인덱싱 방식

# +
array1d = np.arange(start=1, stop=10)
array2d = array1d.reshape(3,3)

array3 = array2d[[0,1], 2]
print('array2d[[0,1], 2] => ',array3.tolist())

array4 = array2d[[0,1], 0:2]
print('array2d[[0,1], 0:2] => ',array4.tolist())

array5 = array2d[[0,1]]
print('array2d[[0,1]] => ',array5.tolist())
# -

# ### 불린 인덱싱

# * 불린 인덱싱이 동작하는 단계
# <br>
# <br>
# - Step1 : array1d > 5와 같이 ndarray의 필터링 조건을 [] 안에 기재
# - Step2 : False 값은 무시하고 True 값에 해당하는 인덱스값만 저장(유의해야 할 사항은 True값 자체인 1을 저장하는 것이 아니라 True값을 가진 인덱스를 저장한다는 것)
# - Step3 : 저장된 읻게스 데이터 세트로 ndarray조회

array1d = np.arange(start=1, stop=10)
array3 = array1d[array1d > 5]
print('array1d > 5 불린 인덱싱 결과 값 :', array3)

array1d > 5

boolean_indexes = np.array([False, False, False, False, False,  True,  True,  True,  True])
array3 = array1d[boolean_indexes]
print('불린 인덱스로 필터링 결과 :', array3)

indexes = np.array([5,6,7,8])
array4 = array1d[ indexes ]
print('일반 인덱스로 필터링 결과 :',array4)

# ## 행렬의 정렬 - sort()와 argsort()

# ### 행렬 정렬

# * np.sort() : 원 행렬은 그대로 유지한 채 원 행렬의 정렬된 행렬을 반환.
# * ndarray.sort() : 원 행렬 자체를 정렬한 형태로 변환하며 반 값은 None

org_array = np.array([ 3, 1, 9, 5]) 
print('원본 행렬:', org_array)
# np.sort( )로 정렬 
sort_array1 = np.sort(org_array)         
print ('np.sort( ) 호출 후 반환된 정렬 행렬:', sort_array1) 
print('np.sort( ) 호출 후 원본 행렬:', org_array)
# ndarray.sort( )로 정렬
sort_array2 = org_array.sort()
print('org_array.sort( ) 호출 후 반환된 행렬:', sort_array2)
print('org_array.sort( ) 호출 후 원본 행렬:', org_array)

# * 내림차순 정렬 : np.sort()[::-1]

sort_array1_desc = np.sort(org_array)[::-1]
print ('내림차순으로 정렬:', sort_array1_desc) 

# +
array2d = np.array([[8, 12], 
                   [7, 1 ]])

sort_array2d_axis0 = np.sort(array2d, axis=0)
print('로우 방향으로 정렬:\n', sort_array2d_axis0)

sort_array2d_axis1 = np.sort(array2d, axis=1)
print('컬럼 방향으로 정렬:\n', sort_array2d_axis1)
# -

# ### 정렬된 행렬의 인덱스 반환하기

# * np.argsort() 
#     - 원본 행렬이 정렬되었을 때 기존 원본 행렬의 원소에 대한 인덱스를 필요로 할 때 np.argsort()를 이용
#     - np.argsort()는 정렬 행렬의 원본 행렬 인덱스를 ndarray 형으로 반환

org_array = np.array([ 3, 1, 9, 5]) 
sort_indices = np.argsort(org_array)
print(type(sort_indices))
print('행렬 정렬 시 원본 행렬의 인덱스:', sort_indices)

org_array = np.array([ 3, 1, 9, 5]) 
sort_indices_desc = np.argsort(org_array)[::-1]
print('행렬 내림차순 정렬 시 원본 행렬의 인덱스:', sort_indices_desc)

# ## 선형대수 연산 - 행렬 내적과 전치 행렬 구하기

# ### 행렬 내적(행렬 곱)

# +
A = np.array([[1, 2, 3],
              [4, 5, 6]])
B = np.array([[7, 8],
              [9, 10],
              [11, 12]])

dot_product = np.dot(A, B)
print('행렬 내적 결과:\n', dot_product)
# -

# ### 전치 행렬

A = np.array([[1, 2],
              [3, 4]])
transpose_mat = np.transpose(A)
print('A의 전치 행렬:\n', transpose_mat)
