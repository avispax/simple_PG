// ConsoleApplication1.cpp : このファイルには 'main' 関数が含まれています。プログラム実行の開始と終了がそこで行われます。
//

#include "pch.h"
#include <iostream>

#include <string>

using namespace cl2;
using namespace std;

int main()
{

	typedef struct {
		unsigned char         port_name[34];
		unsigned char         relative_path_name[258];   // win使用
		short int             duration_switches;
		short int             file_organization;
		short int             maximum_length;            // win使用 delete
		short int             io_type;                   // win使用
		short int             locking_mode;
		short int             access_mode;
		unsigned char         index_name[34];
		unsigned char         full_path_name[258];
		int                   port_id;                   // win使用
		//----- 以下 winで追加する。-------
		long  int             delete_flg;                // win <追加> なし:0 あり:1
		long  int             read_pos;                  // win <追加> 初期:0
		long  int             write_pos;                 // win <追加> 初期:0
	} FILE_PORT_INFO_TYPE;

	static FILE_PORT_INFO_TYPE  som_config_f_info = {
	"som_env_f",                /* port_name         : som_env_f  */
	"aaa",						/* relative_path_name:  SO 環境ﾌｧｲﾙ */
	0,                          /* duration_switches : holdしない */
	3,                          /* file_organization : seq        */
	0,                          /* maximum_length    : ﾚｺｰﾄﾞｻｲｽﾞ  */
	1,                          /* io_type           : input      */
	4,                          /* locking_mode      : implicit   */
	1,                          /* access_mode       : seq        */
	"",                         /* index_name        : なし       */
	"",                         /* full_path_name     (o) */
	0                           /* port_id            (o) */
	};


    cout << "Start C++\n"; 

	Class1 c;

	// 単純呼び出しのタイプ
	c.hello();
	int aaa = c.myInt();
	cout << aaa << endl;

	// 単純に引数を渡すタイプ
	// int
	c.Cl2Int = 999;
	cout << c.Cl2Int << endl;

	//string
	std::string cpp_s = "テスト";
	c.Cs_s = gcnew System::String(cpp_s.c_str());
	c.displayCs_s();

	// 構造体を渡すのに挑戦
	//int bbb = cl2::Class1::soTest(som_config_f_info);
}
