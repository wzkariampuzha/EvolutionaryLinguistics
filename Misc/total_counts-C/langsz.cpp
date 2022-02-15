#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <set>
#include <cstring>
#include <cstdlib>
#include <algorithm>
#include <functional>
#include <iterator>

int main(int argc, char **argv, int year_to_search)
{
    // Argument parsing
    if (argc != 4)
    {
        std::cerr << "Proper usage is " << argv[0] << " [database file] [output file] [year to search]" << std::endl;
        return -1;
    }

    std::ifstream dbfiles(argv[1]);
    if (!dbfiles)
    {
        std::cerr << "Failed to open database " << argv[1] << " for reading." << std::endl;
    }

    std::ofstream outfile(argv[2]);
    if (!outfile)
    {
        std::cerr << "Failed to open output " << argv[2] << " for writing." << std::endl;
    }

    int count_array[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0}; // array for holding the counts
    int year = year_to_search; 
    int sum = 0;
    int sum_with_x = 0;
    std::string word;
    std::string curr_word;
    std::vector<int> temp_word_datas;
    std::string word_type;
    std::vector<std::string> dbfile_names;
    std::string file_name;
    float progress = 0.0;
    int barwidth =70;

    while (dbfiles)
    {//reading in the file names
        getline(dbfiles, file_name);
        dbfile_names.push_back(file_name);
    }

    dbfiles.close();
    for (unsigned int j = 0; j < dbfile_names.size(); j++)
    {//for every single file

//         std::ifstream dbfile(dbfile_names[j].c_str());
//         std::cout << "currently reading " <<dbfile_names[j] <<std::endl;
// //progress bar code, cause why not
//         std::cout << "[";
//     int pos = barwidth * progress;
//     for (int k = 0; k < barwidth; ++k) {
//         if (k < pos) std::cout << "=";
//         else if (k == pos) std::cout << ">";
//         else std::cout << " ";
//     }
//     std::cout << "] " << int(progress * 100.0) << " %\r";
//     std::cout.flush();

        while (dbfile >> word)
        { //this loads all the word data
            curr_word = word;
            //K'il_NOUN	1749	1	1

            for (int i = 0; i < 4; i++)
            { //now we just fill a vector with the ints
                dbfile >> word;
                int temp = atoi(word.c_str());
                temp_word_datas.push_back(temp);
            } //and *slaps the hood of the map* this bad boy can fit so many vectors
            if (temp_word_datas[0] == year && temp_word_datas[2] > 1)
            {
                word_type = curr_word.substr(curr_word.find('_') + 1);

                if (word_type == "NOUN")
                {
                    count_array[0] = count_array[0] + 1;
                }
                if (word_type == "VERB")
                {
                    count_array[1] = count_array[1] + 1;
                }
                if (word_type == "ADJ")
                {
                    count_array[2] = count_array[2] + 1;
                }
                if (word_type == "ADV")
                {
                    count_array[3] = count_array[3] + 1;
                }
                if (word_type == "PRON")
                {
                    count_array[4] = count_array[4] + 1;
                }
                if (word_type == "DET")
                {
                    count_array[5] = count_array[5] + 1;
                }
                if (word_type == "ADP")
                {
                    count_array[6] = count_array[6] + 1;
                }
                if (word_type == "NUM")
                {
                    count_array[7] = count_array[7] + 1;
                }
                if (word_type == "CONJ")
                {
                    count_array[8] = count_array[8] + 1;
                }
                if (word_type == "PRT")
                {
                    count_array[9] = count_array[9] + 1;
                }
                if (word_type == "X")
                {
                    sum_with_x += 1;
                }
            }

            // c_word_data_data.insert(std::pair<std::string, std::vector<int>>(curr_word, temp_word_datas));
            temp_word_datas.clear(); // clean up a bit so we can recycle
            continue;
        }
        dbfile.close();
        progress += .034;
    }
    std::cout.flush();


    // protype count print
    outfile << "There are " << count_array[0] << " _NOUN_'s in the year " << year << std::endl;
    outfile << "There are " << count_array[1] << " _VERB_'s in the year " << year << std::endl;
    outfile << "There are " << count_array[2] << " _ADJ_'s in the year " << year << std::endl;
    outfile << "There are " << count_array[3] << " _ADV_'s in the year " << year << std::endl;
    outfile << "There are " << count_array[4] << " _PRON_'s in the year " << year << std::endl;
    outfile << "There are " << count_array[5] << " _DET_'s in the year " << year << std::endl;
    outfile << "There are " << count_array[6] << " _ADP_'s in the year " << year << std::endl;
    outfile << "There are " << count_array[7] << " _NUM_ 's in the year " << year << std::endl;
    outfile << "There are " << count_array[8] << " _CONJ_'s in the year " << year << std::endl;
    outfile << "There are " << count_array[9] << " _PRT_'s in the year " << year << std::endl;

    outfile << std::endl;
    for (int i = 0; i < 10; i++)
    {
        sum += count_array[i];
        sum_with_x += count_array[i];
    }
    outfile << "There are " << sum << " words overall in the year " << year << " with volume greater than or equal to 2" << std::endl;
    outfile << "And there are " << sum_with_x << " words, when including the _X tag" << std::endl;

    outfile.close();
    return 0;
}
