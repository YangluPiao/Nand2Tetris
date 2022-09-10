///////////////// push constant 111 ////////////////
@111
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// push constant 333 ////////////////
@333
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// push constant 888 ////////////////
@888
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop static 8 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@StaticTest.8
M=D // file_basename.x=*SP
///////////////// pop static 3 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@StaticTest.3
M=D // file_basename.x=*SP
///////////////// pop static 1 ////////////////
@SP
M=M-1 // SP--
A=M
D=M
@StaticTest.1
M=D // file_basename.x=*SP
///////////////// push static 3 ////////////////
@StaticTest.3 // *SP = file_basename.x

D=M
@SP
A=M
M=D
@SP
M=M+1 // SP++
///////////////// push static 1 ////////////////
@StaticTest.1 // *SP = file_basename.x

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
///////////////// push static 8 ////////////////
@StaticTest.8 // *SP = file_basename.x

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
