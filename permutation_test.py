# ==================================================
# 1. 라이브러리 및 입력값 설정
# ==================================================
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

R = int(input())
C = int(input())

# ==================================================
# 2. 관측도수 분할표 구성
# ==================================================
F = np.zeros((C+1,R+1))

for i in range(1,C+1) :
    for j in range(1,R+1) :
        F[i,j] = int(input())

for i in range(1,R+1) :                
    F[0,i] = F.sum(axis=0)[i]
for i in range(1,C+1) :
    F[i,0] = F.sum(axis=1)[i]
F[0,0] = F.sum()/3                                    

# ==================================================
# 3. 기대도수 계산
# ==================================================
E = np.zeros((C,R))
for i in range(1,R+1) :
    for j in range(1,C+1) :
        E[j-1,i-1] = F[0,i]*F[j,0]/F[0,0]

# ==================================================
# 4. 순열검정을 위한 데이터 구성
# ==================================================
N=[]

for i in range(C) :
    for j in range(int(F[i+1,0])) :
        N.append(f"{i+1}")
A=[]

for i in range(R) :
    for j in range(int(F[0,i+1])) :
        A.append(f"{i+1}")

a=sorted(list(set(A)))

# ==================================================
# 5. Permutation을 이용한 검정통계량의 귀무분포 생성
# ==================================================
result=[]
for i in range(100000) :
    P = (np.random.permutation(N))
    U = np.zeros((C,R))
    r=0
    for j in a:
        count=Counter(P[r:r+A.count(j)])
        r+=A.count(j)
        for key,value in count.items():
            U[int(key)-1, int(j)-1]=value
    z=0
    for m in range(C):
        for n in range(R):
            z+=(U[m,n]-E[m,n])**2/E[m,n]
    result.append(z)    

plt.hist(result,color='red',bins=50,density=True)
plt.show()

# ==================================================
# 6. Permutation 분포와 카이제곱 분포 비교
# ==================================================
from scipy.stats import chi2

xx=np.arange(0,max(result),0.2)
plt.plot(xx,chi2.pdf(xx, df=(C-1)*(R-1)))
plt.hist(result,color='red',bins=50,density=True,alpha=0.3)
plt.plot(xx,chi2.pdf(xx, df=(C-1)*(R-1)))
plt.show()

# ==================================================
# 7. 관측 검정통계량 및 P-value 계산
# ==================================================
z=0
for i in range(C):
    for j in range(R):
        z+=(F[i+1,j+1]-E[i,j])**2/E[i,j]

over_number = 0  
for i in range(len(result)) :
    if z < result[i] :
        over_number += 1
P_value = over_number / 100000

# ==================================================
# 8. 독립성 검정 결과 출력
# ==================================================
if P_value < 0.05 :
    print(f"검정을 통해 구한 P-값이 {P_value}(으)로 매우 작은 값이므로, 독립이 아니다.")

else :
    print(f"검정을 통해 구한 P-값이 {P_value}(으)로 0.05보다 큰 값을 가지므로, 독립이다.")