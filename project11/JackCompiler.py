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
    def Kindof(self, name, scope):
        self.enterScope(scope)
        if name in self.table:
            return self.table[name][1]
        else:
            return None
    def Typeof(self, name, scope):
        self.enterScope(scope)
        if name in self.table:
            return self.table[name][0]
        else:
            return None
    def IndexOf(self, name, scope):
        self.enterScope(scope)
        if name in self.table:
            return self.table[name][2]
        else:
            return None
    def has_symbol(self, name, scope):
        self.enterScope(scope)
        if name not in self.table:
            return False
        else:
            return True
    def get_info(self, name, scope):
        if self.has_symbol(name, scope):
            return (self.Typeof(name, scope), self.Kindof(name, scope), self.IndexOf(name, scope))
        else:
            return None
    def print_all(self):
        print("======= class level =======")
        print(self.class_id)
        print(self.class_table)
        print("======= subroutine level =======")
        print(self.subroutine_id)
        print(self.subroutine_table)

class VMWrite:
    def __init__(self):
        pass
    def writePush(self):
        pass
    def writePop(self):
        pass
    def writeArithmetic(self):
        pass
    def writeLabel(self):
        pass

class CompilationEngine:
    def __init__(self, input_f):
        input_str = open(input_f, 'r').read()
        self.tokenizer = JackTokenizer(input_str)
        self.output_xml = open(input_f.replace(".jack", ".xmll"), 'w')
        # self.output_vm = open(input_f.replace(".jack", ".vmm"), 'w')
        self.symbol_table = SymbolTable()
        self.class_name = ""
        self.scope = 0
        # dump tokenizer outptu for debugging purpose
        # token_output = open(input_f.replace(".jack", "T.xmll"), 'w')
        # self.tokenizer.genAllTokens(token_output)
    def wr(self, content, indent = 0):
        self.output_xml.write(" " * indent + "%s\n"%(content))
    def identifier(self, indent):
        if self.tokenizer.tokenType() == "identifier":
            self.wr(self.tokenizer.genToken(), indent)
            name = self.tokenizer.token()
            # try subroutine scope first
            if self.symbol_table.has_symbol(name, 1):
                info = self.symbol_table.get_info(name, 1)
            else:
                info = self.symbol_table.get_info(name, 0)
            if info:
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
            # dec ends with ;
            self.symbol(";", indent)
    def compile(self):
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
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == "keyword":
                t = self.tokenizer.keyWord()
                if t in ["static", "field"]:
                    # now it should be classVarDec
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
        self.vardec(indent)
        self.wr("</classVarDec>", indent - 2)

    def compileSubroutineDec(self, indent):
        self.wr("<subroutineDec>", indent - 2)
        # entering a new subroutine, reset the subroutine table
        self.scope = 1
        self.symbol_table.resetSubroutine()
        # keywords
        self.wr(self.tokenizer.genToken(), indent)
        self.tokenizer.advance()
        # now should be void or a type
        if self.tokenizer.tokenType() == "keyword":
            self.keyword("void", indent)
        else:
            self.type(indent)
        self.tokenizer.advance()
        # now should be subroutine name
        self.identifier(indent)
        self.tokenizer.advance()
        # now should be "("
        self.symbol("(", indent)
        self.tokenizer.advance()
        # add "this" to symbol table
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
                    self.type(indent)
                    self.tokenizer.advance()
                    self.identifier(indent)
                    self.tokenizer.advance()
        self.wr("</parameterList>", indent - 2)
    def compileSubroutineBody(self, indent):
        self.wr("<subroutineBody>", indent - 2)
        self.tokenizer.advance()
        self.symbol("{", indent)
        self.tokenizer.advance()
        # VarDec
        while self.tokenizer.token() == "var":
            self.compileVarDec(indent + 2)
            self.tokenizer.advance()
        # Statements
        self.compileStatements(indent + 2)
        self.symbol("}", indent)
        self.wr("</subroutineBody>", indent - 2)
    def compileVarDec(self, indent):
        self.wr("<varDec>", indent - 2)
        self.vardec(indent)
        self.wr("</varDec>", indent - 2)
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
        self.tokenizer.advance()
        if self.tokenizer.token() == "[":
            self.symbol("[", indent)
            self.tokenizer.advance()
            self.compileExpression(indent + 2)
            self.tokenizer.advance()
            self.symbol("]", indent)
            self.tokenizer.advance()
        self.symbol("=", indent)
        self.tokenizer.advance()
        self.compileExpression(indent + 2)
        self.tokenizer.advance()
        self.symbol(";", indent)
        self.wr("</letStatement>", indent - 2)
    def compileIf(self, indent):
        self.wr("<ifStatement>", indent - 2)
        self.keyword("if", indent)
        self.tokenizer.advance()
        self.symbol("(", indent)
        self.tokenizer.advance()
        self.compileExpression(indent + 2)
        self.tokenizer.advance()
        self.symbol(")", indent)
        self.tokenizer.advance()
        self.symbol("{", indent)
        self.tokenizer.advance()
        self.compileStatements(indent + 2)
        self.symbol("}", indent)
        if self.tokenizer.next_token() == "else":
            self.tokenizer.advance()
            self.keyword("else", indent)
            self.tokenizer.advance()
            self.symbol("{", indent)
            self.tokenizer.advance()
            self.compileStatements(indent + 2)
            self.symbol("}", indent)
        self.wr("</ifStatement>", indent - 2)
    def compileWhile(self, indent):
        self.wr("<whileStatement>", indent - 2)
        self.keyword("while", indent)
        self.tokenizer.advance()
        self.symbol("(", indent)
        self.tokenizer.advance()
        self.compileExpression(indent + 2)
        self.tokenizer.advance()
        self.symbol(")", indent)
        self.tokenizer.advance()
        self.symbol("{", indent)
        self.tokenizer.advance()
        self.compileStatements(indent + 2)
        self.symbol("}", indent)
        self.wr("</whileStatement>", indent - 2)
    def compileSubroutineCall(self, indent):
        self.identifier(indent)
        self.tokenizer.advance()
        # member function
        if self.tokenizer.symbol() == ".":
            self.symbol(".", indent)
            self.tokenizer.advance()
            self.identifier(indent)
            self.tokenizer.advance()
        self.symbol("(", indent)
        self.tokenizer.advance()
        self.compileExpressionList(indent + 2)
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
    def compileReturn(self, indent):
        self.wr("<returnStatement>", indent - 2)
        self.keyword("return", indent)
        self.tokenizer.advance()
        if self.tokenizer.token() != ";":
            self.compileExpression(indent)
            self.tokenizer.advance()
        self.symbol(";", indent)
        self.wr("</returnStatement>", indent - 2)
    def compileExpression(self, indent):
        self.wr("<expression>", indent - 2)
        self.compileTerm(indent + 2)
        # (op term)*
        while self.tokenizer.next_token() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.tokenizer.advance()
            self.wr(self.tokenizer.genToken(), indent)
            self.tokenizer.advance()
            self.compileTerm(indent + 2)
        self.wr("</expression>", indent - 2)
    def compileTerm(self, indent):
        self.wr("<term>", indent - 2)
        tp = self.tokenizer.tokenType()
        if tp in ["integerConstant", "stringConstant"]:
            self.wr(self.tokenizer.genToken(), indent)
        elif tp == "identifier":
            if self.tokenizer.next_token() in ["(", "."]:
                # subroutine call
                self.compileSubroutineCall(indent)
            else:
                self.wr(self.tokenizer.genToken(), indent)
                if self.tokenizer.next_token() == "[":
                    self.tokenizer.advance()
                    self.symbol("[", indent)
                    self.tokenizer.advance()
                    self.compileExpression(indent + 2)
                    self.tokenizer.advance()
                    self.symbol("]", indent)
        elif tp == "keyword":
            if self.tokenizer.token() in ["true", "false", "null", "this"]:
                self.wr(self.tokenizer.genToken(), indent)
            else:
                error("unknown expression: %s"%self.tokenizer.token())
        elif tp == "symbol":
            if self.tokenizer.token() in ["-", "~"]:
                self.wr(self.tokenizer.genToken(), indent)
                self.tokenizer.advance()
                self.compileTerm(indent + 2)
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
        while self.tokenizer.token() != ")":
            self.compileExpression(indent + 2)
            self.tokenizer.advance()
            if self.tokenizer.token() == ",":
                self.symbol(",", indent)
                self.tokenizer.advance()
        self.wr("</expressionList>", indent - 2)

if __name__ == "__main__":
    analyzer = JackAnalyzer(sys.argv[1])
    analyzer.start()
