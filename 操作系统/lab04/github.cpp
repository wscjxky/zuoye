
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <list>
#include <algorithm>


#include "process.hpp"
using namespace std;
// DISPLAY MEM POOL ==============================================================================
void display_mem_pool(vector<char> &mem_pool) {
    int MEM_POOL_SIZE=128;
    int rows = 4;
    int elements_per_row = MEM_POOL_SIZE / rows;

    // 打印分界线
    for (int i = 0; i < elements_per_row; i++)
        cout << '+';

    // 打印内存池
    int i = 0;
    for (auto &pid : mem_pool) {
//        换行
        if (i % elements_per_row == 0)
            cout << endl;
        cout << pid;
        i++;
    }
    cout << '\n';

    // 打印分界线
    for (int i = 0; i < elements_per_row; i++)
        cout << '+';

    cout << endl;
}


// ALPHABETICAL SORT ==============================================================================
bool AB_sort(page_info &a, page_info &b) {
    return (a.ID < b.ID);
}

// DISPLAY PAGES ================================================================================
void display_pages(vector<char> &mem_pool, vector<vector<size_t>> &pages) {
    int elements_per_row = 10;
    // display notice
    cout <<  "PAGE TABLE [page,frame]:\n";

    // sort in alphabetical order
    list<page_info> page_infos;
    for (size_t i = 0; i < pages.size(); i++) {
        page_info temp;
        temp.ID = mem_pool[pages[i][0]];
        temp.index = i;
        page_infos.push_back(temp);
    }
    page_infos.sort(AB_sort);

    // display pages
    list<page_info>::iterator it = page_infos.begin();
    size_t j = 0;
    while (it != page_infos.end()) {
        size_t idx = it->index;
        size_t pg_size = pages[idx].size();
        for (j = 0; j < pg_size; j++) {
            if (j == 0)
                cout << it->ID << ": ";
            else if (j % elements_per_row == 0)
                cout << '\n';

            cout << '[' << j << ',' << pages[idx][j] << ']';


            if ((j+1) % elements_per_row != 0 && j<pg_size-1)
                cout << ' ';
        }
        //if (j % elements_per_row != 0)
        cout << '\n';
        it++;
    }
}

// PARSE INPUT ===================================================================================
void parse_input(ifstream &InputStream, vector<Process> &processes) {

    char pid;
    int mem_frames;
    int arr_time;
    int run_time;
    char delimiter;
    vector<int> arrival_times;
    vector<int> run_times;
    string line;

    // pull a whole line from the input file
    while (getline(InputStream, line)) {

        arrival_times.clear();
        run_times.clear();

        // Ignore commented lines
        if (line[0] == '#') {
            continue;
        }

        stringstream ss(line);

        // first two values are the process ID and the memory frames needed
        ss >> pid >> mem_frames;

        // Then read an indeterminate number of arrival_time/run_time
        while (ss >> arr_time) {
            ss >> delimiter
               >> run_time;

            arrival_times.push_back(arr_time);
            run_times.push_back(run_time);
        }

        processes.push_back(Process(pid, mem_frames, arrival_times.size(), arrival_times, run_times));
    }

}


// MAIN ==========================================================================================
2