using System;
using System.IO;

namespace _12_5_Puzzle_A
{
    class Program
    {
        static int value(string bin_string)
        {
            string row = bin_string.Substring(0, 7);
            string col = bin_string.Substring(7, 3);

            row = row.Replace("B", "1");
            row = row.Replace("F", "0");

            col = col.Replace("R", "1");
            col = col.Replace("L", "0");




            return (Convert.ToInt32(row, 2) * 8) + Convert.ToInt32(col, 2);
        }

        static void Main(string[] args)
        {
            StreamReader input = new StreamReader("input.txt");
            String input_string = input.ReadToEnd();
            String[] inputs = input_string.Split("\n");

            int max_val = -1;

            foreach(string test_input in inputs)
            {
                int cur_val = value(test_input);
                if(max_val < cur_val)
                {
                    max_val = cur_val;
                }
            }
            Console.WriteLine(max_val);
        }
    }
}
