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
	//�N���X�錾
	csDLL cs;

	cs.testString = gcnew System::String((char*)msg);
	cs.show_String();

	return 111;
}
