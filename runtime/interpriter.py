from frontend.ast import *
from runtime.values import *
from runtime.env import *
from frontend.ast import *
from frontend.lexer import *

def eval(astNode, env: Environment):
    if type(astNode) == NumericLiteral:
        return NumVal(astNode.value)
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
    return env.vars[ident.symbol]

def evalVarDec(dec, env):
    return env.declareVar(dec.ident, eval(dec.val, env), dec.constant)

def evalCallExpr(expr: CallExpression, env):
    args = []
    for i in expr.args:
        args.insert(0, eval(i, env))
    fn = eval(expr.calle, env)

    if type(fn) == NativeFxnVal:
        result = fn.call.args(args, env)
        return result
    elif type(fn) == FxnVal:
        scope = Environment(fn.decEnv)
        for i in range(0, len(fn.params) -1):
            varName = fn.params[i]
            scope.declareVar(varName, args[i], False)
        result = NullVal()
        for stmt in fn.body:
            result = eval(stmt, scope)
        return result
    raise ValueError("cannot call non fxn val")

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