from frontend.parser import *
from runtime.env import *
from runtime.interpriter import *
print("lipu li seme?")
fl = open(input() + ".ike", "r")
inpt = fl.read()
env = createGlobEnv(None)
parser = Parser(env)
program = parser.produceAst(inpt)
eval(program, env)