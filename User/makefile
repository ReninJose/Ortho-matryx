CC=/usr/bin/g++
CFLAGS=-I.
DEPS=User.h
OBJ=User.o

%.o: %.c
	$(CC) -c -o $@ $^ $(CFLAGS)

build: $(OBJ) $(DEPS) 
	$(CC) -o User $^ $(CFLAGS)
	
run:
	./User $(COMMAND)

clean: 
	rm -f User 

debug:
	make clean
	make build
	make run