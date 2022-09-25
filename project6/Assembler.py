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

def parse_asm(file_path):
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
            die(len(tmp) == 1, "")
            l.append(tmp[0])
    return l

def wr(f, msg):
    line = "%s\n"%msg.strip()
    print(line, end='')
    f.write(line)

class Translator:
    def __init__(self, input_path, all_commands):
        folder_name = os.path.split(input_path.strip("/"))[0]
        file_basename = os.path.splitext(os.path.basename(input_path))[0]
        self.hack_file_name = os.path.join(folder_name, file_basename + ".hack")
        # member var
        self.f = open(self.hack_file_name, 'w')
        self.all_commands = all_commands
        self.symbol_address = 16
        self.symbol_table = dict()
        # init symbol table
        for i in range(16):
            self.symbol_table["R%d"%i] = i
        self.symbol_table["SCREEN"] = 16384
        self.symbol_table["KBD"] = 24576
        self.symbol_table["SP"]   = 0
        self.symbol_table["LCL"]  = 1
        self.symbol_table["ARG"]  = 2
        self.symbol_table["THIS"] = 3
        self.symbol_table["THAT"] = 4
        # comp map
        self.comp_map = dict()
        self.comp_map["0"]   = "0101010"
        self.comp_map["1"]   = "0111111"
        self.comp_map["-1"]  = "0111010"
        self.comp_map["D"]   = "0001100"
        self.comp_map["A"]   = "0110000"
        self.comp_map["!D"]  = "0001101"
        self.comp_map["!A"]  = "0110001"
        self.comp_map["-D"]  = "0001111"
        self.comp_map["-A"]  = "0110011"
        self.comp_map["D+1"] = "0011111"
        self.comp_map["A+1"] = "0110111"
        self.comp_map["D-1"] = "0001110"
        self.comp_map["A-1"] = "0110010"
        self.comp_map["D+A"] = "0000010"
        self.comp_map["D-A"] = "0010011"
        self.comp_map["A-D"] = "0000111"
        self.comp_map["D&A"] = "0000000"
        self.comp_map["D|A"] = "0010101"
        self.comp_map["M"]   = "1110000"
        self.comp_map["!M"]  = "1110001"
        self.comp_map["-M"]  = "1110011"
        self.comp_map["M+1"] = "1110111"
        self.comp_map["M-1"] = "1110010"
        self.comp_map["D+M"] = "1000010"
        self.comp_map["D-M"] = "1010011"
        self.comp_map["M-D"] = "1000111"
        self.comp_map["D&M"] = "1000000"
        self.comp_map["D|M"] = "1010101"
        # dest map
        self.dest_map = dict()
        self.dest_map[""]    = "000"
        self.dest_map["M"]   = "001"
        self.dest_map["D"]   = "010"
        self.dest_map["DM"]  = "011"
        self.dest_map["MD"]  = "011"
        self.dest_map["A"]   = "100"
        self.dest_map["AM"]  = "101"
        self.dest_map["MA"]  = "101"
        self.dest_map["AD"]  = "110"
        self.dest_map["DA"]  = "110"
        self.dest_map["ADM"] = "111"
        self.dest_map["AMD"] = "111"
        self.dest_map["DAM"] = "111"
        self.dest_map["DMA"] = "111"
        self.dest_map["MAD"] = "111"
        self.dest_map["MDA"] = "111"
        # jump map
        self.jump_map = dict()
        self.jump_map[""]    = "000"
        self.jump_map["JGT"] = "001"
        self.jump_map["JEQ"] = "010"
        self.jump_map["JGE"] = "011"
        self.jump_map["JLT"] = "100"
        self.jump_map["JNE"] = "101"
        self.jump_map["JLE"] = "110"
        self.jump_map["JMP"] = "111"

    def wr(self, msg):
        wr(self.f, msg)
    def translate(self):
        actual_line_number = 0
        actual_commands = []
        # 1st pass, add symbols to symbol table
        for command in self.all_commands:
            if command.startswith("("):
                m = re.search(r"\((.*)\)", command)
                die(m, "re not matched")
                self.symbol_table[m.group(1)] = actual_line_number
            else:
                actual_commands.append(command)
                actual_line_number += 1
        # 2nd pass, translate A and C instructions
        for i, command in enumerate(actual_commands):
            if command.startswith("@"):
                self.translate_a_command(command)
            else:
                self.translate_c_command(command)
        info("output is saved as '%s'"%self.hack_file_name)
    def translate_a_command(self, command):
        var = command[1:]
        num = 0
        try:
            num = int(var)
        except ValueError:
            if var in self.symbol_table:
                num = self.symbol_table[var]
            else:
                self.symbol_table[var] = self.symbol_address
                num = self.symbol_address
                self.symbol_address += 1
        content = "{0:016b}".format(num)
        self.wr(content)
    def translate_c_command(self, command):
        dest = ""
        comp = ""
        jump = ""
        if "=" in command:
            dest = command.split("=")[0]
            command = command.replace(dest + "=", "")
        if ";" in command:
            jump = command.split(";")[-1]
            command = command.replace(";" + jump, "")
        comp = command.strip()
        content = "111" + self.comp_map[comp] + self.dest_map[dest] + self.jump_map[jump]
        die(len(content) == 16, "invalid C instruction '%s'"%content)
        self.wr(content)

def main(input_path):
    all_commands = parse_asm(input_path)
    print(all_commands)
    t = Translator(input_path, all_commands)
    t.translate()

if __name__ == "__main__":
    path = sys.argv[1]
    die(os.path.isfile(path), "'%s' does not exist"%path)
    main(path)
