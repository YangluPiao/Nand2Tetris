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
////////// Sys.vm //////////
///////////////// function Sys.init 0 ////////////////
(Sys.init)
///////////////// push constant 4000 ////////////////
@4000
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
///////////////// push constant 5000 ////////////////
@5000
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
///////////////// call Sys.main 0 ////////////////
@Sys.main.$ret.1 // return_label, it's an address
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
@Sys.main // goto Sys.main
0;JMP
(Sys.main.$ret.1)
///////////////// pop temp 1 ////////////////
@1
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
///////////////// label LOOP ////////////////
(LOOP)
///////////////// goto LOOP ////////////////
@LOOP
0;JMP
///////////////// function Sys.main 5 ////////////////
(Sys.main)
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
@SP // local var #2
A=M
M=0
@SP // SP++
M=M+1
@SP // local var #3
A=M
M=0
@SP // SP++
M=M+1
@SP // local var #4
A=M
M=0
@SP // SP++
M=M+1
///////////////// push constant 4001 ////////////////
@4001
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
///////////////// push constant 5001 ////////////////
@5001
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
///////////////// push constant 200 ////////////////
@200
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop local 1 ////////////////
@1
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
///////////////// push constant 40 ////////////////
@40
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop local 2 ////////////////
@2
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
///////////////// push constant 6 ////////////////
@6
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// pop local 3 ////////////////
@3
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
///////////////// push constant 123 ////////////////
@123
D=A
@SP
A=M
M=D //  *SP = x;
@SP
M=M+1 // SP++
///////////////// call Sys.add12 1 ////////////////
@Sys.add12.$ret.2 // return_label, it's an address
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
@Sys.add12 // goto Sys.add12
0;JMP
(Sys.add12.$ret.2)
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
///////////////// push local 2 ////////////////
@2
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
///////////////// push local 3 ////////////////
@3
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
///////////////// push local 4 ////////////////
@4
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
///////////////// function Sys.add12 0 ////////////////
(Sys.add12)
///////////////// push constant 4002 ////////////////
@4002
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
///////////////// push constant 5002 ////////////////
@5002
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
///////////////// push constant 12 ////////////////
@12
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
