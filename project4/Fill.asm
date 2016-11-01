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

(INFLOOP)
  @SCREEN
  D=A
  @addr
  M=D // addr=16384 (base address of Hack screen)
  @KBD
  D=M
  @FILLLOOP // if (kbd) goto FILLLOOP
  D;JNE

(EMPLOOP)
  @addr  // RAM[addr] = 0
  A=M
  M=0
  @addr
  MD=M+1 // addr++; if (addr == KBD) goto INFLOOP
  @KBD
  D=D-A
  @INFLOOP
  D;JEQ

  @EMPLOOP
  0;JMP

(FILLLOOP)
  @addr  // RAM[addr] = -1
  A=M
  M=-1
  @addr
  MD=M+1 // addr++; if (addr == KBD) goto INFLOOP
  @KBD
  D=D-A
  @INFLOOP
  D;JEQ

  @FILLLOOP
  0;JMP
