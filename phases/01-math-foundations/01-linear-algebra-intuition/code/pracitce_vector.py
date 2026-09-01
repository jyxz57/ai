import math

class vector:
    def __init__(self,components):
        self.components = list(components)
    def __len__(self):
        return len(self.components)
    def __add__(self,other):
        result=[]
        for a,b in zip(self.components,other.components):
            result.append(a+b)
        return vector(result)
    def __sub__(self,other):
        return vector([a-b for a,b in zip(self.components,other.components)])
    def __mul__(self,scalar):
        return vector([x * scalar for x in self.components])
    def dot(self,other):
        return sum(a * b for a,b in zip(self.components,other.components))
    def magnitude(self):
        return sum(x**2 for x in self.components)**0.5
    def normalize(self):
        mag=self.magnitude()
        return vector([round(x/mag,6) for x in self.components])
    def cossine(self,other):
        return self.dot(other)/(self.magnitude()*other.magnitude())
    def angle(self,other):
        cos_theta=self.cossine(other)
        return math.degrees(math.acos(cos_theta))
    def projection(self,other):
        scalar=self.dot(other)/other.dot(other)
        return vector(x*scalar for x in self.components)
    def __str__(self):
        return str(self.components)
          

class matrix:
    def __init__(self,components):
        self.rows=[vector(row) for row in components]
        self.row_count=len(self.rows)
        self.col_count=len(self.rows[0])
    def __add__(self,other):
        result=[]
        for a,b in zip(self.rows,other.rows):
            result.append((a+b).components)
        return matrix(result)
    def __mul__(self,scalar):
        return matrix((row*scalar).components for row in self.rows)
    def __matmul__(self, other):
        if isinstance(other,vector):
            return vector([sum(self.rows[i].components[j]*other.components[j] for j in range(self.col_count)) for i in range(self.row_count)])
        result=[]
        for i in range(self.row_count):
            result_row=[]
            for k in range(other.row_count):
                total=0
                for j in range(self.col_count):
                    total+=(self.rows[i].components[j]*other.rows[j].components[k])
                result_row.append(total)
            result.append(result_row)
        return matrix(result)
    def transpose(self):
        result=[]
        for j in range(self.col_count):
            result_row=[]
            for i in range(self.row_count):
                result_row.append(self.rows[i].components[j])
            result.append(result_row)
        return matrix(result)
    def rank(self):
        copyrow=[row.components[:] for row in self.rows]
        rank=0
        for j in range(self.col_count):
            pivot=None
            for i in range(rank,self.row_count):
                if(abs(copyrow[i][j])>1e-9):
                    pivot=i
                    break
            if pivot is None:
                continue
            copyrow[rank],copyrow[pivot]=copyrow[pivot],copyrow[rank]
            for i in range(rank+1,self.row_count):
                scale=copyrow[i][j]/copyrow[rank][j]
                delrow=[x*scale for x in copyrow[rank]]
                copyrow[i]=[a-b for a,b in zip(copyrow[i],delrow)]
            rank+=1
        return rank
    def __str__(self):
        return str([row.components for row in self.rows])
            




if __name__=="__main__":
    v1 = vector([1,2,3])
    v2 = vector([4,5,6])
    v3=vector([1,1])
    v4=vector([1,0])
    print(f"v1+v2={v1+v2}")
    print(f"v1-v2={v1-v2}")
    print(f"v1*2={v1*2}")
    print(f"v1*v2={v1.dot(v2)}")
    print(f"{v1.normalize()}")
    print(f"{v1.cossine(v2)}")
    print(f"theta={v1.angle(v2)}")
    print(f"projection={v3.projection(v4)}")
    m1=matrix([[1,2],[3,4]])
    m2=matrix([[4,5],[5,6]])
    print(f"m1+m2={m1+m2}")
    print(f"m1*2={m1*2}")
    print(f"m1*m2={m1 @ m2}")
    print(f"m1*v3={m1@v3}")
    print(f"m1的转置矩阵={m1.transpose()}")
    print(f"m1的秩={m1.rank()}")
    m3=matrix([[1,2],[2,4]])
    m4=matrix([[1,0],[0,1]])
    print(f"m3的秩={m3.rank()}")