from unittest import result
from joblib import PrintTime
import numpy as np
from itertools import permutations 

# affinity_matrix 

a=np.array([
    [45,0,45,0]
    ,[0,80,5,75]
    ,[45,5,53,3]
    ,[0,75,3,78]
])

# a = np.array([[60, 0, 45, 60], [0,50,50,10], [45, 50, 95, 55], [60, 10, 55, 70]])

print('Affinity Matrix: \n', a, '\n')

def bond(a_x, a_y):
  return 2 * sum(a_x * a_y)

dim = a.shape[0]


permutations = list(permutations(range(dim))) 


best_score = 0
best = None

for p in permutations:
  bond_energy = []
  for i in range(dim-1):
    bond_energy += [bond(a[:,[p[i]]],a[:,[p[i+1]]])]
  
  if sum(bond_energy) > best_score: 
    best_score = sum(bond_energy); best = p


permutation = [0, 2,1,3]

idx = np.empty_like(permutation)
idx[permutation] = np.arange(len(permutation))
a[:] = a[:, idx]
a[:]=a[idx,:]
print(a)

print('\n')
print('Best Order:', best, 'Highest Bond Energy', best_score)


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
    print("QU: ",QU)
    print("QL",QL)
    print("QI",QI)
    return (QU*QL)-np.power(QI,2)

print(partitioning(a,3))

# 80 column you defined variable how many iteration should run

