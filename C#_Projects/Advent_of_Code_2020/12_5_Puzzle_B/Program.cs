using System;
using System.IO;

namespace _12_5_Puzzle_B
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

        static int findSeat(int[] seats)
        {
            int lower = 0;
            int higher = seats.Length;
            int[] seat_area = seats;

            while(higher - lower > 1)
            {
                int halfway = higher - ((higher - lower) / 2);
                if(seat_area[halfway] == seat_area[lower] + (halfway - lower))
                {
                    lower = halfway; 
                }
                else{
                    higher = halfway;
                }
            }
            return(seat_area[lower] + 1);
        }

        static void Main(string[] args)
        {
            StreamReader input = new StreamReader("..\\12_5_Puzzle_A\\input.txt");
            String input_string = input.ReadToEnd();
            String[] inputs = input_string.Split("\n");

            int[] ids = new int[inputs.Length];

            for(int i = 0; i < inputs.Length; i++)
            {
                ids[i] = value(inputs[i]);
            }
            
            Array.Sort(ids);

            Console.WriteLine(findSeat(ids));
        }
    }
}

