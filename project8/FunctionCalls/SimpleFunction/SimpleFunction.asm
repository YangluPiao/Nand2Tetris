////////// SimpleFunction.vm //////////
///////////////// function SimpleFunction.test 2 ////////////////
(SimpleFunction.test)
@SP // local var #0
A=M
M=0
@SP // SP++
M=M+1
@SP // local var #1
A=M
M=0
@SP // SP++
M=M+1
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
///////////////// push local 1 ////////////////
@1
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
///////////////// not ////////////////
@SP
M=M-1 // SP--
@SP
A=M
D=M
@y
M=D // y = *SP
@y
M=!M
D=M
@SP
A=M
M=D // *SP=y(for unary)/x(for binary)
@SP
M=M+1
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
