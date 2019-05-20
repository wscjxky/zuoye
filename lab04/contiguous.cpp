#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

#include "process.hpp"
using namespace std;
int defrag_time = 0;


// PID SORT ======================================================================================
bool pid_sort(Process &a, Process &b) {
    return a.getPID() < b.getPID();
}


// DEFRAG UPDATE =================================================================================
/* Update the process parameters (end times, start frames, etc.) to account for
    the changes made during defragmentation                                                     */
void defrag_update(vector<char> &mem_pool, vector<Process> &processes, int time_added) {

    // add the time it took to defrag to all arrival times
    for (auto &proc : processes) {
        for (int i = 0; i < proc.getNumBursts(); i++) {
            proc.addToArrTime(i, time_added);
        }
    }


    char prev_frame = '-';
    for (int i = 0; i < MEM_POOL_SIZE; i++) {

        // a new process start was detected
        if (mem_pool[i] != prev_frame) {
            for (auto &proc : processes) {

                // update the start frame of that process
                if (proc.getPID() == mem_pool[i]) {
                    proc.updateStartFrame(i);
                    proc.addToEndTime(time_added);
                }
            }
        }

        prev_frame = mem_pool[i];
    }


}
// DEFRAGMENTATION ===============================================================================
/* Push all processes to the top of memory to make room at the bottom                           */
int defragmentation(vector<char> &mem_pool, Process &proc, int &start_frame) {
    char pid = proc.getPID();
    cout << "ms: Cannot place process " << pid << " -- starting defragmentation\n";

    int total_frames = 0;
    vector<char> moved_frames;
    int start_move = 0;
    int return_loc = 0;
    int free_counter = 0;
    char cache;
    char last_frame_moved = '-';

    int i = 0;
    while (i < MEM_POOL_SIZE) {
        if (mem_pool[i] == '-') {
            // restart the search from here after moving some frames
            return_loc = i;

            // count the size of the free block
            while (i < MEM_POOL_SIZE  &&  mem_pool[i] == '-') {
                free_counter++;
                i++;
            }

            // no more frames to move
            if (i == MEM_POOL_SIZE){
                i = return_loc;
                break;
            }

            start_move = i;

            // move the memory
            while (i < MEM_POOL_SIZE  &&  i < (start_move+free_counter-1)) {

                // Don't move empty frames
                if (mem_pool[i] == '-') break;

                // move the memory
                cache = mem_pool[i];   // cache the memory in that frame
                mem_pool[i] = '-';      // erase the frame
                mem_pool[i-free_counter] = cache;   // write the cached frame to the new location

                i++;
                total_frames++;

                // keep track of which processes had their frames moved
                if (last_frame_moved != cache){
                    last_frame_moved = cache;
                    moved_frames.push_back(last_frame_moved);
                }
            }

            i = return_loc;
            free_counter = 0;

        } else
            i++;
    }

    start_frame = i;

    // update the global clock
    defrag_time += (total_frames * T_MEMMOVE);
    cout << "time " << "ms: Defragmentation complete (moved " << total_frames << " frames:";
    for (size_t i = 0; i < moved_frames.size(); i++) {
        cout << " " << moved_frames[i];
        if (i != moved_frames.size()-1) cout << ",";
    }
    cout << ")\n";
    display_mem_pool(mem_pool);

    // place the new process in memory
    for (; i < start_frame + proc.getNumFrames(); i++)
        mem_pool[i] = pid;


    cout << "ms: Placed process " << pid << ":\n";
    display_mem_pool(mem_pool);

    return true;
}


// SEARCH MEM POOL ===============================================================================
/*  Search the mem pool for the requested space according to the algorithm provided
    return -1 if it is only possible with defragmentation
    return -2 if it is not possible
    otherwise return the starting frame for the available space                                 */
int search_mem_pool(vector<char> &mem_pool, int frames_needed, string algorithm) {

    int total = 0;
    int smallest = MEM_POOL_SIZE+1;
    int largest = 0;

    int free_counter = 0;
    int start_frame = -1;

    int i = 0;
    while (i < MEM_POOL_SIZE) {
        // 如果找到空闲内存.
        if (mem_pool[i] == '-') {

            // 计算需要的快
            while (i < MEM_POOL_SIZE  &&  mem_pool[i] == '-') {
                total++;
                free_counter++;
                i++;
            }

            // 如果算法是ｂｅｓｔ，并且找到了合适的内存则存入
            if (algorithm == "best"  &&  free_counter < smallest  &&  free_counter >= frames_needed) {
                start_frame = i - free_counter;
                smallest = free_counter;

            // 如果算法是ｗｏｒｓｔ，并且找到了合适的内存则存入
            } else if (algorithm == "worst"  && free_counter > largest  && free_counter >= frames_needed) {
                start_frame = i - free_counter;
                largest = free_counter;
            }

            free_counter = 0;


        } else
            i++;
    }

    // 收回内存
    if (start_frame == -1  &&  total >= frames_needed)
        return -1;

    // 没有足够的时间
    else if (start_frame == -1  &&  total < frames_needed)
        return -2;

    // 找到了合适的段
    return start_frame;
}


// PROCESS REMOVAL ===============================================================================
void process_removal(vector<char> &mem_pool, Process &proc) {

    int start = proc.getStartingFrame();
    int frames = proc.getNumFrames();

    for (int i = start; i < start + frames; i++ )
        mem_pool[i] = '-';

    cout << "ms: Process " << proc.getPID() << " removed:\n";
    display_mem_pool(mem_pool);
}


// FIRST FIT ======================================================================================
bool first_fit(string algorithm, vector<char> &mem_pool, vector<Process> &processes,
                       Process &proc, int &start_frame) {

    char pid = proc.getPID();
    int frames_needed = proc.getNumFrames();

    cout << "当前正在处理ｐｉｄ： " << pid << "  (需要的页面数： " << frames_needed<<endl;
    if (frames_needed == 0)
        return false;

    // 使用制定算法创建内存池，返回合适的块
    start_frame = search_mem_pool(mem_pool, frames_needed, algorithm);

    // 销毁回收内存
    if (start_frame == -1) {
        int time_added = defragmentation(mem_pool, proc,  start_frame);
        defrag_update(mem_pool, processes, time_added);
        return true;
    }
        //内存不够
    else if (start_frame == -2) {
        cout << "内存不足退出"<<endl;
        return false;

    } else {
        for (int i = start_frame; i < start_frame + frames_needed; i++) {
            mem_pool[i] = pid;
        }
        cout << "消耗时间 " << "处理完成： " << pid << endl;
        display_mem_pool(mem_pool);
        return true;
    }
}

// BEST FIT ======================================================================================
bool best_or_worst_fit(string algorithm, vector<char> &mem_pool, vector<Process> &processes,
                       Process &proc, int &start_frame) {

    char pid = proc.getPID();
    int frames_needed = proc.getNumFrames();

    cout << "当前正在处理ｐｉｄ： " << pid << "  (需要的页面数： " << frames_needed<<endl;
	if (frames_needed == 0)
		return false;

    // 使用制定算法创建内存池，返回合适的块
    start_frame = search_mem_pool(mem_pool, frames_needed, algorithm);

    // 销毁回收内存
    if (start_frame == -1) {
        int time_added = defragmentation(mem_pool, proc,  start_frame);
        defrag_update(mem_pool, processes, time_added);
        return true;
    }
    //内存不够
    else if (start_frame == -2) {
        cout << "内存不足退出"<<endl;
        return false;

    } else {
        for (int i = start_frame; i < start_frame + frames_needed; i++) {
            mem_pool[i] = pid;
        }
        cout << "消耗时间 " << "处理完成： " << pid << endl;
        display_mem_pool(mem_pool);
        return true;
    }
}

// 计算 =====================================================================================
void simulator(vector<Process> processes, string algorithm) {

    int t = 0;
    defrag_time = 0;
    int remaining_processes = processes.size();

    vector<char> mem_pool(MEM_POOL_SIZE, '-');

    // temporary buffers for when multiple processes are arriving/leaving at the same time
    vector<Process> arriving;
    vector<Process> leaving;

    cout <<"分配机制开始 (算法： " << algorithm << ")"<<endl;

    while (remaining_processes > 0) {

        for (auto &proc : processes) {
//            回收进程 ,如果结束时间为ｔ轮次
            if (!proc.finished()  &&  proc.getEndTime() == t) {
                process_removal(mem_pool, proc);
                proc.removed();
                if (proc.finished())
                    remaining_processes--;
            }

        }
        // 检查是否已经完成
        for (auto &proc : processes) {

            // if a process is arriving at the current time
            if (!proc.finished()  &&  proc.getArrTime( proc.getCurrentBurst() ) == t) {

                bool success;
                int start_frame;

                // attempt to place it; start_frame is guaranteed to be set if success == true
                // t may be changed if defragmentation occurred
                if (algorithm == "Next-Fit")
                    success =true;
//                    success = next_fit(mem_pool, processes, proc, t, start_frame);

                else if (algorithm == "Best-Fit")
                    success = best_or_worst_fit("best", mem_pool, processes, proc, start_frame);

                else if (algorithm == "Worst-Fit")
                    success = best_or_worst_fit("worst", mem_pool, processes, proc, start_frame);


                if (success) {
                    proc.placed(t, start_frame);

                } else {
                    proc.skipped();
                    if (proc.finished())
                        remaining_processes--;
                }
            }
        }
        t++;
    }

}




// CONTIGUOUS MEMORY ALLOCATION ==================================================================
void contiguous_memory_allocation(vector<Process> &processes) {
//    simulator(processes, "First-Fit");
//    cout << "\n";
//
    simulator(processes, "Best-Fit");
    cout << "\n";
//
//	simulator(processes, "Worst-Fit");
//	cout << "\n";
}





