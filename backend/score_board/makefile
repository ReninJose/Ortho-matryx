## Author: Renin Kingsly Jose

CC = /usr/bin/g++
OBJ_NAME = sb

build: sb_generator.cpp
	$(CC) -o $(OBJ_NAME) $^ 

run: $(OBJ_NAME)			## Just in case
	./$^

clean: $(OBJ_NAME)
	rm -f $^

debug:
	make clean
	make build