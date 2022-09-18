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
////////// Main.vm //////////
///////////////// function Main.fibonacci 0 ////////////////
(Main.fibonacci)
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
///////////////// push constant 2 ////////////////
@2
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// lt ////////////////
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
M=M-D
D=M
@x
M=-1
@skip0 // if x < y, skip setting 0
D;JLT
@x
M=0
(skip0)
@x

D=M
@SP
A=M
M=D // *SP=y(for unary)/x(for binary)
@SP
M=M+1
///////////////// if-goto IF_TRUE ////////////////
@SP
M=M-1
A=M
D=M
@IF_TRUE
D;JNE
///////////////// goto IF_FALSE ////////////////
@IF_FALSE
0;JMP
///////////////// label IF_TRUE ////////////////
(IF_TRUE)
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
///////////////// label IF_FALSE ////////////////
(IF_FALSE)
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
///////////////// push constant 2 ////////////////
@2
D=A
@SP
A=M
M=D //  *SP = x;
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
///////////////// call Main.fibonacci 1 ////////////////
@Main.fibonacci.$ret.1 // return_label, it's an address
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
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL // LCL = SP
M=D
@Main.fibonacci // goto Main.fibonacci
0;JMP
(Main.fibonacci.$ret.1)
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
///////////////// push constant 1 ////////////////
@1
D=A
@SP
A=M
M=D //  *SP = x;
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
///////////////// call Main.fibonacci 1 ////////////////
@Main.fibonacci.$ret.2 // return_label, it's an address
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
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL // LCL = SP
M=D
@Main.fibonacci // goto Main.fibonacci
0;JMP
(Main.fibonacci.$ret.2)
///////////////// add ////////////////
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
M=M+D // x = x + y
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
///////////////// push constant 4 ////////////////
@4
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// call Main.fibonacci 1 ////////////////
@Main.fibonacci.$ret.3 // return_label, it's an address
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
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL // LCL = SP
M=D
@Main.fibonacci // goto Main.fibonacci
0;JMP
(Main.fibonacci.$ret.3)
///////////////// label WHILE ////////////////
(WHILE)
///////////////// goto WHILE ////////////////
@WHILE
0;JMP
