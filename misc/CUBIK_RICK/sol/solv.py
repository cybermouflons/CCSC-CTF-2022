#https://github.com/pglass/cube
## Sistarismeno Writeup apo tratrafe2

from rubik.cube import Cube
from rubik.solve import Solver

## Read file
cube_strs=[]
f = open("RGBYOW.txt", "r")
for line in f:
	line = line.replace("\n","").split(" ")
	line = [x for x in line if x != ""]
	cube_strs.append(line)
cubes_str = "".join(sum(cube_strs, []))

## Initiate two cubes
cube1_str = cubes_str[::2]
cube2_str = cubes_str[1::2]
print(cube1_str)
print(cube2_str)
c1 = Cube(cube1_str)
c2 = Cube(cube2_str)

## Solve the first cube
solver = Solver(c1)
solver.solve()
moves = " ".join(solver.moves) #+" Z" 
# Note: We added the Z rotation to keep the centers steady - This depends on the solver.

## Solve the second cube based on the moves of the first
c2.sequence(moves)
print(c2)

## Derive the solution
sol = c2.__str__().split("\n")
sol = sol[0]+sol[3]+sol[6]+sol[1]+sol[4]+sol[7]+sol[2]+sol[5]+sol[8]
sol = sol.replace(" ","")
print(sol)

