#include <iostream>
#include <fstream>
#include <istream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

string FilePath = "./xxx.csv";

int main(void)
{
	//逐行读取
	ifstream csv_data(FilePath, ios::in);
	string line;

	if (!csv_data.is_open())
	{
		return 0;
	}
	string row;
	istringstream sin;
	while (getline(csv_data, line))
	{
		sin.clear();
		sin.str(line);
		while (getline(sin, row, ','))
		{
			cout << "逐行输出单个为:" << row << endl;
		}
	}
	csv_data.close();

	//行写入
	ofstream write_csv(FilePath, ios::app);
	if (write_csv.is_open())
	{
		//一次endl为一行
		write_csv << "text" << ","
			<< "text_2" << ","
			<< "text_n" << ","
			<< "text_last" << endl;
	}
	write_csv.close();
}
