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
    elif type(astNode) == IfStmt:
        return evalIfStmt(astNode, env)
    elif type(astNode) == WhileStmt:
        return evalWhileStmt(astNode, env)
    elif type(astNode) == ForStmt:
        return evalForStmt(astNode, env)
    raise ValueError("Ast node not yet set up for interpritation: " + str(type(astNode)))

def evalPrgrm(program: Program, env):
    lastEval = NullVal()
    for st in program.body:
        lastEval = eval(st, env)
    return lastEval

def evalAssign(node: AssignmentExpr, env):
    if type(node.assigne) != Identifier:
        raise ValueError("invalide asignee")
    
    val = eval(node.value, env)

    varName = node.assigne.symbol

    return env.assignVar(varName, val)

def evalIfStmt(stmt, env):
    b = eval(stmt.qual, env)
    if type(b) == BoolVal:
        if b.value:
            for ex in stmt.body:
                eval(ex, env)
    return NullVal()

def evalWhileStmt(stmt, env):
    while (True):
        b = eval(stmt.qual, env)
        if type(b) == BoolVal:
            if not b.value:
                break
        else:
            break
        for ex in stmt.body:
                eval(ex, env)
    return NullVal()


def evalForStmt(stmt, env):
    e = Environment(env)
    eval(stmt.args[0], e)
    while (True):
        
        cond = eval(stmt.args[1], e)
        if type(cond) == BoolVal:
            if not cond.value:
                break
        else:
            break
        for ex in stmt.body:
            eval(ex, e)
        eval(stmt.args[2], e)
    return NullVal()

def evalBin(binop: BinaryExpression, env):
    left = eval(binop.left, env)
    right = eval(binop.right, env)
    if (type(right) == NumVal and type(left) == NumVal):
        return evalNumBinExpr(left, right, binop.operator)
    if type(right) == BoolVal and type(left) == BoolVal:
        return evalBoolBinExpr(left, right, binop.operator)
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
        args.append(eval(i, env))
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

def evalBoolBinExpr(left, right, operator):
    l = left.value
    r = right.value
    result = False
    if operator == "sama":
        result = l == r
    elif operator == "en":
        result = l and r
    elif operator == "anu":
        result = l or r
    return BoolVal(result)

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
    elif operator == "%":
        result = l % r
    elif operator == "suli":
        result = l > r
    elif operator == "lili":
        result = l < r
    if operator == "sama":
        result = l == r
    if type(result) == bool:
        return BoolVal(result)
    return NumVal(result)