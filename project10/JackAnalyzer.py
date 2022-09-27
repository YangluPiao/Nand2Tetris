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
            return ""
    def symbol(self):
        if self.tokenType() == "symbol":
            if self.cur_token in self.symbol_map:
                return self.symbol_map[self.cur_token]
            else:
                return self.cur_token
        else:
            return ""
    def identifier(self):
        if self.tokenType() == "identifier":
            return self.cur_token
        else:
            return ""
    def intVal(self):
        if self.tokenType() == "integerConstant":
            return self.cur_token
        else:
            return ""
    def stringVal(self):
        if self.tokenType() == "stringConstant":
            return self.cur_token.strip("\"")
        else:
            return ""
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
        self.idx = 0
    def genAllTokens(self, f):
        self.rewind()
        f.write("<tokens>\n")
        while self.hasMoreTokens():
            self.advance()
            f.write(self.genToken() + "\n")
        f.write("</tokens>\n")
        self.rewind()

class CompilationEngine:
    def __init__(self, input_f):
        input_str = open(input_f, 'r').read()
        self.tokenizer = JackTokenizer(input_str)
        self.output = open(input_f.replace(".jack", ".xmll"), 'w')
        self.parse_tree = []
        # for debugging purpose
        token_output = open(input_f.replace(".jack", "T.xmll"), 'w')
        self.tokenizer.genAllTokens(token_output)
    def wr(self, content, indent = 0):
        self.output.write(" " * indent + "%s\n"%(content))
    def compile(self):
        self.compileClass(2)
    def compileClass(self, indent):
        pass

    def compileClassVarDec(self):
        pass
    def compileSubroutineDec(self):
        pass
    def compileParameterList(self):
        pass
    def compileSubroutineBody(self):
        pass
    def compileVarDec(self):
        pass
    def compileStatements(self):
        pass
    def compileLet(self):
        pass
    def compileIf(self):
        pass
    def compileWhile(self):
        pass
    def compileDo(self):
        pass
    def compileReturn(self):
        pass
    def compilExpression(self):
        pass
    def compileTerm(self):
        pass
    def compileExpressionList(self):
        pass

if __name__ == "__main__":
    analyzer = JackAnalyzer(sys.argv[1])
    analyzer.start()
