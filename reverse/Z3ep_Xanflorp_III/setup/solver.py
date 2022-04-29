import angr
import claripy

#test
project = angr.Project("binary")

#sets the state address of the binary
state = project.factory.blank_state(addr=0x08049251)

x = [ claripy.BVS(f"w{i}",8) for i in range(8) ]
inputs = claripy.Concat(*x)

#sets the ebx
state.regs.ebx = 0x804f000

#sets the eax
state.regs.eax = 0x45

#symbolic weights variable
state.memory.store(0x0804f020,inputs)

#hook function
#the value of ebx is set to one
@project.hook(0x080491bb)
def edit_yoyo(state):
	state.regs.ebx= 0x1


simulation = project.factory.simgr(state)

simulation.explore(find=0x0804c23f,avoid=0x0804c253)

if simulation.found:
	solution_state = simulation.found[0]
	sol = solution_state.solver.eval(inputs,cast_to=bytes)
	print(f"[*]Solution is {sol}")
else:
	raise Exception('Could not find the solution')

