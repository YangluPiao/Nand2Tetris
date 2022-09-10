///////////////// push constant 10 ////////////////
@10
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
///////////////// push constant 21 ////////////////
@21
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// push constant 22 ////////////////
@22
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop argument 2 ////////////////
@2
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
///////////////// pop argument 1 ////////////////
@1
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
///////////////// push constant 36 ////////////////
@36
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop this 6 ////////////////
@6
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
///////////////// push constant 42 ////////////////
@42
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// push constant 45 ////////////////
@45
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop that 5 ////////////////
@5
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
///////////////// push constant 510 ////////////////
@510
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop temp 6 ////////////////
@6
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
///////////////// push that 5 ////////////////
@5
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
///////////////// push this 6 ////////////////
@6
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
///////////////// push this 6 ////////////////
@6
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
///////////////// push temp 6 ////////////////
@6
D=A
@5
D=A+D
@addr
M=D // addr = 5 + i
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
