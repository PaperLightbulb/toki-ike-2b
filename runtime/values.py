class NullVal:
    value = "null"

class NumVal:
    def __init__(self, val: float):
        self.value = val

class BoolVal:
    def __init__(self, val: bool):
        self.value = val

class ObjVal:
    def __init__(self, prop):
        self.prop = prop

class FxnCall:
    def __init__(self, args, env):
        self.args = args
        self.env = env

class NativeFxnVal:
    def __init__(self, call):
        self.call = call
    call: FxnCall

class FxnVal:
    def __init__(self, name, params, decEnv, body):
        self.name = name
        self.params = params
        self.decEnv = decEnv
        self.body = body
    name: str
    params = []
    body = []