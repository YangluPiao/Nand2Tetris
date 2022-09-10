// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// whiten screen
// while true:
//   if key pressed:
//     blacken screen
//     if key unpressed:
//       whiten screen
@color
M=-1 // pretend it's black, so force whiten screen later
D=-1
@COLOR_WHITE
0;JMP
(COLOR_WHITE)
	@color
	M=0
	@COLOR
	D;JMP
(COLOR_BLACK)
	@color
	M=-1
	@COLOR
	D;JMP
(CHECK_KEY)
	@KBD // read from keyboard
	D=M
	@selection // use this variable to decide what to do next
	M=D
	@color // check previous color
	D=M
	@selection
	M=D+M
	D=M // ==0: check_key again; >0: need blacken; <0: need whiten
	@COLOR_WHITE
	D;JLT
	@COLOR_BLACK
	D;JGT
	@CHECK_KEY
	D;JEQ
(COLOR)
	@SCREEN
	D=A
	@addr
	M=D
	@r
	M=0
	// loop through rows
	(LOOP_R)
		@r
		D=M
		@256
		D=D-A
		@COLOR_END
		D;JEQ
		// loop through cols
		@c
		M=0
		(LOOP_C)
				@c
				D=M
				@32
				D=D-A
				@LOOP_R_END
				D;JEQ
				// coloring screen
				@color
				D=M // read color
				@addr
				A=M
				M=D
				// increment addr
				@addr
				M=M+1
				// increment column
				@c
				M=M+1
				@LOOP_C
				0;JMP
	(LOOP_R_END)
		// increment row
		@r
		M=M+1
		@LOOP_R
		0;JMP
(COLOR_END)
	@CHECK_KEY
	0;JMP