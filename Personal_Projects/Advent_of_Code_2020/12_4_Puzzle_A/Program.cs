using System;
using System.IO;
using System.Collections.Generic;

namespace _12_4_Puzzle_A
{
    class Program
    {
        static bool tester(String input_string){
            String test_string = input_string.Replace("\r\n", " ");
            String[] test_array = test_string.Split(" ");
            if (test_array.Length == 8)
            {
                return true;
            }
            else if(test_array.Length == 7)
            {
                foreach (String test in test_array)
                {
                    String[] test_value = test.Split(":");
                    if(test_value[0] == "cid"){
                        return false;
                    }
                }
                return true;
            }
            else
            {
                return false;
            }
        }

        static void Main(string[] args)
        {
            StreamReader input = new StreamReader("input.txt");
            String input_string = input.ReadToEnd();
            String[] inputs = input_string.Split("\r\n\r\n");
            int input_count = 0;
            int acceptable_input_count = 0;

            foreach (string test_input in inputs)
            {
                input_count++;
                if(tester(test_input))
                {
                    acceptable_input_count++;
                }
            }

            Console.WriteLine(input_count);
            Console.WriteLine(acceptable_input_count);



        }
    }
}
