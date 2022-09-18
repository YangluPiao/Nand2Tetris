////////// FibonacciSeries.vm //////////
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
///////////////// pop pointer 1 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@THAT
M=D // THIS/THAT=*SP
///////////////// push constant 0 ////////////////
@0
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop that 0 ////////////////
@0
D=A
@THAT
D=M+D
@addr
M=D // addr = THAT + i
@SP
M=M-1 // SP--
A=M
D=M
@addr
A=M
M=D // *addr=*SP
///////////////// push constant 1 ////////////////
@1
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop that 1 ////////////////
@1
D=A
@THAT
D=M+D
@addr
M=D // addr = THAT + i
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
///////////////// label MAIN_LOOP_START ////////////////
(MAIN_LOOP_START)
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
///////////////// if-goto COMPUTE_ELEMENT ////////////////
@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JNE
///////////////// goto END_PROGRAM ////////////////
@END_PROGRAM
0;JMP
///////////////// label COMPUTE_ELEMENT ////////////////
(COMPUTE_ELEMENT)
///////////////// push that 0 ////////////////
@0
D=A
@THAT
D=M+D
@addr
M=D // addr = THAT + i
A=M
D=M
@SP
A=M
M=D  // *SP = *addr
@SP
M=M+1 // SP++
///////////////// push that 1 ////////////////
@1
D=A
@THAT
D=M+D
@addr
M=D // addr = THAT + i
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
///////////////// pop that 2 ////////////////
@2
D=A
@THAT
D=M+D
@addr
M=D // addr = THAT + i
@SP
M=M-1 // SP--
A=M
D=M
@addr
A=M
M=D // *addr=*SP
///////////////// push pointer 1 ////////////////
@THAT // *SP = THIS/THAT

D=M
@SP
A=M
M=D
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
///////////////// pop pointer 1 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@THAT
M=D // THIS/THAT=*SP
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
///////////////// goto MAIN_LOOP_START ////////////////
@MAIN_LOOP_START
0;JMP
///////////////// label END_PROGRAM ////////////////
(END_PROGRAM)
