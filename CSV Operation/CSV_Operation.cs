using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;

public class Class
{
    //针对在unity中实现读写
    private string filePath = "Assets/xxx.csv";
    private StreamReader SR;
    private StreamWriter SW;

    void Main()
	{
        if(File.Exists(filePath))
        {
            //逐行读取
            SR = new StreamReader(filePath);
            string line = SR.ReadLine(); //读取表头
            while(!SR.EndOfStream)
            {
                line = SR.ReadLine();
                string[] row = line.Split(',');
                foreach(string data in row)
                {
                    Console.WriteLine("逐行读取单个为：" + data);
                }
            }
            SR.Close();

            //逐行写入
            SW = new StreamWriter(filePath);
            SW.WriteLine("title, title2, titleN");
            SW.WriteLine("text1, text2, textN");
            SW.Flush();
            SW.Close();
        }
    }
}
