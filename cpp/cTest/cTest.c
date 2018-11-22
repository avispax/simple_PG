#include<stdio.h>
#include "cppTest.h"

int main(void) {

	unsigned char URL[100] = "https://10.230.245.12/emsapi/services/PSXAPI/r11_00_00";
	unsigned char user[16] = "admin";
	unsigned char pass[16] = "admin";

	int ccc = UCTest(URL);

	return 0;
}