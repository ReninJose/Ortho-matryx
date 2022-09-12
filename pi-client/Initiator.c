// Author: Renin Kingsly Jose
// Rev 1.0

#include<stdio.h>
#include<python2.7/Python.h>        // Embedding python API

int main(int argc, char* argv[]) {
  
    FILE* fp;
    char* name;

    name = "piClient.py";        // Python file's name

    // Do not change anything beyond this line
    Py_SetProgramName(name);
    
    Py_Initialize();

    PySys_SetArgv(argc, argv);
    
    fp = fopen(name, "r");
    PyRun_SimpleFile(fp, name);
    
    Py_Finalize();

	return 0;
}