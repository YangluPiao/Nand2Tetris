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
////////// BasicLoop.vm //////////
///////////////// push constant 0 ////////////////
@0
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop local 0 ////////////////
@0
D=A
@LCL
D=M+D
@addr
M=D // addr = LCL + i
@SP
M=M-1 // SP--
A=M
D=M
@addr
A=M
M=D // *addr=*SP
///////////////// label LOOP_START ////////////////
(LOOP_START)
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
///////////////// push local 0 ////////////////
@0
D=A
@LCL
D=M+D
@addr
M=D // addr = LCL + i
A=M
D=M
@SP
A=M
M=D  // *SP = *addr
@SP
M=M+1 // SP++
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
///////////////// pop local 0 ////////////////
@0
D=A
@LCL
D=M+D
@addr
M=D // addr = LCL + i
@SP
M=M-1 // SP--
A=M
D=M
@addr
A=M
M=D // *addr=*SP
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
///////////////// pop argument 0 ////////////////
@0
D=A
@ARG
D=M+D
@addr
M=D // addr = ARG + i
@SP
M=M-1 // SP--
A=M
D=M
@addr
A=M
M=D // *addr=*SP
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
///////////////// if-goto LOOP_START ////////////////
@SP
M=M-1
A=M
D=M
@LOOP_START
D;JNE
///////////////// push local 0 ////////////////
@0
D=A
@LCL
D=M+D
@addr
M=D // addr = LCL + i
A=M
D=M
@SP
A=M
M=D  // *SP = *addr
@SP
M=M+1 // SP++
