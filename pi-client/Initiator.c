// Author: Renin Kingsly Jose
// Rev 1.0

#include<stdio.h>
#include<python2.7/Python.h>        // Embedding python API

int main() {
    char* argv[3];
    int argc;
    FILE* fp;

    argc = 3;                       // Argument count

    argv[0] = "piClient.py";        // Python file's name
    argv[1] = "arg1";               // Argument 1
    argv[2] = "arg2";               // Argument 2

    Py_SetProgramName(argv[0]);

	Py_Initialize();

    PySys_SetArgv(argc, argv);

	fp = fopen(argv[0], "r");
	PyRun_SimpleFile(fp, argv[0]);

	Py_Finalize();

	return 0;
}