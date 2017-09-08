colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

p = [];
for i in range(len(colors)):
    p.append([])

initProb = 1.0/(len(colors)*len(colors[0]))

#init probability uniform
for i in range(len(p)):
    for j in range(len(colors[0])):
        p[i].append(initProb)

pHit = sensor_right
pMiss = 1.0 - pHit
pMove = p_move
pStay = 1.0 - pMove

def sense(p, Z):
    q = []
    for i in range(len(p)):
        q.append([])#create new row
        for j in range(len(p[i])):
            hit = (Z == colors[i][j])
            q[i].append(p[i][j] * (hit * pHit + (1 - hit) * pMiss))
    s = 0
    for i in range(len(q)):
        s+= sum(q[i])

    for i in range(len(q)):
        for j in range(len(q[i])):
            if q[i][j] != 0:
                q[i][j] = q[i][j] / s
    return q

def move(p, V,U):
    q = []
    for i in range(len(p)):
        q.append([])#create new row
        for j in range(len(p[i])):
            s = pMove * p[(i - V) % len(p)][(j - U) % len(p[i])]
            s = s + pStay * p[i][j]
            q[i].append(s)
    return q


for k in range(len(measurements)):

   p = move(p, motions[k][0], motions[k][1])
   p = sense(p, measurements[k])


#Your probability array must be printed
#with the following code.

show(p)




