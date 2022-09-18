////////// bootstrap //////////
@256 // SP = 256
D=A
@SP
M=D
// calling Sys.init
@Sys.init.$ret.0 // return_label, it's an address
D=A
@SP // *SP = return_label
A=M
M=D
@SP // SP++
M=M+1
@LCL
D=M
@SP // *SP = LCL
A=M
M=D
@SP // SP++
M=M+1
@ARG
D=M
@SP // *SP = ARG
A=M
M=D
@SP // SP++
M=M+1
@THIS
D=M
@SP // *SP = THIS
A=M
M=D
@SP // SP++
M=M+1
@THAT
D=M
@SP // *SP = THAT
A=M
M=D
@SP // SP++
M=M+1
@SP // ARG = SP - 5 - nArgs
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL // LCL = SP
M=D
@Sys.init // goto Sys.init
0;JMP
(Sys.init.$ret.0)
////////// Class1.vm //////////
///////////////// function Class1.set 0 ////////////////
(Class1.set)
///////////////// push argument 0 ////////////////
@0
D=A
@ARG
D=M+D
@addr
M=D // addr = ARG + i
A=M
D=M
@SP
A=M
M=D  // *SP = *addr
@SP
M=M+1 // SP++
///////////////// pop static 0 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@Class1.vm.0
M=D // Class1.vm.x=*SP
///////////////// push argument 1 ////////////////
@1
D=A
@ARG
D=M+D
@addr
M=D // addr = ARG + i
A=M
D=M
@SP
A=M
M=D  // *SP = *addr
@SP
M=M+1 // SP++
///////////////// pop static 1 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@Class1.vm.1
M=D // Class1.vm.x=*SP
///////////////// push constant 0 ////////////////
@0
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// return ////////////////
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
M=D+1
@endframe // THAT = *(endFrame - 1)
D=M
@1
A=D-A
D=M
@THAT
M=D
@endframe // THIS = *(endFrame - 2)
D=M
@2
A=D-A
D=M
@THIS
M=D
@endframe // ARG = *(endFrame - 3)
D=M
@3
A=D-A
D=M
@ARG
M=D
@endframe // LCL = *(endFrame - 4)
D=M
@4
A=D-A
D=M
@LCL
M=D
@return_addr // goto return_addr
A=M
0;JMP
///////////////// function Class1.get 0 ////////////////
(Class1.get)
///////////////// push static 0 ////////////////
@Class1.vm.0 // *SP = Class1.vm.x

D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++
///////////////// push static 1 ////////////////
@Class1.vm.1 // *SP = Class1.vm.x

D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++
///////////////// sub ////////////////
@SP
M=M-1 // SP--
@SP
A=M
D=M
@y
M=D // y = *SP
@SP
M=M-1 // SP--
@SP
A=M
D=M
@x
M=D // x = *SP
@y
D=M
@x
M=M-D // x = x - y
D=M
@SP
A=M
M=D // *SP=y(for unary)/x(for binary)
@SP
M=M+1
///////////////// return ////////////////
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
M=D+1
@endframe // THAT = *(endFrame - 1)
D=M
@1
A=D-A
D=M
@THAT
M=D
@endframe // THIS = *(endFrame - 2)
D=M
@2
A=D-A
D=M
@THIS
M=D
@endframe // ARG = *(endFrame - 3)
D=M
@3
A=D-A
D=M
@ARG
M=D
@endframe // LCL = *(endFrame - 4)
D=M
@4
A=D-A
D=M
@LCL
M=D
@return_addr // goto return_addr
A=M
0;JMP
////////// Sys.vm //////////
///////////////// function Sys.init 0 ////////////////
(Sys.init)
///////////////// push constant 6 ////////////////
@6
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// push constant 8 ////////////////
@8
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// call Class1.set 2 ////////////////
@Class1.set.$ret.1 // return_label, it's an address
D=A
@SP // *SP = return_label
A=M
M=D
@SP // SP++
M=M+1
@LCL
D=M
@SP // *SP = LCL
A=M
M=D
@SP // SP++
M=M+1
@ARG
D=M
@SP // *SP = ARG
A=M
M=D
@SP // SP++
M=M+1
@THIS
D=M
@SP // *SP = THIS
A=M
M=D
@SP // SP++
M=M+1
@THAT
D=M
@SP // *SP = THAT
A=M
M=D
@SP // SP++
M=M+1
@SP // ARG = SP - 5 - nArgs
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL // LCL = SP
M=D
@Class1.set // goto Class1.set
0;JMP
(Class1.set.$ret.1)
///////////////// pop temp 0 ////////////////
@0
D=A
@5
D=A+D
@addr
M=D // addr = 5 + i
@SP
M=M-1 // SP--
A=M
D=M
@addr
A=M
M=D // *addr=*SP
///////////////// push constant 23 ////////////////
@23
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// push constant 15 ////////////////
@15
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// call Class2.set 2 ////////////////
@Class2.set.$ret.2 // return_label, it's an address
D=A
@SP // *SP = return_label
A=M
M=D
@SP // SP++
M=M+1
@LCL
D=M
@SP // *SP = LCL
A=M
M=D
@SP // SP++
M=M+1
@ARG
D=M
@SP // *SP = ARG
A=M
M=D
@SP // SP++
M=M+1
@THIS
D=M
@SP // *SP = THIS
A=M
M=D
@SP // SP++
M=M+1
@THAT
D=M
@SP // *SP = THAT
A=M
M=D
@SP // SP++
M=M+1
@SP // ARG = SP - 5 - nArgs
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL // LCL = SP
M=D
@Class2.set // goto Class2.set
0;JMP
(Class2.set.$ret.2)
///////////////// pop temp 0 ////////////////
@0
D=A
@5
D=A+D
@addr
M=D // addr = 5 + i
@SP
M=M-1 // SP--
A=M
D=M
@addr
A=M
M=D // *addr=*SP
///////////////// call Class1.get 0 ////////////////
@Class1.get.$ret.3 // return_label, it's an address
D=A
@SP // *SP = return_label
A=M
M=D
@SP // SP++
M=M+1
@LCL
D=M
@SP // *SP = LCL
A=M
M=D
@SP // SP++
M=M+1
@ARG
D=M
@SP // *SP = ARG
A=M
M=D
@SP // SP++
M=M+1
@THIS
D=M
@SP // *SP = THIS
A=M
M=D
@SP // SP++
M=M+1
@THAT
D=M
@SP // *SP = THAT
A=M
M=D
@SP // SP++
M=M+1
@SP // ARG = SP - 5 - nArgs
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL // LCL = SP
M=D
@Class1.get // goto Class1.get
0;JMP
(Class1.get.$ret.3)
///////////////// call Class2.get 0 ////////////////
@Class2.get.$ret.4 // return_label, it's an address
D=A
@SP // *SP = return_label
A=M
M=D
@SP // SP++
M=M+1
@LCL
D=M
@SP // *SP = LCL
A=M
M=D
@SP // SP++
M=M+1
@ARG
D=M
@SP // *SP = ARG
A=M
M=D
@SP // SP++
M=M+1
@THIS
D=M
@SP // *SP = THIS
A=M
M=D
@SP // SP++
M=M+1
@THAT
D=M
@SP // *SP = THAT
A=M
M=D
@SP // SP++
M=M+1
@SP // ARG = SP - 5 - nArgs
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL // LCL = SP
M=D
@Class2.get // goto Class2.get
0;JMP
(Class2.get.$ret.4)
///////////////// label WHILE ////////////////
(WHILE)
///////////////// goto WHILE ////////////////
@WHILE
0;JMP
////////// Class2.vm //////////
///////////////// function Class2.set 0 ////////////////
(Class2.set)
///////////////// push argument 0 ////////////////
@0
D=A
@ARG
D=M+D
@addr
M=D // addr = ARG + i
A=M
D=M
@SP
A=M
M=D  // *SP = *addr
@SP
M=M+1 // SP++
///////////////// pop static 0 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@Class2.vm.0
M=D // Class2.vm.x=*SP
///////////////// push argument 1 ////////////////
@1
D=A
@ARG
D=M+D
@addr
M=D // addr = ARG + i
A=M
D=M
@SP
A=M
M=D  // *SP = *addr
@SP
M=M+1 // SP++
///////////////// pop static 1 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@Class2.vm.1
M=D // Class2.vm.x=*SP
///////////////// push constant 0 ////////////////
@0
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// return ////////////////
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
M=D+1
@endframe // THAT = *(endFrame - 1)
D=M
@1
A=D-A
D=M
@THAT
M=D
@endframe // THIS = *(endFrame - 2)
D=M
@2
A=D-A
D=M
@THIS
M=D
@endframe // ARG = *(endFrame - 3)
D=M
@3
A=D-A
D=M
@ARG
M=D
@endframe // LCL = *(endFrame - 4)
D=M
@4
A=D-A
D=M
@LCL
M=D
@return_addr // goto return_addr
A=M
0;JMP
///////////////// function Class2.get 0 ////////////////
(Class2.get)
///////////////// push static 0 ////////////////
@Class2.vm.0 // *SP = Class2.vm.x

D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++
///////////////// push static 1 ////////////////
@Class2.vm.1 // *SP = Class2.vm.x

D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++
///////////////// sub ////////////////
@SP
M=M-1 // SP--
@SP
A=M
D=M
@y
M=D // y = *SP
@SP
M=M-1 // SP--
@SP
A=M
D=M
@x
M=D // x = *SP
@y
D=M
@x
M=M-D // x = x - y
D=M
@SP
A=M
M=D // *SP=y(for unary)/x(for binary)
@SP
M=M+1
///////////////// return ////////////////
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
M=D+1
@endframe // THAT = *(endFrame - 1)
D=M
@1
A=D-A
D=M
@THAT
M=D
@endframe // THIS = *(endFrame - 2)
D=M
@2
A=D-A
D=M
@THIS
M=D
@endframe // ARG = *(endFrame - 3)
D=M
@3
A=D-A
D=M
@ARG
M=D
@endframe // LCL = *(endFrame - 4)
D=M
@4
A=D-A
D=M
@LCL
M=D
@return_addr // goto return_addr
A=M
0;JMP
