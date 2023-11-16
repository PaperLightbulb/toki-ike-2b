from runtime.values import *
from inspect import isfunction

class Environment:
    def __init__(self, parent):
        if parent == None:
            self.glob = True
        else:
            self.glob = False
        self.parent = parent
        self.vars = {}
        self.consts = {}

    def declareVar(self, varName, value, constant):
        if varName in self.vars:
            raise ValueError("Cannot create already created var: ", varName)
        self.vars[varName] = value
        if constant:
            self.consts[varName] = True
        print(varName, " = ", value)
        return value
    
    def assignVar(self, varName, value):
        env = self.resolve(varName)
        if varName in env.constants:
            raise ValueError("Cannot reassign constant: ", varName)
        env.vars[varName] = value
        print(varName, " = ", value)
        return value
    
    def lookUpVar(self, varName):
        env = self.resolve(varName)
        return env.vars[varName]
    
    def resolve (self, varName):
        if varName in self.vars:
            return self
        if not self.parent:
            raise ValueError("Cannot resolve variable as it does not exist: ", varName)
        return self.parent.resolve(varName)

def createGlobEnv(parent):
    env = Environment(parent)
    env.declareVar("true", BoolVal(True), True)
    env.declareVar("false", BoolVal(False), True)
    env.declareVar("null", NullVal(), True)

    env.declareVar("toki", NativeFxnVal(FxnCall(prnList, env)), True)
    env.declareVar("kute", NativeFxnVal(FxnCall(inpt, env)), True)

    return env

def prnList(args, env):
    for i in args:
        if isfunction(i):
            print(i(args))
        if type(i) == NumVal:
            print(i.value, end="")
        else:
            print(i, end="")
    print()
    return NullVal()

def inpt(args, env):
    return NumVal(float(input(args[0].value)))