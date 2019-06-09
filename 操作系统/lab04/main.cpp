#include <atomic>
#include <thread>
#include <iostream>
#define OK 1
#define ERROR -1
#include <vector>
using namespace std;
atomic<bool> ready(false);
atomic_flag semaphore = ATOMIC_FLAG_INIT;

int wait(){
    return semaphore.test_and_set();
}
int signal(int id)
{
    while (!ready) {
        this_thread::yield();
    }
    for (int i = 0; i < 1000000; ++i) {
    }
    if (!wait) {
        return OK;
    }
    return OK;
};

int main()
{
    vector<thread> threads;
    for (int i = 1; i <= 10; ++i)
        threads.push_back(thread(signal, i));
    ready = true;
    for (auto & th:threads)
        th.join();
    return 0;
}
//void wait()
//{
//    while (TestAndSet(&guard) == 1);
//    if (semaphore value == 0) {
//        atomically add process to a queue of processes
//        waiting for the semaphore and set guard to 0;
//    }else {
//        semaphore value--;
//        guard = 0;
//    }
//}
//void signal()
//{
//    while (TestAndSet(&guard) == 1);
//    if (semaphore value == 0 &&
//                           there is a process on the wait queue)
//    wake up the first process in the queue
//    of waiting processes
//    else
//    semaphore value++;
//    guard = 0;
//}