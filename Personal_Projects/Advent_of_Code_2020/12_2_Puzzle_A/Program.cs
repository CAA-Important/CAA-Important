using System;
using System.IO;

namespace _12_2_Puzzle_A
{
    class Program
    {
        static void Main(string[] args)
        {
            string path = Directory.GetCurrentDirectory();
            path += "\\input.txt";

            StreamReader sr = File.OpenText(path);
            string s;
            int numValid = 0;

            while((s = sr.ReadLine()) != null)
            {
                string[] password = s.Split(":");
                string[] password_reqs = password[0].Split(" ");
                string[] password_counts = password_reqs[0].Split("-");
                int lower = Int32.Parse(password_counts[0]);
                int higher = Int32.Parse(password_counts[1]);
                int charCount = 0;
                char requirement = password_reqs[1][0];
                bool valid = true;

                foreach (char c in password[1])
                {
                    if(c.Equals(requirement))
                    {
                        charCount++;

                        if(charCount > higher)
                        {
                            valid = false;
                            break;
                        }
                    }
                }

                if(charCount < lower)
                {
                    valid = false;
                }

                if(valid)
                {
                    numValid++;
                }
            }

            Console.WriteLine(numValid);
        }
    }
}
