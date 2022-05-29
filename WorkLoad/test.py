n_queries = 4
n_attributes = 4
#attribute usage matrix
aum = [[1,0,1,0],[0,1,1,0],[0,1,0,1],[0,0,1,1]]

#number of sites
n_sites = 3 

#access matrix
acc = [[15,5,25,3],[20,0,25,0],[10,0,25,0]]

#prefix sum for each query
pre = [0 for i in range(n_queries)]
for i in range(n_queries):
    for j in range(n_sites):
        pre[i] = pre[i]+acc[j][i]

#attribute affinity matrix
aam = [[0 for i in range(n_attributes)] for j in range(n_attributes)]

#calculation of the aam
for i in range(n_attributes):
    for j in range(n_attributes):
#         if(i==j):
#             aam[i][j]=0
#             continue
        for q in range(n_queries):
            if aum[q][i]==1 and aum[q][j]==1:
                aam[i][j] = aam[i][j]+pre[q]
          
print("Attribute affinity matrix")
for i in range(n_attributes):
    print(aam[i])
print("Access Site Sums")
print(pre)

def bond(Ax,Ay):
    if Ax==-1 or Ay==-1:
        return 0
    ans = 0
    for i in range(n_attributes):
        ans = ans + (aam[i][Ax]*aam[i][Ay])
    return ans

def cont(Ai,Ak,Aj):
    print("bond ",Ai, "bond", Ak, " = ", bond(Ai,Ak))
    print("bond ",Ak, "bond", Aj, " = ", bond(Ak,Aj))
    print("bond ",Ai, "bond", Aj, " = ", bond(Ai,Aj))
    return 2*bond(Ai,Ak) + 2*bond(Ak,Aj) - 2*bond(Ai,Aj)

def BEA():
    ca = []
    ca.append(0)
    ca.append(1)
    index  = 2
    while index < n_attributes:
        maxi = -1 
        maxc = -100000
        for i in range(1,index):
                con = cont(ca[i-1],index,ca[i])
                print("Index ", i+1, " ", "cont ", ca[i],index+1,ca[i]+1, con)
                if con > maxc:
                    maxi = i
                    maxc = con
        #boundary left
        con = cont(-1,index,ca[0])
        print("Index ", i+1, " ", "cont ", 1,index+1,ca[0]+1, con)
        if con > maxc:
            maxi = 0
            maxc = con
        #boundary right
        con = cont(ca[index-1],index,-1)
        print("Index ", i+1, " ", "cont ", ca[index-1]+1,index+1,index+2, con)
        if con > maxc:
            maxi = index
        if maxi==index:
            ca.append(index)    
        else:
            ca.append(0)
            for j in range(index,maxi,-1):
                ca[j]=ca[j-1]
            ca[maxi] = index
        print(ca)
        index = index + 1
    print("FINAL Clustered Affinity Matrix")
    print(ca)
    return ca
CA = BEA()
ca = [[0 for i in range(n_attributes)] for j in range(n_attributes)]
for i in range(n_attributes):
    for j in range(n_attributes):
        ca[i][j] = aam[CA[i]][CA[j]]

print(ca)


def shift_row(mat):
    row_first=[]
    for i in range(n_attributes):
        row_first.append(mat[0][i])
    for i in range(1,n_attributes):
        for j in range(n_attributes):
            mat[i-1][j]=mat[i][j]
    for i in range(n_attributes):
        mat[n_attributes-1][i]=row_first[i]
   # print(row_first)
    return mat
   
def shift_column(mat):
    col_first=[]
    for i in range(n_attributes):
        col_first.append(mat[i][0])
    for i in range(n_attributes):
        for j in range(1,n_attributes):
            mat[i][j-1]=mat[i][j]
    for i in range(n_attributes):
        mat[i][n_attributes-1]=col_first[i]
    return mat

start=n_attributes-2
aum = [[1,0,1,0],[0,1,0,1],[0,1,1,0],[0,0,1,1]]
AQ=[]
for i in range(n_attributes):
    row=[]
    for j in range(n_attributes):
        if aum[i][j]==1:
            row.append(j)
    AQ.append(row)

print(AQ)

TQ=[]
BQ=[]
OQ=[]

for i in range(n_queries):
    if AQ[i][1] <= start:
        TQ.append(i)
    elif AQ[i][0] > start:
        BQ.append(i)
    else:
        OQ.append(i)

    
print(TQ)
print(BQ)
print(OQ)

CTQ=0
CBQ=0
COQ=0

for i in range(len(TQ)):
    CTQ=CTQ+pre[TQ[i]]
for i in range(len(BQ)):
    CBQ=CBQ+pre[BQ[i]]
for i in range(len(OQ)):
    COQ=COQ+pre[OQ[i]]
best=CTQ*CBQ-COQ*COQ


shift=0
for i in range(4):
    for j in range(n_attributes-3,0,-1):
        TQ=[]
        BQ=[]
        OQ=[]

        for k in range(n_queries):
            if AQ[k][1] <= j:
                TQ.append(i)
            elif AQ[k][0] > j:
                BQ.append(k)
            else:
                OQ.append(k)
        CTQ=0
        CBQ=0
        COQ=0
        
        for k in range(len(TQ)):
            CTQ=CTQ+pre[TQ[k]]
        for k in range(len(BQ)):
            CBQ=CBQ+pre[BQ[k]]
        for k in range(len(OQ)):
            COQ=COQ+pre[OQ[k]]
        z=CTQ*CBQ-COQ*COQ
        if z>best:
            best=z
            start=j
            shift=i
    shift_row(ca)
    shift_column(ca)
    shift_row(aum)
    shift_column(aum)
    AQ=[]
    for i in range(n_attributes):
        row=[]
        for j in range(n_attributes):
            if aum[i][j]==1:
                row.append(j)
        AQ.append(row)
last=n_attributes-1
for i in range(shift):
    ele=CA[last]
    for j in range(last,1,-1):
        CA[j]=CA[j-1]
    CA[0]=ele
F1={1}
F2={1}
print("First Half")
for i in range(0,start):
    F1.add(CA[i]+1)
print(F1)    
print("Second Half")

for i in range(start,n_attributes):
    F2.add(CA[i]+1)
print(F2)  
print("Split is:")  
print(start)
print("Shift is")
print(shift)