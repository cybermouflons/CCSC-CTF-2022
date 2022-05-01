from boxed import run

def target_func(a,b,c=0):
    return a+b*c

result = run(target_func, args=(1,2), kwargs={"c":3})