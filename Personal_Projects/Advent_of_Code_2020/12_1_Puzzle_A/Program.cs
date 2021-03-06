using System;
using System.IO;

namespace _12_1_Puzzle_A
{
    class Program
    {
        static int Solution(int toSum, int[] sortedNumbers)
        {
            int left = 0;
            int right = sortedNumbers.Length - 1;

            while(sortedNumbers[left] + sortedNumbers[right] != toSum)
            {
                if(left > right)
                {
                    return -1;
                }

                if(sortedNumbers[left] + sortedNumbers[right] > toSum){
                    right--;
                }
                else
                {
                    left++;
                }
            }

            return(sortedNumbers[left] * sortedNumbers[right]);

        }


        static void Main(string[] args)
        {
            string path = Directory.GetCurrentDirectory();
            path += "\\input.txt";

            StreamReader sr = File.OpenText(path);
            string s;
            string numberString = "";

            while((s = sr.ReadLine()) != null)
            {
                numberString += s + ";";
            }

            numberString = numberString.Substring(0, numberString.Length - 1);

            string[] numberStringList = numberString.Split(";");

            int[] numberList = new int[numberStringList.Length];

            for(int i = 0; i < numberStringList.Length; i++)
            {
                numberList[i] = Int32.Parse(numberStringList[i]);
            }

            Console.WriteLine(Solution(2020, MergeSorter.MergeSort(numberList)));

            //int[] temp = {1721, 979, 366, 299, 675, 1456};
            //int[] sorted = MergeSorter.MergeSort(temp);
            //Console.WriteLine(Solution(2020, sorted));
            //string sorted_string = "";
            //for(int i = 0; i < sorted.Length; i++)
            //{
            //    sorted_string += sorted[i] + " ";
            //}
            //Console.WriteLine(sorted_string);
        }
    }

    public class MergeSorter
    {
        static int[] Merge(int[] a, int[] b)
        {
            int[] merged = new int[a.Length + b.Length];
            int a_index = 0;
            int b_index = 0;
            int merged_index = 0;

            while((a_index < a.Length) && (b_index < b.Length))
            {
                if(a[a_index] < b[b_index])
                {
                    merged[merged_index] = a[a_index];
                    a_index++;
                }

                else
                {
                    merged[merged_index] = b[b_index];
                    b_index++;
                }
                merged_index++;
            }

            if(a_index < a.Length)
            {
                for(int i = a_index; i < a.Length; i++)
                {
                    merged[merged_index] = a[i];
                    merged_index++;
                }
            }

            else
            {
                for(int i = b_index; i < b.Length; i++)
                {
                    merged[merged_index] = b[i];
                    merged_index++;
                }
            }

            return(merged);
        }

        public static int[] MergeSort(int[] toSort){
            if(toSort.Length == 1){
                return toSort;
            }

            int[] a = new int[(int)Math.Floor(toSort.Length / 2.0)];
            int[] b = new int[(int)Math.Ceiling(toSort.Length / 2.0)];

            for(int i = 0; i < a.Length; i++)
            {
                a[i] = toSort[i];
            }

            for(int i = 0; i < b.Length; i++)
            {
                b[i] = toSort[i + a.Length];
            }

            return Merge(MergeSort(a), MergeSort(b));

        }
    }
}
