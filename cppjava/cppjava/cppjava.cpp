#include "cppjava.h"
#include <jni.h>
#include <iostream>

#pragma comment(lib, "jvm.lib")

using namespace System;

int main()
{
	std::cout << "start cppjava" << std::endl;

	JNIEnv *env;
	JavaVM *vm;
	JavaVMInitArgs vm_args;
	JavaVMOption options[1];
	options[0].optionString = "-Djava.class.path=C:\\work\\MyMain.jar"; // Jar�t�@�C���̏ꏊ

	vm_args.version = JNI_VERSION_1_8;
	vm_args.options = options;
	vm_args.nOptions = 1;

	// JVM�̍쐬
	int result = JNI_CreateJavaVM(&vm, (void **)&env, &vm_args);

	if (result != 0) {
		printf("Fail to create JavaVM (%d).\n", result);
		return 1;
	}
	//MyMain.class�̎擾�i�N���X�p�X��茟���j
	jclass cls = env->FindClass("java_test/MyMain");
	if (cls == 0) {
		printf("Fail to find class\n");
		return 1;
	}
	jmethodID cns = env->GetMethodID(cls, "<init>", "()V");
	if (cns==NULL) {
		printf("Fail to find <init>\n");
		return 1;
	}
	jobject obj = env->NewObject(cls, cns);
	
	jmethodID mj = env->GetMethodID(cls, "getmain", "(Ljava/lang/String[];)Ljava/lang/String[];");
	if (mj==NULL) {
		printf("Fail to call method\n");
		return 1;
	}

	jstring str = (jstring)env->CallObjectMethod(obj, mj, env->NewStringUTF("sssssss"));

	//UTF��char�z��ɕϊ���A�R���\�[���Ɋ֐��̖߂�l���o�́B
	printf("[%s]\n", env->GetStringUTFChars(str, NULL));

	vm->DestroyJavaVM();

	Console::Read();
	return 0;

}

cppjava::cppjava(void)
{

}
