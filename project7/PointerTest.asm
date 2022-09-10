///////////////// push constant 3030 ////////////////
@3030
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop pointer 0 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@THIS
M=D // THIS/THAT=*SP
///////////////// push constant 3040 ////////////////
@3040
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop pointer 1 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@THAT
M=D // THIS/THAT=*SP
///////////////// push constant 32 ////////////////
@32
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop this 2 ////////////////
@2
D=A
@THIS
D=M+D
@addr
M=D // addr = THIS + i
@SP
M=M-1 // SP--
A=M
D=M
@addr
A=M
M=D // *addr=*SP
///////////////// push constant 46 ////////////////
@46
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop that 6 ////////////////
@6
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
///////////////// push pointer 0 ////////////////
@THIS // *SP = THIS/THAT

D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++
///////////////// push pointer 1 ////////////////
@THAT // *SP = THIS/THAT

D=M
@SP
A=M
M=D
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
///////////////// push this 2 ////////////////
@2
D=A
@THIS
D=M+D
@addr
M=D // addr = THIS + i
A=M
D=M
@SP
A=M
M=D  // *SP = *addr
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
///////////////// push that 6 ////////////////
@6
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
