from unittest import result
from joblib import PrintTime
import numpy as np
from itertools import permutations 
import Configuration
from Utils.DataStructures import DataStructures
from Helper.Helper import Helper
import numpy as np

columns=Helper.get_workloads()
# ["name","surname","age","phone","website"]
DS=DataStructures(columns)


aum= DS.generate_attribute_usage_matrix(columns)
print(aum)

a=DS.generate_attribute_affinity_matrix(aum)
# affinity_matrix 

# a = np.array([[60, 0, 45, 60], [0,50,50,10], [45, 50, 95, 55], [60, 10, 55, 70]])

print('Affinity Matrix: \n', a, '\n')

def bond(a_x, a_y):
  return 2 * sum(a_x * a_y)

dim = a.shape[0]

permutations = list(permutations(range(dim))) 
print("This step is passed")
best_score = 0
best = None
for p in permutations:
  bond_energy = []
  for i in range(dim-1):
    bond_energy += [bond(a[:,[p[i]]],a[:,[p[i+1]]])]
    
  if sum(bond_energy) > best_score: 
    best_score = sum(bond_energy); best = p

print("test")
permutation =best  #[0, 2,1,3]

idx = np.empty_like(permutation)
idx[permutation] = np.arange(len(permutation))
a[:] = a[:, idx]
a[:]=a[idx,:]

def partitioning(matrix,point):
    QI=0
    QU=0
    QL=0
    Sum=0
    
    length=len(matrix)

    for i in range(length):
        for j in range(length):
            Sum+=matrix[i,j]
            if i<point and j<point:
                QU+=matrix[i,j]
            
            if i>=point and j>=point:
                QL+=matrix[i,j]

    
    QI=Sum-(QL+QU)
    return (QU*QL)-np.power(QI,2)

for level in range(Configuration.PARTITIONING):
  p=1
  length=a.shape[0]
  for p in range(length):
    Z=partitioning(a,p)
    if Z<0:
      break

  matrix=np.zeros((p,p))
  for i in range(p):
    for j in range(p):
      matrix[i,j]=a[i,j]
  print("Point is :",p)
  a=matrix

print(a)

