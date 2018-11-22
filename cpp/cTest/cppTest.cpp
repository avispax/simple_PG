#include <string>
#include "cppTest.h"

#include <stdio.h>


//#using "csDll.dll"

using namespace csDll;

extern "C" int cppTestInt()
{

	csDLL^ csdll = gcnew csDLL();
    csdll->helloDLL();
	return 999;
}

extern "C" int UCTest(unsigned char* msg)
{
	//ƒNƒ‰ƒXéŒ¾
	csDLL cs;

	cs.testString = gcnew System::String((char*)msg);
	cs.show_String();

	return 111;
}
