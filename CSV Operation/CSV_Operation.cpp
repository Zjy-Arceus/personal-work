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
	//���ж�ȡ
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
			cout << "�����������Ϊ:" << row << endl;
		}
	}
	csv_data.close();

	//��д��
	ofstream write_csv(FilePath, ios::app);
	if (write_csv.is_open())
	{
		//һ��endlΪһ��
		write_csv << "text" << ","
			<< "text_2" << ","
			<< "text_n" << ","
			<< "text_last" << endl;
	}
	write_csv.close();
}
