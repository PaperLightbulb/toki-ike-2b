class Program:
    def __init__(self, body: []):
        self.body = body

class VarDec:
    def __init__(self, val, constant: bool, ident: str):
        self.constant = constant
        self.ident = ident
        self.val = val

class FxnDec:
    def __init__(self, params, name: str, body):
        self.params = params
        self.name = name
        self.body = body

class IfStmt:
    def __init__(self, qual: bool, body):
        self.qual = qual
        self.body = body

class WhileStmt:
    def __init__(self, qual: bool, body):
        self.qual = qual
        self.body = body

class ForStmt:
    def __init__(self, args, body):
        self.args = args
        self.body = body

class AssignmentExpr:
    def __init__(self, assigne, val):
        self.assigne = assigne
        self.value = val
    
class BinaryExpression:
    def __init__(self, left, right, operator: str):
        self.left = left
        self.right = right
        self.operator = operator

class CallExpression:
    def __init__(self, args, caller):
        self.args = args
        self.caller = caller

class MemberExpression:
    def __init__(self, obj, prop, computed: bool):
        self.obj = obj
        self.prop = prop
        self.computed = computed

class Identifier:
    def __init__(self, sym: str):
        self.symbol = sym

class NumericLiteral:
    def __init__(self, val: float):
        self.value = val

class StringLiteral:
    def __init__(self, val: str):
        self.value = val

class ObjectLiteral:
    def __init__(self, props):
        self.properties = props

class Property:
    def __init__(self, key: str, val):
        self.key = key
        self.value = val

class NotStmt:
    def __init__(self, val):
        self.value = val