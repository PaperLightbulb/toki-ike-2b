from frontend.lexer import *
from frontend.ast import *
from runtime.values import *

class Parser:
    def __init__(self, env):
        self.tokens = []
        self.env = env

    def notEof(self):
        return self.at().type != TokenType.EOF

    def at(self):
        return self.tokens[0]

    def eat(self):
        return self.tokens.pop(0)
    
    def expect(self, type, err):
        prev = self.eat()

        if not ('prev' in locals() or 'prev' in globals()) or prev.type != type:
            raise ValueError(err)
        return prev
    
    def produceAst(self, sourceCode):
        self.tokens = tokenize(sourceCode)

        prgrm = Program([])

        while self.notEof():
            prgrm.body.append(self.parseStmt())

        return prgrm
    
    def parseStmt(self):
        if self.at().type == TokenType.LET or self.at().type == TokenType.CONST:
            return self.parseVarDec()
        elif self.at().type == TokenType.FN:
            return self.parseFnDec()
        return self.parseExpression()
    
    def parseExpression(self):
        return self.parseAssignmentExpr()
    
    def parseAssignmentExpr(self):
        left = self.parseObjExpr()
        if self.at().type == TokenType.EQUALS:
            self.eat()
            val = self.parseAssignmentExpr()
            return AssignmentExpr(left, val)
        return left
    
    def parseObjExpr(self):
        if self.at().type != TokenType.OPENBRACE:
            return self.parseAdditive()
        self.eat()
        props = {}
        while self.notEof() and self.at().type != TokenType.CLOSEBRACE:
            key = self.expect(TokenType.IDENTIFIER, "obj literal key expected").value
            if self.at().type == TokenType.COMMA:
                self.eat()
                props[key] = NullVal()
            elif self.at().type == TokenType.CLOSEBRACE:
                props[key] = NullVal()
            else:
                self.expect(TokenType.COLON, "Expected colon in object")
                val = self.parseExpression()
                props[key] = val
                if self.at().type != TokenType.CLOSEBRACE:
                    self.expect(TokenType.COMMA, "Expected comma or closing brace in object")
        self.expect(TokenType.CLOSEBRACE, "Object is missing closing brace")
        return ObjectLiteral(props)
    
    
    def parseFxnDec(self):
        self.eat()
        name = self.expect(TokenType.IDENTIFIER, "expected identifier following fn")
        args = self.parseArgs()
        params = []
        for i in args:
            if type(i) != Identifier:
                raise ValueError("inside fxn dec params not of type str")
            params.insert(0,i.symbol)
        self.expect(TokenType.OPENBRACE, "expected fn body followin fn dec")

        body = []
        while self.at().type != TokenType.EOF and self.at().type != TokenType.CLOSEBRACE:
            body.insert(0, self.parseStmt())
        
        self.expect(TokenType.CLOSEBRACE, "close brace expected")

        fn = FxnDec(params, name, body)
        return fn
    
    def parseVarDec(self):
        isConstant = (self.eat().type == TokenType.CONST)
        ident = self.expect(TokenType.IDENTIFIER,"expected let or const").value

        if self.at().type == TokenType.SEMI:
            self.eat()
            if isConstant:
                raise ValueError("must assign val to const")
            return VarDec(NullVal(), False, ident)
        
        self.expect(TokenType.EQUALS, "expeceted equals token ident in var dec")
        #print("Start")
        dec = VarDec(self.parseExpression(), isConstant, ident)
        #print("AKLFSJAKLF:")
        #print(self.at().value)
        
        self.expect(TokenType.SEMI, "var dec must end with semi: " + ident)
        return dec
    
    def parsePrimary(self):
        tk = self.at().type
        if tk == TokenType.IDENTIFIER:
            return Identifier(self.eat().value)
        elif tk == TokenType.NUMBER:
            return NumericLiteral(float(self.eat().value))
        elif tk == TokenType.OPENPAREN:
            self.eat()
            value = self.parseExpression()
            self.expect(TokenType.CLOSEPAREN, "Expected a close paren")
            return value
        raise ValueError(self.at().value + " " + str(self.at().type))
    
    def parseAdditive(self):
        left = self.parseMultiplicative()
        while self.at().value == "+" or self.at().value == "-":
            operator = self.eat().value
            right = self.parseMultiplicative()
            left = BinaryExpression(left, right, operator)
        return left
    
    def parseMultiplicative(self):
        left = self.parseCallMemExpr()
        while self.at().value == "*" or self.at().value == "/" or self.at().value == "%":
            operator = self.eat().value
            right = self.parseCallMemExpr()
            left = BinaryExpression(left, right, operator)
        return left
    
    
    def parseCallMemExpr(self):
        member = self.parseMemExpr()
        if self.at().type == TokenType.OPENPAREN:
            print("parsing call expr")
            return self.parseCallExpr(member)
        return member
        
    def parseCallExpr(self, caller):
        CallExpr = CallExpression(self.parseArgs(), caller)

        if self.at().type == TokenType.OPENPAREN:
            CallExpr = self.parseCallExpr(CallExpr)

        return CallExpr

    def parseArgs(self):
        self.expect(TokenType.OPENPAREN, "missing open paren")
        if self.at().type == TokenType.CLOSEPAREN:
            args = []
        else:
            args = self.parseArgsList()
        
        self.expect(TokenType.CLOSEPAREN, "missing close paren")
        return args

    def parseArgsList(self):
        args = [self.parseAssignmentExpr()]

        while self.notEof() and self.at().type == TokenType.COMMA:
            self.eat()
            args.insert(0, self.parseAssignmentExpr())

        return args

    def parseMemExpr(self):
        obj = self.parsePrimary()
        while self.at().type == TokenType.DOT or self.at().type == TokenType.OPENBRACKET:
            op = self.eat()
            computed: bool
            if op.type == TokenType.DOT:
                computed = False
                prop = self.parsePrimary()
                if type(prop) != Identifier:
                    raise ValueError(prop)
            else:
                #print("e")
                computed = True
                prop = self.parseExpression()
                self.expect(TokenType.CLOSEBRACKET, "missing closebracket")
            obj = MemberExpression(obj, prop, computed)
        
        return obj


