# Simple Makefile for the Unix Engine
CC = gcc
CFLAGS = -Iinclude
SRC = main.c src/calculator.c
OBJ = $(SRC:.c=.o)
TARGET = app.out

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET)

clean:
	rm -f $(SRC:.c=.o) $(TARGET)
