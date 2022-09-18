#!/usr/bin/python3
import os, glob, sys, re, textwrap
from collections import OrderedDict

def info(msg):
    print("[INFO] %s"%msg)

def error(msg):
    print("[ERROR] %s"%msg)
    sys.exit(-1)

def die(cond, msg):
    if not cond:
        error(msg)

def parse_vm(file_path, all_commands):
    l = []
    file_basename = os.path.basename(file_path)
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("//") or not line: continue
            tmp = []
            for x in line.split():
                if not x: continue
                if x == "//": break
                tmp.append(x)
            if not tmp: continue
            l.append(tmp)
    all_commands[file_basename] = l

def wr(f, msg):
    line = "%s\n"%msg.strip()
    print(line, end='')
    f.write(line)

class Translator:
    def __init__(self, input_path, all_commands):
        self.skip_label = 0
        if os.path.isdir(input_path): # input is a directory
            self.folder_basename = os.path.basename(input_path.strip("/"))
            self.am_file_name = os.path.join(input_path, self.folder_basename + ".asm")
            self.is_folder = True
        else: # input is a single vm file
            folder_name = os.path.split(input_path.strip("/"))[0]
            self.folder_basename = os.path.basename(folder_name.strip("/"))
            self.am_file_name = os.path.join(folder_name, self.folder_basename + ".asm")
            self.is_folder = False
        self.f = open(self.am_file_name, 'w')
        self.all_commands = all_commands
        # changes at runtime
        self.cur_function_name = ""
        self.cur_static_namespace = ""
        self.return_label_counter = 0

    def wr(self, msg):
        wr(self.f, msg)

    def translate_all(self):
        if self.is_folder: # generate bootstrap code for folder only
            content = textwrap.dedent("""
                @256 // SP = 256
                D=A
                @SP
                M=D
                // calling Sys.init""")
            content += self.translate_function(["call", "Sys.init", "0"])
            self.wr("////////// bootstrap //////////")
            self.wr(content)
        for file_path, command_list in self.all_commands.items():
            self.wr("////////// %s //////////"%file_path)
            self.cur_static_namespace = os.path.basename(file_path)
            self.translate(command_list)
        info("asm file is saved as: %s"%self.am_file_name)

    def translate_memory_seg(self, cmd):
        segment_map = {
                "local": "LCL",
                "argument": "ARG",
                "self": "THIS",
                "that": "THAT",
                "temp": "5",
                # for pointer:
                "0"   : "THIS",
                "1"   : "THAT",
        }
        die(len(cmd) == 3, "unknown command '%s'"%cmd)
        act = cmd[0]
        seg = cmd[1]
        arg = cmd[2]
        if seg == "constant":
            # *SP=arg; SP++;
            die(act == "push", "only push is an valid action for constant")
            content = textwrap.dedent("""
                @%s
                D=A
                @SP
                A=M
                M=D //  *SP = x;
                @SP
                M=M+1 // SP++"""%arg)
        elif seg in ["local", "argument", "self", "that", "temp"]:
            # addr=segment+i;
            content = textwrap.dedent("""
                @%s
                D=A
                @%s
                D=%s+D
                @addr
                M=D // addr = %s + i"""%(
                    arg,
                    segment_map[seg],
                    ("A" if seg == "temp" else "M"),
                    segment_map[seg]))
            if act == "pop":
                # SP--; *addr=*SP
                content += textwrap.dedent("""
                    @SP
                    M=M-1 // SP--
                    A=M
                    D=M
                    @addr
                    A=M
                    M=D // *addr=*SP""")
            elif act == "push":
                # *SP=*addr; SP++;
                content += textwrap.dedent("""
                    A=M
                    D=M
                    @SP
                    A=M
                    M=D  // *SP = *addr
                    @SP
                    M=M+1 // SP++""")
            else:
                error("unknown act '%s'"%act)
        elif seg in ["pointer", "static"]:
            if act == "push":
                # *SP = THIS/THAT/<static_namespace>.x; SP++;
                content = textwrap.dedent("""
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1 // SP++
                    """)
                if seg == "pointer":
                    content = textwrap.dedent("""
                        @%s // *SP = THIS/THAT
                        %s"""%(segment_map[arg], content))
                else: # static
                    register = "%s.%s"%(self.cur_static_namespace, arg)
                    content = textwrap.dedent("""
                        @%s // *SP = %s.x
                        %s"""%(register, self.cur_static_namespace, content))
            elif act == "pop":
                # SP--; THIS/THAT/<static_namespace>.x=*SP;
                content = textwrap.dedent("""
                    @SP
                    M=M-1 // SP--
                    A=M
                    D=M""")
                if seg == "pointer":
                    content += textwrap.dedent("""
                        @%s
                        M=D // THIS/THAT=*SP
                        """%segment_map[arg])
                else: # static
                    register = "%s.%s"%(self.cur_static_namespace, arg)
                    content += textwrap.dedent("""
                        @%s
                        M=D // %s.x=*SP
                        """%(register, self.cur_static_namespace))
            else:
                error("unknown act '%s'"%act)
        else:
            error("unknown segment '%s'"%seg)
        return content

    def translate_arith_logical(self, cmd):
        die(len(cmd) == 1, "unknown command '%s'"%cmd)
        op = cmd[0]
        # SP--; y = *SP
        content = textwrap.dedent("""
            @SP
            M=M-1 // SP--
            @SP
            A=M
            D=M
            @y
            M=D // y = *SP""")
        if op in ["neg", "not"]: # unary op
            if op == "neg":
                content += textwrap.dedent("""
                    @y
                    M=-M""")
            elif op == "not":
                content += textwrap.dedent("""
                    @y
                    M=!M""")
            else:
                error("unknown op '%s'"%op)
        else: # binary op
            # SP--; y = *SP
            content += textwrap.dedent("""
                @SP
                M=M-1 // SP--
                @SP
                A=M
                D=M
                @x
                M=D // x = *SP
                @y
                D=M""") # now D is 'y'
            if op == "add":
                # x=x+y *SP=x;
                content += textwrap.dedent("""
                    @x
                    M=M+D // x = x + y""")
            elif op == "sub":
                # x=x-y; *SP=x;
                content += textwrap.dedent("""
                    @x
                    M=M-D // x = x - y""")
            elif op in ["gt", "lt", "eq"]:
                if op == "gt":
                    # x = (x > y ? -1 : 0)
                    content += textwrap.dedent("""
                        @x
                        M=M-D
                        D=M
                        @x
                        M=-1
                        @skip%d // if x > y, skip setting 0
                        D;JGT"""%self.skip_label)
                elif op == "lt":
                    # x = (x < y ? -1 : 0)
                    content += textwrap.dedent("""
                        @x
                        M=M-D
                        D=M
                        @x
                        M=-1
                        @skip%d // if x < y, skip setting 0
                        D;JLT"""%self.skip_label)
                elif op == "eq":
                    # x = (x == y ? -1 : 0)
                    content += textwrap.dedent("""
                        @x
                        M=M-D
                        D=M
                        @x
                        M=-1
                        @skip%d // if x == y, skip setting 0
                        D;JEQ"""%self.skip_label)
                content += textwrap.dedent("""
                    @x
                    M=0
                    (skip%d)
                    @x
                    """%(self.skip_label))
                self.skip_label += 1
            elif op == "and":
                # x=(x&y);
                content += textwrap.dedent("""
                    @x
                    M=M&D // x = (x&y)
                    """)
            elif op == "or":
                # x=(x|y); *SP=x;
                content += textwrap.dedent("""
                    @x
                    M=M|D // x = (x|y)
                    """)
            else:
              error("unknown op '%s'"%op)
        # *SP = x/y; SP++
        content += textwrap.dedent("""
            D=M
            @SP
            A=M
            M=D // *SP=y(for unary)/x(for binary)
            @SP
            M=M+1""")
        return content

    def translate_branching(self, cmd):
        act = cmd[0]
        label = cmd[1]
        if act == "label":
            # (label)
            content = textwrap.dedent("""
                (%s)"""%label)
        elif act == "if-goto":
            # SP--; D=*SP; jump to label if D != 0
            content = textwrap.dedent("""
                @SP
                M=M-1
                A=M
                D=M
                @%s
                D;JNE"""%label)
        elif act == "goto":
            content = textwrap.dedent("""
                @%s
                0;JMP"""%label)
        else:
            error("unknown act: '%s'"%act)
        return content

    def translate_function(self, cmd):
        act = cmd[0]
        if act == "function":
            self.cur_function_name = cmd[1]
            num_local_var = cmd[2]
            content = "(" + self.cur_function_name + ")"
            for i in range(int(num_local_var)):
                content += textwrap.dedent("""
                    @SP // local var #%d
                    A=M
                    M=0
                    @SP // SP++
                    M=M+1"""%i)
        elif act == "return":
            die(self.cur_function_name, "empty function name")
            content = textwrap.dedent("""
                @LCL // endFrame = LCL
                D=M
                @endframe
                M=D
                @5 // return_addr = *(endFrame - 5)
                A=D-A
                D=M
                @return_addr
                M=D
                @SP  // *ARG = pop()
                M=M-1
                @SP
                A=M
                D=M
                @ARG
                A=M
                M=D
                @ARG
                D=M
                @SP // SP = ARG + 1
                M=D+1""")
            for i, p in enumerate(["THAT", "THIS", "ARG", "LCL"]):
                i += 1
                content += textwrap.dedent("""
                    @endframe // %s = *(endFrame - %d)
                    D=M
                    @%d
                    A=D-A
                    D=M
                    @%s
                    M=D"""%(p, i, i, p))
            content += textwrap.dedent("""
                @return_addr // goto return_addr
                A=M
                0;JMP""")
        elif act == "call":
            function_name = cmd[1]
            num_arg = int(cmd[2])
            return_label = "%s.$ret.%d"%(function_name, self.return_label_counter)
            self.return_label_counter += 1
            content = textwrap.dedent("""
                @%s // return_label, it's an address
                D=A
                @SP // *SP = return_label
                A=M
                M=D
                @SP // SP++
                M=M+1"""%return_label)
            for p in["LCL", "ARG", "THIS", "THAT"]:
                content += textwrap.dedent("""
                    @%s
                    D=M
                    @SP // *SP = %s
                    A=M
                    M=D
                    @SP // SP++
                    M=M+1"""%(p, p))
            content += textwrap.dedent("""
                @SP // ARG = SP - 5 - nArgs
                D=M
                @5
                D=D-A
                @%d
                D=D-A
                @ARG
                M=D
                @SP
                D=M
                @LCL // LCL = SP
                M=D
                @%s // goto %s
                0;JMP
                (%s)"""%(num_arg, function_name, function_name, return_label))
        else:
            error("unknown act: '%s'"%act)
        return content

    def translate(self, command_list):
        for cmd in command_list:
            # print the input VM command as comment
            self.wr("///////////////// %s ////////////////"%(" ".join(cmd)))
            die(cmd, "unknown command '%s'"%cmd)
            act = cmd[0]
            if act in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
                content = self.translate_arith_logical(cmd)
            elif act in ["push", "pop"]:
                content = self.translate_memory_seg(cmd)
            elif act in ["label", "if-goto", "goto"]:
                content = self.translate_branching(cmd)
            elif act in ["function", "return", "call"]:
                content = self.translate_function(cmd)
            else:
                error("unknown command '%s'"%(" ".join(cmd)))
            die(content, "empty content")
            self.wr(content)

def main(input_path):
    all_commands = OrderedDict()
    if os.path.isdir(input_path):
        for file_path in glob.glob(input_path + "/*.vm"):
            parse_vm(file_path, all_commands)
    else:
        parse_vm(input_path, all_commands)
    print(all_commands)
    t = Translator(input_path, all_commands)
    t.translate_all()

if __name__ == "__main__":
    path = sys.argv[1]
    die(os.path.isfile(path) or os.path.isdir(path), "'%s' does not exist"%path)
    main(path)
