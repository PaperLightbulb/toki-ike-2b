from frontend.parser import *
from runtime.env import *
from runtime.interpriter import *

fl = open("run.txt", "r")
inpt = fl.read()
env = createGlobEnv(None)
parser = Parser(env)
program = parser.produceAst(inpt)
eval(program, env)