using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;

namespace _12_4_Puzzle_B
{
    class Program
    {
        static bool validator(String[] test_array)
        {
            foreach(string test in test_array)
            {
                String[] test_val = test.Split(":");

                switch(test_val[0])
                {
                    case "byr":
                        if (test_val[1].Length != 4)
                        {
                            return false;
                        }

                        else if (Int32.Parse(test_val[1]) < 1920 || Int32.Parse(test_val[1]) > 2002)
                        {
                            return false;
                        }

                        else
                        {
                            break;
                        }

                    case "iyr":
                        if (test_val[1].Length != 4)
                        {
                            return false;
                        }

                        else if (Int32.Parse(test_val[1]) < 2010 || Int32.Parse(test_val[1]) > 2020)
                        {
                            return false;
                        }

                        else
                        {
                            break;
                        }

                    case "eyr":
                        if (test_val[1].Length != 4)
                        {
                            return false;
                        }

                        else if (Int32.Parse(test_val[1]) < 2020 || Int32.Parse(test_val[1]) > 2030)
                        {
                            return false;
                        }

                        else
                        {
                            break;
                        }

                    case "hgt":
                        String val = test_val[1].Substring(0, test_val[1].Length - 2);
                        String metric = test_val[1].Substring(test_val[1].Length - 2);

                        if (metric == "cm")
                        {
                            if (Int32.Parse(val) < 150 || Int32.Parse(val) > 193)
                            {
                                return false;
                            }
                        }

                        else if (metric == "in")
                        {
                            if (Int32.Parse(val) < 59 || Int32.Parse(val) > 76)
                            {
                                return false;
                            }
                        }

                        else{
                            return false;
                        }

                        break;

                    case "hcl":
                        if (test_val[1][0] != '#')
                        {
                            return false;
                        }

                        else if (test_val[1].Length != 7)
                        {
                            return false;
                        }

                        String char_check = test_val[1].Substring(1, test_val[1].Length - 1);
                        //Could have removed first character and attempted a hex parse.  Parse failure means invalid.
                        char[] legal_chars = {'a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'};

                        foreach (char character in char_check)
                        {

                            if(char_check.Contains(character))
                            {
                                continue;
                            }
                            else
                            {
                                return false;
                            }
                        }
                        break;

                    case "ecl":
                        String[] acceptable_strings = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"};

                        if (acceptable_strings.Contains(test_val[1]))
                        {
                            break;
                        }
                        else
                        {
                            return false;
                        }

                    case "pid":
                        if (test_val[1].Length != 9)
                        {
                            return false;
                        }

                        try
                        {
                            Int32.Parse(test_val[1]);
                        }
                        catch
                        {
                            return false;
                        }

                        break;

                    default:
                        continue;

                


                }
            }

            return true;
        }
        static bool tester(String input_string){
            String test_string = input_string.Replace("\r\n", " ");
            String[] test_array = test_string.Split(" ");
            if (test_array.Length == 8)
            {
                return validator(test_array);
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
                return validator(test_array);
            }
            else
            {
                return false;
            }
        }

        static void Main(string[] args)
        {
            StreamReader input = new StreamReader("..\\12_4_Puzzle_A\\input.txt");
            String input_string = input.ReadToEnd();
            String[] inputs = input_string.Split("\r\n\r\n");
            int input_count = 0;
            int acceptable_input_count = 0;

            foreach (string test_input in inputs)
            {
                input_count++;
                if(tester(test_input))
                {
                    //Console.WriteLine(test_input);
                    //Console.ReadLine();
                    acceptable_input_count++;
                }
            }

            Console.WriteLine(input_count);
            Console.WriteLine(acceptable_input_count);



        }
    }
}
