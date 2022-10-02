#! /usr/bin/python3
import os, glob, sys, re, textwrap

def info(msg):
    print("[INFO] %s"%msg)

def error(msg):
    print("[ERROR] %s"%msg)
    sys.exit(-1)

def die(cond, msg):
    if not cond:
        error(msg)

class JackAnalyzer:
    def __init__(self, input_path):
        self.input_path = input_path
    def start(self):
        input_file_list = []
        if os.path.isdir(self.input_path):
            for f in glob.glob(os.path.join(self.input_path, "*.jack")):
                input_file_list.append(f)
        else:
            input_file_list.append(self.input_path)
        for f in input_file_list:
            engine = CompilationEngine(f)
            engine.compile()

class JackTokenizer:
    def __init__(self, input_str):
        self.tokens = []
        self.keywords = ["class", "constructor", "function", "method", "field", "static",
                "var", "int", "char", "boolean", "void", "true", "false", "null",
                "this", "let", "do", "if", "else", "while", "return"]
        self.symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*",
                "/", "&", "|", "<", ">", "=", "~"]
        self.symbol_map = dict()
        self.symbol_map["<"] = "&lt;"
        self.symbol_map[">"] = "&gt;"
        self.symbol_map["&"] = "&amp;"
        # remove all comments and leading and trailing white spaces
        lines = []
        multiline_comment = False
        for line in input_str.split("\n"):
            if line.startswith("//"):
                continue
            line = re.sub(r"\/\*.*\*\/", "", line)
            line = re.sub(r"\/\/.*", "", line)
            line = line.strip()
            if not line:
                continue
            if line.startswith("/*"):
                multiline_comment = True
            elif line.endswith("*/"):
                multiline_comment = False
            elif not multiline_comment:
                lines.append(line)
        tokens = []
        for line in lines:
            string_const = False
            token = ""
            for x in line:
                if x == "\"":
                    token += x
                    if string_const:
                        string_const = False
                    else:
                        string_const = True
                        continue
                elif string_const:
                    token += x
                    continue
                elif x in self.symbols:
                    if token:
                        tokens.append(token)
                        token = ""
                    tokens.append(x)
                    continue
                elif x != " " and x != "\n":
                    token += x
                    continue
                # now we just finished finding a token, possibily empty
                if (token):
                    tokens.append(token)
                    token = ""
        # done extracting all tokens
        self.tokens = tokens
        self.idx = -1
        self.cur_token = ""
    def hasMoreTokens(self):
        return self.idx + 1 < len(self.tokens)
    def advance(self):
        self.idx += 1
        self.cur_token = self.tokens[self.idx]
    def token(self):
        return self.cur_token
    def next_token(self):
        if self.hasMoreTokens():
            return self.tokens[self.idx + 1]
        else:
            return ""
    def tokenType(self):
        if self.cur_token in self.keywords:
            return "keyword"
        elif self.cur_token in self.symbols:
            return "symbol"
        elif self.cur_token.isdigit():
            return "integerConstant"
        elif self.cur_token.startswith("\""):
            return "stringConstant"
        else:
            return "identifier"
    def keyWord(self):
        if self.tokenType() == "keyword":
            return self.cur_token
        else:
            error("unknown keyword: %s"%self.cur_token)
    def symbol(self):
        if self.tokenType() == "symbol":
            if self.cur_token in self.symbol_map:
                return self.symbol_map[self.cur_token]
            else:
                return self.cur_token
        else:
            error("unknown symbol: %s"%self.cur_token)
    def identifier(self):
        if self.tokenType() == "identifier":
            return self.cur_token
        else:
            error("unknown identifier: %s"%self.cur_token)
    def intVal(self):
        if self.tokenType() == "integerConstant":
            return self.cur_token
        else:
            error("unknown integerConstant: %s"%self.cur_token)
    def stringVal(self):
        if self.tokenType() == "stringConstant":
            return self.cur_token.strip("\"")
        else:
            error("unknown stringConstant: %s"%self.cur_token)
    def genToken(self):
        ty = self.tokenType()
        t = ""
        if ty == "keyword":
            t = self.keyWord()
        elif ty == "symbol":
            t = self.symbol()
        elif ty == "identifier":
            t = self.identifier()
        elif ty == "integerConstant":
            t = self.intVal()
        elif ty == "stringConstant":
            t = self.stringVal()
        else:
            error("kek")
        return "<%s> %s </%s>"%(ty, t, ty)
    def rewind(self):
        self.idx = -1
    def genAllTokens(self, f):
        self.rewind()
        f.write("<tokens>\n")
        while self.hasMoreTokens():
            self.advance()
            f.write(self.genToken() + "\n")
        f.write("</tokens>\n")
        self.rewind()

class SymbolTable:
    def __init__(self):
        self.class_id = dict()
        self.class_id["field"] = 0
        self.class_id["static"] = 0
        self.class_table = dict()

        self.subroutine_id = dict()
        self.subroutine_table = dict()
        self.resetSubroutine()

        # used as pointer to tables and ids for current scope
        self.id_table = None
        self.table = None
    def resetSubroutine(self):
        self.subroutine_id.clear()
        for t in ["argument", "var"]:
            self.subroutine_id[t] = 0
        self.subroutine_table = dict()

    def startSubroutine(self):
        self.resetSubroutine()
        self.resetId(self.subroutine_id)
        self.subroutine_table = dict()

    def enterScope(self, scope):
        if scope == 0:
            self.id_table = self.class_id
            self.table = self.class_table
        else:
            self.id_table = self.subroutine_id
            self.table = self.subroutine_table

    # scope == 0: class, scope == 1: subroutine
    # value is: type, kind, id
    def define(self, name, type, kind):
        if kind in ["field", "static"]:
            scope = 0
        else:
            scope = 1
        self.enterScope(scope)
        self.table[name] = (type, kind, self.id_table[kind])
        self.id_table[kind] += 1
    def VarCount(self, kind, scope):
        self.enterScope(scope)
        return self.id_table[kind]
    def find_in_scope(self, name, scope):
        self.enterScope(scope)
        if name in self.table:
            return self.table[name]
        else:
            return None
    def find_info(self, name):
        subroutine_scope = self.find_in_scope(name, 1)
        if subroutine_scope:
            return subroutine_scope
        class_scope = self.find_in_scope(name, 0)
        if class_scope:
            return class_scope
        return None
    def find_entry(self, name, entry):
        info = self.find_info(name)
        if info:
            return info[entry]
        else:
            return None
    def Kindof(self, name):
        return self.find_entry(name, 1)
    def Typeof(self, name):
        return self.find_entry(name, 0)
    def IndexOf(self, name):
        return self.find_entry(name, 2)
    def print_all(self):
        print("======= class level =======")
        print(self.class_table)
        print("======= subroutine level =======")
        print(self.subroutine_table)

class VMWrite:
    def __init__(self, output_f):
        self.output_vm = output_f
        self.labels = dict() # label -> counter
    def write(self, content):
        self.output_vm.write("%s\n"%(content))
    def write_operation(self, operation, segment, index):
        self.write("%s %s %d"%(operation, segment, index))
    def writePush(self, segment, index):
        self.write_operation("push", segment, index)
    def writePop(self, segment, index):
        self.write_operation("pop", segment, index)
    def writeArithmetic(self):
        pass
    def lookupLabel(self, l):
        if l not in self.labels:
            self.labels[l] = 0
        return self.labels[l]
    def incrementLabelCounter(self, l):
        self.labels[l] += 1
    def getLabel(self, l):
        i = self.lookupLabel(l)
        self.incrementLabelCounter(l)
        return "%s%d"%(l, i)
    def writeLabel(self, l):
        self.write("label %s"%(l))
    def writeGoto(self, l):
        self.write("goto %s"%(l))
    def writeIfGoto(self, l):
        self.write("if-goto %s"%(l))
    def writeIf(self, l):
        self.write("not")
        self.write("if-goto %s"%(l))
    def writeCall(self, name, num_args):
        self.write("call %s %d"%(name, num_args))
    def writeFunction(self, name, num_local_vars):
        self.write("function %s %d"%(name, num_local_vars))
    def writeReturn(self):
        self.write("return")
    def writeInt(self, val):
        self.writePush("constant", val)
    def writeString(self, string):
        string = string[1:-1]
        self.writeInt(len(string))
        self.writeCall("String.new", 1)
        for c in string:
            self.writeInt(ord(c))
            self.writeCall("String.appendChar", 2)


class CompilationEngine:
    def __init__(self, input_f):
        input_str = open(input_f, 'r').read()
        self.tokenizer = JackTokenizer(input_str)
        self.output_xml = open(input_f.replace(".jack", ".xmll"), 'w')
        self.symbol_table = SymbolTable()
        self.class_name = ""
        self.class_member_counter = 0
        self.subroutine_type = ""
        self.subroutine_name = ""
        self.scope = 0
        # VM Writer
        self.output_vm_name = input_f.replace(".jack", ".vm")
        self.output_vm = open(self.output_vm_name, 'w')
        self.vmwriter = VMWrite(self.output_vm)
        # dump tokenizer outptu for debugging purpose
        # token_output = open(input_f.replace(".jack", "T.xmll"), 'w')
        # self.tokenizer.genAllTokens(token_output)

    def symbol_info(self, name):
        return self.symbol_table.find_info(name)
    def symbol_id(self, name):
        info = self.symbol_info(name)
        return info[2]
    def symbol_vm_seg(self, name):
        info = self.symbol_info(name)
        ty = info[1]
        lookup = {
                "field": "this",
                "argument": "argument",
                "static": "static",
                "var": "local"
                }
        return lookup[ty]
    def symbol_get_seg_and_idx(self, name):
        return self.symbol_vm_seg(name), self.symbol_id(name)
    def cur_symbol_get_seg_and_idx(self):
        return self.symbol_get_seg_and_idx(self.tokenizer.token())
    def wr(self, content, indent = 0):
        self.output_xml.write(" " * indent + "%s\n"%(content))
    def identifier(self, indent):
        if self.tokenizer.tokenType() == "identifier":
            self.wr(self.tokenizer.genToken(), indent)
            name = self.tokenizer.token()
            # try subroutine scope first
            info = self.symbol_info(name)
            if info: # if it doesn't exist, then it's a function name instead of a symbol
                self.wr("<!-- name=%s type=%s kind=%s id=%d -->"
                        %(name, info[0], info[1], info[2]), indent)
        else:
            error("unkonwn identifier: %s"%self.tokenizer.token())
    def keyword(self, kw, indent):
        t = self.tokenizer.token()
        if t == kw:
            self.wr(self.tokenizer.genToken(), indent)
        else:
            error("missing keyword %s, got %s instead"%(kw, t))
    def symbol(self, symb, indent):
        t = self.tokenizer.token()
        if t == symb:
            self.wr(self.tokenizer.genToken(), indent)
        else:
            error("missing symbol %s, got %s instead"%(symb, t))
    # type: int|char|boolean|varName
    def type(self, indent):
        if self.tokenizer.tokenType() == "keyword":
            t = self.tokenizer.keyWord()
            if t in ["int", "char", "boolean"]:
                self.wr(self.tokenizer.genToken(), indent)
                return True
        elif self.tokenizer.tokenType() == "identifier":
            self.identifier(indent)
            return True
        return False
    # type varName (',' varName)* ';'
    def vardec(self, indent):
        # static or field or var
        symbol_kind = self.tokenizer.token()
        self.wr(self.tokenizer.genToken(), indent)
        self.tokenizer.advance()
        # now should a type
        symbol_type = self.tokenizer.token()
        self.type(indent)
        self.tokenizer.advance()
        # now should be a varName(identifier)
        symbol_name = self.tokenizer.token()
        self.symbol_table.define(symbol_name, symbol_type, symbol_kind)
        self.identifier(indent)
        self.tokenizer.advance()
        counter = 1
        if self.tokenizer.tokenType() == "symbol":
            while self.tokenizer.symbol() != ";":
                # more decs
                self.symbol(",", indent)
                self.tokenizer.advance()
                symbol_name = self.tokenizer.token()
                # type and kind remain unchanged
                self.symbol_table.define(symbol_name, symbol_type, symbol_kind)
                self.identifier(indent)
                self.tokenizer.advance()
                counter += 1
            # dec ends with ;
            self.symbol(";", indent)
        # return number of variables
        return counter
    def compile(self):
        info("output vm file will be located at: %s"%self.output_vm_name)
        while self.tokenizer.hasMoreTokens():
            # advance is done at the begining, so don't advance after each subroutine
            self.tokenizer.advance()
            die(self.tokenizer.token() == "class", "missing keyword class")
            self.compileClass(2)
    def compileClass(self, indent):
        self.wr("<class>", indent - 2)
        self.scope = 0
        self.wr(self.tokenizer.genToken(), indent)
        self.tokenizer.advance()
        # current token should be an identifier
        self.class_name = self.tokenizer.token()
        self.wr(self.tokenizer.genToken(), indent)
        self.tokenizer.advance()
        # now it should be {
        self.symbol("{", indent)
        self.class_member_counter = 0
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == "keyword":
                t = self.tokenizer.keyWord()
                if t == "field":
                    # now it should be classVarDec
                    self.class_member_counter += self.compileClassVarDec(indent + 2)
                elif t == "static":
                    self.compileClassVarDec(indent + 2)
                elif t in ["constructor", "function", "method"]:
                    # now it should be subroutineDec
                    self.compileSubroutineDec(indent + 2)
            elif self.tokenizer.tokenType() == "symbol":
                self.symbol("}", indent)
                break
            else:
                error("syntax error in compileClass: "%self.tokenizer.token())
        self.wr("</class>", indent - 2)
    def compileClassVarDec(self, indent):
        self.wr("<classVarDec>", indent - 2)
        counter = self.vardec(indent)
        self.wr("</classVarDec>", indent - 2)
        return counter

    def compileSubroutineDec(self, indent):
        self.wr("<subroutineDec>", indent - 2)
        # entering a new subroutine, reset the subroutine table
        self.scope = 1
        self.symbol_table.resetSubroutine()
        self.subroutine_type = self.tokenizer.keyWord()
        # keywords
        self.wr(self.tokenizer.genToken(), indent)
        self.tokenizer.advance()
        # now should be void or a type
        if self.tokenizer.token() == "void":
            self.keyword("void", indent)
        else:
            self.type(indent)
        self.tokenizer.advance()
        # now should be subroutine name
        self.identifier(indent)
        self.subroutine_name = self.tokenizer.token()
        self.tokenizer.advance()
        # now should be "("
        self.symbol("(", indent)
        self.tokenizer.advance()
        # add "this" to symbol table
        if self.subroutine_type == "method":
            self.symbol_table.define("this", self.class_name, "argument")
        # now is parameter list
        self.compileParameterList(indent + 2)
        # ")"
        self.symbol(")", indent)
        # subroutine body
        self.compileSubroutineBody(indent + 2)
        self.wr("</subroutineDec>", indent - 2)
    def compileParameterList(self, indent):
        self.wr("<parameterList>", indent - 2)
        if self.type(indent):
            symbol_type = self.tokenizer.token()
            self.tokenizer.advance()
            symbol_name = self.tokenizer.token()
            self.symbol_table.define(symbol_name, symbol_type, "argument")
            self.identifier(indent)
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == "symbol":
                while self.tokenizer.symbol() != ")": # ends with ")"
                    # more params
                    self.symbol(",", indent)
                    self.tokenizer.advance()
                    symbol_type = self.tokenizer.token()
                    self.type(indent)
                    self.tokenizer.advance()
                    symbol_name = self.tokenizer.token()
                    self.identifier(indent)
                    self.symbol_table.define(symbol_name, symbol_type, "argument")
                    self.tokenizer.advance()
        self.wr("</parameterList>", indent - 2)
    def compileSubroutineBody(self, indent):
        self.wr("<subroutineBody>", indent - 2)
        self.tokenizer.advance()
        self.symbol("{", indent)
        self.tokenizer.advance()
        # VarDec
        counter = 0
        while self.tokenizer.token() == "var":
            counter += self.compileVarDec(indent + 2)
            self.tokenizer.advance()
        self.vmwriter.writeFunction("%s.%s"%(self.class_name, self.subroutine_name), counter)
        if self.subroutine_type == "constructor":
            self.vmwriter.writePush("constant", self.class_member_counter)
            self.vmwriter.writeCall("Memory.alloc", 1)
            self.vmwriter.writePop("pointer", 0)
        elif self.subroutine_type == "method":
            self.vmwriter.writePush("argument", 0)
            self.vmwriter.writePop("pointer", 0)
        # Statements
        self.compileStatements(indent + 2)
        self.symbol("}", indent)
        # exit subroutine
        self.scope = 0
        self.wr("</subroutineBody>", indent - 2)
    def compileVarDec(self, indent):
        self.wr("<varDec>", indent - 2)
        counter = self.vardec(indent)
        self.wr("</varDec>", indent - 2)
        return counter
    def compileStatements(self, indent):
        self.wr("<statements>", indent - 2)
        while self.tokenizer.tokenType() == "keyword" and self.tokenizer.hasMoreTokens():
            if self.tokenizer.keyWord() == "let":
                self.compileLet(indent + 2)
            elif self.tokenizer.keyWord() == "if":
                self.compileIf(indent + 2)
            elif self.tokenizer.keyWord() == "while":
                self.compileWhile(indent + 2)
            elif self.tokenizer.keyWord() == "do":
                self.compileDo(indent + 2)
            elif self.tokenizer.keyWord() == "return":
                self.compileReturn(indent + 2)
            self.tokenizer.advance()
        self.wr("</statements>", indent - 2)
    def compileLet(self, indent):
        self.wr("<letStatement>", indent - 2)
        self.keyword("let", indent)
        self.tokenizer.advance()
        self.identifier(indent)
        # record the LHS
        self.scope = 1 # subroutine scope
        lhs = self.tokenizer.token()
        self.tokenizer.advance()
        if self.tokenizer.token() == "[": # array
            self.symbol("[", indent)
            self.tokenizer.advance()
            self.compileExpression(indent + 2)
            # push index(constant) first, followed by identifier
            seg, idx = self.symbol_get_seg_and_idx(lhs)
            self.vmwriter.writePush(seg, idx)
            # array access
            self.vmwriter.write("add")
            self.tokenizer.advance()
            self.symbol("]", indent)
            self.tokenizer.advance()
            self.symbol("=", indent)
            self.tokenizer.advance()
            self.compileExpression(indent + 2)
            self.vmwriter.writePop("temp", 0) # store value in temp
            self.vmwriter.writePop("pointer", 1) # restore destination
            self.vmwriter.writePush("temp", 0)
            self.vmwriter.writePop("that", 0)
        else:
            self.symbol("=", indent)
            self.tokenizer.advance()
            self.compileExpression(indent + 2)
            seg, idx = self.symbol_get_seg_and_idx(lhs)
            self.vmwriter.writePop(seg, idx)
        self.tokenizer.advance()
        self.symbol(";", indent)
        self.wr("</letStatement>", indent - 2)
    def compileIf(self, indent):
        self.wr("<ifStatement>", indent - 2)
        self.keyword("if", indent)
        self.tokenizer.advance()
        self.symbol("(", indent) # subroutine scope
        self.tokenizer.advance()
        self.compileExpression(indent + 2)
        self.tokenizer.advance()
        self.symbol(")", indent)
        self.tokenizer.advance()
        self.symbol("{", indent)
        self.tokenizer.advance()
        if_label = self.vmwriter.getLabel("IF_TRUE")
        else_label = self.vmwriter.getLabel("IF_FALSE")
        end_label = self.vmwriter.getLabel("IF_END")
        self.vmwriter.writeIfGoto(if_label)
        self.vmwriter.writeGoto(else_label)
        self.vmwriter.writeLabel(if_label)
        self.compileStatements(indent + 2)
        self.symbol("}", indent)
        if self.tokenizer.next_token() == "else":
            self.vmwriter.writeGoto(end_label)
            self.vmwriter.writeLabel(else_label)
            self.tokenizer.advance()
            self.keyword("else", indent)
            self.tokenizer.advance()
            self.symbol("{", indent)
            self.tokenizer.advance()
            self.compileStatements(indent + 2)
            self.symbol("}", indent)
            self.vmwriter.writeLabel(end_label)
        else:
            # need this
            self.vmwriter.writeLabel(else_label)
        self.wr("</ifStatement>", indent - 2)
    def compileWhile(self, indent):
        self.wr("<whileStatement>", indent - 2)
        self.keyword("while", indent)
        body_label = self.vmwriter.getLabel("WHILE_EXP")
        self.vmwriter.writeLabel(body_label)
        end_label = self.vmwriter.getLabel("WHILE_END")
        self.tokenizer.advance()
        self.symbol("(", indent)
        self.tokenizer.advance()
        self.compileExpression(indent + 2)
        self.vmwriter.writeIf(end_label)
        self.tokenizer.advance()
        self.symbol(")", indent)
        self.tokenizer.advance()
        self.symbol("{", indent)
        self.tokenizer.advance()
        self.compileStatements(indent + 2)
        self.symbol("}", indent)
        self.vmwriter.writeGoto(body_label)
        self.vmwriter.writeLabel(end_label)
        self.wr("</whileStatement>", indent - 2)
    def compileSubroutineCall(self, indent):
        self.identifier(indent)
        name = self.tokenizer.token()
        self.tokenizer.advance()
        # member function
        is_static_function = False
        if self.tokenizer.symbol() == ".":
            if self.symbol_table.find_info(name): # customized member functions
                seg, idx = self.symbol_get_seg_and_idx(name)
                self.vmwriter.writePush(seg, idx)
                # replace name with type of the object
                name = self.symbol_table.Typeof(name)
            else: # static functions
                is_static_function = True
            self.symbol(".", indent)
            name += "."
            self.tokenizer.advance()
            self.identifier(indent)
            name += self.tokenizer.token()
            self.tokenizer.advance()
        else:
            # member function of current class
            self.vmwriter.writePush("pointer", 0)
            name = self.class_name + "." + name
        self.symbol("(", indent)
        self.tokenizer.advance()
        num_args = self.compileExpressionList(indent + 2)
        if not is_static_function:
            # implicitly passing "this"
            num_args += 1
        self.vmwriter.writeCall(name, num_args)
        self.symbol(")", indent)
    def compileDo(self, indent):
        self.wr("<doStatement>", indent - 2)
        self.keyword("do", indent)
        self.tokenizer.advance()
        # now is subroutine call
        self.compileSubroutineCall(indent)
        self.tokenizer.advance()
        self.symbol(";", indent)
        self.wr("</doStatement>", indent - 2)
        # always pop return value
        self.vmwriter.writePop("temp", 0)
    def compileReturn(self, indent):
        self.wr("<returnStatement>", indent - 2)
        self.keyword("return", indent)
        self.tokenizer.advance()
        if self.tokenizer.token() != ";":
            self.compileExpression(indent)
            self.tokenizer.advance()
        else:
            # void
            self.vmwriter.writeInt(0)
        self.vmwriter.writeReturn()
        self.symbol(";", indent)
        self.wr("</returnStatement>", indent - 2)
    def compileExpression(self, indent):
        self.wr("<expression>", indent - 2)
        self.compileTerm(indent + 2)
        op_map= {
                "+": "add",
                "-": "sub",
                "*": "call Math.multiply 2",
                "/": "call Math.divide 2",
                "&": "and",
                "|": "or",
                "<": "lt",
                ">": "gt",
                "=": "eq"
                }
        # (op term)*
        while self.tokenizer.next_token() in op_map:
            self.tokenizer.advance()
            # cache the operator, pushing it later
            op = self.tokenizer.token()
            self.wr(self.tokenizer.genToken(), indent)
            self.tokenizer.advance()
            self.compileTerm(indent + 2)
            self.vmwriter.write(op_map[op])
        self.wr("</expression>", indent - 2)
    def compileTerm(self, indent):
        self.wr("<term>", indent - 2)
        tp = self.tokenizer.tokenType()
        if tp in ["integerConstant", "stringConstant"]:
            self.wr(self.tokenizer.genToken(), indent)
            if tp == "stringConstant":
                self.vmwriter.writeString(self.tokenizer.token())
            elif tp == "integerConstant":
                self.vmwriter.writeInt(int(self.tokenizer.token()))
        elif tp == "identifier":
            if self.tokenizer.next_token() in ["(", "."]:
                # subroutine call
                self.compileSubroutineCall(indent)
            else:
                seg, idx = self.cur_symbol_get_seg_and_idx()
                if self.tokenizer.next_token() == "[":
                    self.tokenizer.advance()
                    self.symbol("[", indent)
                    self.tokenizer.advance()
                    self.compileExpression(indent + 2)
                    # push identifier(arugment) after index(constant)
                    self.vmwriter.writePush(seg, idx)
                    self.wr(self.tokenizer.genToken(), indent)
                    # array access
                    self.vmwriter.write("add")
                    self.tokenizer.advance()
                    self.symbol("]", indent)
                    self.vmwriter.writePop("pointer", 1) # restore destination
                    self.vmwriter.writePush("that", 0)
                else:
                    self.vmwriter.writePush(seg, idx)
                    self.wr(self.tokenizer.genToken(), indent)
        elif tp == "keyword":
            name = self.tokenizer.token()
            if name in ["true", "false", "null", "this"]:
                self.wr(self.tokenizer.genToken(), indent)
                if name == "this":
                    self.vmwriter.writePush("pointer", 0)
                else:
                    self.vmwriter.writeInt(0)
                    if name == "true":
                        self.vmwriter.write("not")
            else:
                error("unknown expression: %s"%self.tokenizer.token())
        elif tp == "symbol":
            if self.tokenizer.token() in ["-", "~"]:
                sym = self.tokenizer.token()
                # unary operators
                self.wr(self.tokenizer.genToken(), indent)
                self.tokenizer.advance()
                self.compileTerm(indent + 2)
                if sym == "-":
                    self.vmwriter.write("neg")
                else:
                    self.vmwriter.write("not")
            elif self.tokenizer.token() == "(":
                self.symbol("(", indent)
                self.tokenizer.advance()
                self.compileExpression(indent + 2)
                self.tokenizer.advance()
                self.symbol(")", indent)
        else:
            error("unkonwn term %s"%self.tokenizer.token())
        self.wr("</term>", indent - 2)
    def compileExpressionList(self, indent):
        self.wr("<expressionList>", indent - 2)
        counter = 0
        while self.tokenizer.token() != ")":
            self.compileExpression(indent + 2)
            counter += 1
            self.tokenizer.advance()
            if self.tokenizer.token() == ",":
                self.symbol(",", indent)
                self.tokenizer.advance()
        self.wr("</expressionList>", indent - 2)
        return counter

if __name__ == "__main__":
    analyzer = JackAnalyzer(sys.argv[1])
    analyzer.start()
