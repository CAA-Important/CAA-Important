using System;
using System.IO;
using System.Collections.Generic;

namespace _12_3_Puzzle_A
{
    class Program
    {
        static void Main(string[] args)
        {
            StreamReader input = new StreamReader("C:\\Users\\austi\\Documents\\DevEnvironments\\VS_Code\\C_Sharp_Code\\Advent_of_Code_2020\\12_3_Puzzle_A\\input.txt");
            List<string> inputLines = new List<string>();

            string line = input.ReadLine();

            while(line != null)
            {
                inputLines.Add(line);
                line = input.ReadLine();
            }

            int down = 0;
            int right = 0;
            int treeCount = 0;

            /*while(down < inputLines.Count - 1)
            {
                //down++;
                //right++;

                //down++;
                //right += 3;

                //down++;
                //right += 5;

                //down++;
                //right += 7;

                //down += 2;
                //right++;

                if(right >= inputLines[down].Length)
                {
                    right = right % inputLines[down].Length;
                }

                if(inputLines[down][right].Equals('#'))
                {
                    treeCount++;
                }
            }*/

            Console.WriteLine(191 * 60 * 64 * 63 * 32);
        }
    }
}
