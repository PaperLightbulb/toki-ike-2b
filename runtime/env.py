from runtime.values import *
from inspect import isfunction
from frontend.ast import *

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
    
    def tracePath(self, expr):
        path = []
        e = expr
        while type(e) == MemberExpression:
            path.insert(0, e.prop.symbol)
            e = e.obj
        path.insert(0, e.symbol)
        return path
    
    def assignMem(self, memEx, value):
        path = self.tracePath(memEx)
        env = self.resolve(path[0])
        if path[0] in env.consts:
            raise ValueError("Cannot reassign constant: ", path[0])
        obj = env.vars[path[0]]

        self.assignVar(path[0], self.makeObj(path, obj, value))
    
    def makeObj(self, path, obj, value):
        path.pop(0)
        obj.path = value
    
    def getRoot(self, memEx):
        if memEx.obj != memEx:
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

    return env

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