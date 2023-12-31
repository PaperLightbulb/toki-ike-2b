from runtime.values import *
from inspect import isfunction
from frontend.ast import *
import time

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
        return value
    
    def declareFxn(self, name, params, decEnv, body):
        fn = FxnVal(name, params, decEnv, body)
        return decEnv.declareVar(name, fn, True)
    
    def assignVar(self, varName, value):
        env = self.resolve(varName)
        if varName in env.consts:
            raise ValueError("Cannot reassign constant: ", varName)
        env.vars[varName] = value
        return value
    
    def getRoot(self, memEx):
        if memEx.obj != MemberExpression:
            return memEx.obj
        return self.getRoot(memEx.obj)
    
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
    env.declareVar("a", BoolVal(True), True)
    env.declareVar("powe", BoolVal(False), True)
    env.declareVar("ala", NullVal(), True)

    env.declareVar("toki", NativeFxnVal(FxnCall(prnList, env)), True)
    env.declareVar("kute", NativeFxnVal(FxnCall(inpt, env)), True)
    env.declareVar("kulupu", NativeFxnVal(FxnCall(concatStr, env)), True)
    env.declareVar("tenpo", NativeFxnVal(FxnCall(delay, env)), True)

    return env

def delay(args, env):
    val = args[0]
    if type(val) == NumVal:
        if val.value == 0:
            input()
        elif val.value < 0:
            raise ValueError("cannot delay for negative time")
        else:
            time.sleep(val.value)
    elif type(val) == BoolVal:
        input()
    else:
        raise ValueError("Cannot delay for non numeric or boolean value")

def prnList(args, env):
    for i in args:
        out = i
        if isfunction(out):
            out = out(args)
        
        if type(out) == NumVal:
            print(out.value, end="")
        elif type(out) == StringVal:
            print(out.value, end="")
        elif type(out) == BoolVal:
            print(str(out.value).lower(), end="")
        elif type(out) == NullVal:
            print("ala", end="")
        else:
            print(out, end="")
    print()
    return NullVal()

def inpt(args, env):
    inpt = input(args[0].value)
    if is_float(inpt):
        return NumVal(float(inpt))
    return StringVal(inpt)

def concatStr(args, env):
    out = ""
    for s in args:
        if isfunction(s):
            s = s(args)

        if type(s) == StringVal:
            out += s.value
        else:
            print("Cannot concat non string value")
    
    return StringVal(out)

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False