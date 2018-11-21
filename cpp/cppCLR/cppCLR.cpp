#include "cppCLR.h"

//#using "csDll.dll"

using namespace csDll;

extern "C" int testCppInt()
{

	csDLL^ csdll = gcnew csDLL();
    csdll->helloDLL();
	return 999;
}
