from frontend.ast import *
from runtime.values import *
from runtime.env import *
from frontend.ast import *
from frontend.lexer import *

def eval(astNode, env: Environment):
    if type(astNode) == NumericLiteral:
        return NumVal(astNode.value)
    elif type(astNode) == StringLiteral:
        return StringVal(astNode.value)
    elif type(astNode) == BinaryExpression:
        return evalBin(astNode, env)
    elif type(astNode) == Program:
        return evalPrgrm(astNode, env)
    elif type(astNode) == VarDec:
        return NumVal(evalVarDec(astNode, env))
    elif type(astNode) == AssignmentExpr:
        return evalAssign(astNode, env)
    elif type(astNode) == CallExpression:
        return evalCallExpr(astNode, env)
    elif type(astNode) == Identifier:
        return evalIdent(astNode, env)
    elif type(astNode) == FxnDec:
        return evalFxnDec(astNode, env)
    elif type(astNode) == ObjectLiteral:
        return evalObjExpr(astNode, env)
    elif type(astNode) == MemberExpression:
        return evalMemExpr(astNode, env)
    raise ValueError("Ast node not yet set up for interpritation: " + str(type(astNode)))

def evalPrgrm(program: Program, env):
    lastEval = NullVal()
    for st in program.body:
        lastEval = eval(st, env)
    return lastEval

def evalAssign(node: AssignmentExpr, env):
    if type(node.assigne) != Identifier:
        raise ValueError("invalide asignee")
    
    varName = node.assigne.symbol

    val = eval(node.value, env)
    return env.assignVar(varName, val)

def evalBin(binop: BinaryExpression, env):
    left = eval(binop.left, env)
    right = eval(binop.right, env)
    if (type(right) == NumVal and type(left) == NumVal):
        return evalNumBinExpr(left, right, binop.operator)
    return NullVal()

def evalIdent(ident, env):
    return env.lookUpVar(ident.symbol)

def evalVarDec(dec: VarDec, env):
    return env.declareVar(dec.ident, eval(dec.val, env), dec.constant)

def evalFxnDec(dec: FxnDec, env):
    return env.declareFxn(dec.name.value, dec.params, env, dec.body)

def evalObjExpr(obj: ObjectLiteral, env):
    object = ObjVal({})

    for p in obj.properties:
        value = obj.properties[p]
        if value == None:
            runtimeVal = env.lookUpVar(p)
        else:
            runtimeVal = eval(value, env)

        object.prop[p] = runtimeVal
    
    return object

def evalCallExpr(expr: CallExpression, env):
    args = []
    for i in expr.args:
        args.insert(0, eval(i, env))
    fn = eval(expr.caller, env)

    if type(fn) == NativeFxnVal:
        result = fn.call.args(args, env)
        return result
    elif type(fn) == FxnVal:
        scope = Environment(fn.decEnv)
        for i in range(0, len(fn.params)):
            varName = fn.params[i]
            scope.declareVar(varName, args[i], False)
        result = NullVal()
        for stmt in fn.body:
            result = eval(stmt, scope)
        return result.value
    raise ValueError("cannot call non fxn val: ", type(fn), " ", fn.value)

def evalMemExpr(expr: MemberExpression, env):
    if type(expr.obj) != MemberExpression:
        return env.lookUpVar(expr.obj.symbol).prop[expr.prop.symbol]
    return evalMemExpr(expr.obj, env).prop[expr.prop.symbol]

def evalNumBinExpr(left, right, operator):
    l = float(left.value)
    r = float(right.value)
    result = 0
    if operator == "+":
        result = l + r
    elif operator == "-":
        result = l - r
    elif operator == "*":
        result = l * r
    elif operator == "/":
        result = l / r
    else:
        result = l % r
    return NumVal(result)