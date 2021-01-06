if __name__=='__main__':
    G1 = np.array([[0,0,1,0,0],
                  [0,1,2,1,0],
                  [1,2,-16,2,1],
                  [0,1,2,1,0],
                  [0,0,1,0,0]]
        )
    G2 = np.array([[1,1,1,1,1],
                  [1,1,1,1,1],
                  [1,1,-24,1,1],
                  [1,1,1,1,1],
                  [1,1,1,1,1]]
        )
    
    numr = 0
    denr = 0
    for u in range(-2,3,1):
        for v in range(-2,3,1):
            numr += G1[u+2,v+2]*(u**2+v**2)
            denr += (u**2+v**2)**2
    
    print(numr/denr)
    
    numr = 0
    denr = 0
    for u in range(-2,3,1):
        for v in range(-2,3,1):
            numr += G2[u+2,v+2]*(u**2+v**2)
            denr += (u**2+v**2)**2
    
    print(numr/denr)    
    
    