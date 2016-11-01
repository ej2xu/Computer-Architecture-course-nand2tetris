// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

  @R2 // clear R2
  M=0
  @R0
  D=M
  @LOOP // if R0 >= 0
  D;JGE

  @R0 // in case R0 is negative, flip sign of both R0 and R1
  M=-D
  @R1
  M=-M

(LOOP) // while (R0 != 0) R2 += R1
  @R0
  D=M
  @END
  D;JEQ

  @R1
  D=M
  @R2
  M=D+M
  @R0
  M=M-1
  @LOOP
  0;JMP

(END) // end program
  @END
  0;JMP
