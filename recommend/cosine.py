from numpy import *
vector1 = ones(4)
vector2 = [3,3,6,8]
print max(vector1)
cosV12 = dot(vector1,vector2)/(linalg.norm(vector1)*linalg.norm(vector2))
print cosV12
