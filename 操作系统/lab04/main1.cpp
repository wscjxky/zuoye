///*
//MUHAMMAD UMAR #gamingumar
//Variable Size Partitioning (Contiguous Allocation) Simulator using C/C++ on Linux.
//A simulation that explores the effects of limited memory
//and memory management based on contiguous allocation.
//Simulator will read information and characteristics of processes
// from input files and then simulate the execution of the processes.
//*/
//#include<iostream>
//#include<string>
//#include<fstream>
//#include<sstream>
//using namespace std;
//bool mem[2000];
//int holeCount;
//int holeSize[2000];
//int holeStart[2000],holeEnd[2000];
//int wait = -4;
//int newHoleStart,newOffset;
//int timer,choice;
//int lastFit = 0;
//int lastSize = 0;
//int finishCount = 0;
//float totalTat = 0;
//int hole(int,string);
//
//
//
//class process		//*** CLASS process ***
//{
//public:
//    process *next;
//
//    int pid,at,life,size;
//    int exeTime,exeStart,exeEnd;
//    int startLoc,endLoc;
//    bool state,finish;
//    float tat;
//
//    process()
//    {
//        tat = 0;
//        finish = 0;
//        state = 0;
//        exeTime = 0;
//        exeEnd = 0;
//        next = NULL;
//    }
//};
//class queue		//*** CLASS QUEUE ***
//{
//public:
//    process *front;
//    process *rear;
//    int count;
//
//    bool queue_empty();
//    void enqueue(int,int,int,int,int,int,bool);
//    void dequeue(int);
//    void update(int,string action);
//    void print(string);
//    int search(int,string action);
//
//    queue()
//    {
//        front = NULL;
//        rear = NULL;
//        count = 0;
//    }
//};
//queue processQ;
//
//
//ofstream output;
//
//// MAIN FUNCTION
//int main()
//{
//    cout<<"\n VARIABLE SIZE PARTITIONING SIMULATOR \n\n";
//
//
//    cout<<"\n 1-> First-Fit Algorithm ";
//    cout<<"\n 2-> Best-Fit Algorithm ";
//    cout<<"\n 3-> Next-Fit Algorithm ";
//    cout<<"\n\tEnter Your Choice==>";
//    cin>>choice;
//
//    switch(choice)
//    {
//        case 1:
//        {
//            cout<<"\n FIRST FIT SIMULATOR \n";
//            output.open("First-Fit-11.txt");
//
//            output<<"\n FIRST FIT SIMULATOR \n";
//            break;
//        }
//        case 2:
//        {
//            cout<<"\n BEST FIT SIMULATOR \n";
//            output.open("Best-Fit-11.txt");
//
//            output<<"\n BEST FIT SIMULATOR \n";
//            break;
//        }
//        case 3:
//        {
//            cout<<"\n NEXT FIT SIMULATOR \n";
//            output.open("Next-Fit-11.txt");
//
//            output<<"\n NEXT FIT SIMULATOR \n";
//            break;
//        }
//        default:
//            cout<<"\n WRONG CHOICE \n";
//    }
//
//    if(choice != 1 && choice != 2 && choice != 3)
//    {
//        return 0;
//    }
//
////	output<<"\n CHKIHNG \n";
//    string dataFile;
//    int totalProcess,count,pro;
//    int pid[10],at[10],life[10],size[10];
//
//    int i,j,data;
//    int mi,mj;
//
////	int from;
//    int loc,offset,tmp;
//
//    int start,exe,finish;
//    int state;
//
//
//    //initializing memory
//    for(i=0;i<2000;i++)
//    {
//        mem[i] = 0;
//    }
//
//
//    ///////////////////////////////////
//
//    for(i=0;i<10;i++)
//    {
//        pid[i] = 0;
//        at[i] = 0;
//        life[i] = 0;
//        size[i] = 0;
//    }
//
//    ifstream file("gp11.txt");
//    // First Entry is total Processess Number
//    file >>totalProcess;
//    //cout<<"Total Process= " <<totalProcess;
//
//    count = 0; pro = 0;
//    while(file >> data)
//    {
//        if(count == 0)
//        {
//            pid[pro] = data;
//            //	cout<<"\nPID = " <<pid[pro];
//        }
//        if(count == 1)
//        {
//            at[pro] = data;
//            file >> data;
//            life[pro] = data;
//            //	cout<<"\nArrival = " <<at[pro];
//            //	cout<<"\nLife life = " <<life[pro];
//        }
//        if(count == 2)
//        {
//            size[pro] = data;
//            //	cout<<"\nAddress Space = " <<size[pro];
//
//            if(size[pro] > 2000)
//            {
//                cout<<"\n PROCESS " <<pid[pro] <<" can't fit in Memory \n";
//                output<<"\n PROCESS " <<pid[pro] <<" can't fit in Memory \n";
//                return 0;
//            }
//
//            count = -1;
//            pro++;
//            //	cout<<endl;
//        }
//        count++;
//        //cout<<"\n " <<data;
//    }
//
//
//    //INSERTING DATA INTO PROCESS QUEUE
//
//    int t = 0;
//    timer = 0;
//    mj = 0;
//    while(true)
//    {
//        t = timer;
//        for(i=0;i<totalProcess;i++)
//        {
//            //Arrival Time
//            if(timer == at[i] && size[i] < 2000)
//            {
//
//                cout<<"\n T = " <<timer;
//                cout<<": Process " <<pid[i] <<" arrives\n";
//                cout<<"\t Input Queue: [ ";
//
//                output<<"\n T = " <<timer;
//                output<<": Process " <<pid[i] <<" arrives\n";
//                output<<"\t Input Queue: [ ";
//                j=0;
//                while(j<=i)
//                {
//                    tmp = processQ.search(pid[j],"finish");
//                    if(tmp == 0)
//                    {
//                        tmp = processQ.search(pid[j],"state");
//                        if(tmp == 0 || t == timer)
//                        {
//                            cout<<pid[j] <<" ";
//
//                            output<<pid[j] <<" ";
//                        }
//                    }
//                    j++;
//                }
//                cout<<"]\n\t Memory map:\n";
//
//                output<<"]\n\t Memory map:\n";
//                hole(0,"showHoles");
//
//
//                //	cout<<"\n------------------------------------";
//                //	cout<<"\n[Timer] = " <<timer;
//                //	cout<<"\n\tPROCESS " <<pid[i] <<" ARRIVES\n";
//                //	cout<<"\t OF SIZE " <<size[i] ;
//                //	cout<<"\n------------------------------------";
//                loc = hole(size[i],"none");
//                //	cout<<"\nLOC= " <<loc;
//
//                if(loc == wait)
//                {
//                    offset = size[i] + holeStart[loc] ;
//                    processQ.enqueue(pid[i],at[i],life[i],size[i],
//                                     holeStart[loc],offset-1,0);
//                }
//                else
//                {
//                    offset = size[i] + holeStart[loc] ;
//                    processQ.enqueue(pid[i],at[i],life[i],size[i],
//                                     holeStart[loc],offset-1,1);
//
//                    if(i==0)
//                    {
//                        //	offset = size[i] + holeStart[loc];
//                        //	cout<<"\nLOC= " <<loc;
//                        //for(mi=holeStart[loc];mi<offset;mi++)
//                        for(mi=0;mi<size[i];mi++)
//                        {
//                            mem[mi] = 1;
//                        }
//
//                        /*		cout<<"\nHole Start= "<<size[i];//holeStart[loc];
//                        cout<<"\nHole End= "<<"1999";//holeEnd[loc];
//                        cout<<"\nHole Size= "<<2000-size[i];//holeSize[loc];
//                        //	cout<<"\nFill Count= "<<holeCount;
//                        cout<<endl;cout<<endl;
//                        */
//                    }
//                    else
//                    {
//                        //	loc = hole(size[i]);
//                        //	tmp = loc;
//                        //	offset = size[i] + holeStart[loc];
//                        //	cout<<"\nLOC= " <<loc;
//                        for(mi=holeStart[loc];mi<offset;mi++)
//                        {
//                            mem[mi] = 1;
//                        }
//
//                        //	loc = hole(size[i]);
//                        /*		cout<<"\nHole Start= "<<holeStart[loc];
//                        cout<<"\nHole End= "<<holeEnd[loc];
//                        cout<<"\nHole Size= "<<holeSize[loc];
//                        //	cout<<"\nFill Count= "<<holeCount;
//                        cout<<endl;cout<<endl;
//                        */
//                    }
//                }
//                //arrival output
//                //	cout<<"\n TIMER= " <<timer;
//                //	processQ.print();
//            }//at close
//
//
//
//            //IF WAITING TIME FINISHES
//
//            //Find holes if fits, then change wait state
//            state = processQ.search(pid[i],"state");
//            finish = processQ.search(pid[i],"finish");
//            //if process is waiting
//            if(state == 0 && finish == 0)
//            {
//                //	cout<<"\n[TIMER]= " <<timer;
//                //	cout<<"\n Process " <<pid[i] <<" is waiting.";
//                loc = hole(size[i],"none");
//                //	cout<<"\n NEW LOC= " <<loc;
//
//                if(loc != wait && timer >= at[i])
//                {
//                    //	cout<<"\n[TIMER]= " <<timer;
//                    //	cout<<"\n Process " <<pid[i] <<" wait finish.";
//                    //	cout<<"\n NEW LOC= " <<loc;
//
//                    //	output<<"\n[TIMER]= " <<timer;
//                    //	output<<"\n Process " <<pid[i] <<" wait finish.";
//                    offset = size[i] + holeStart[loc];
//
//                    newHoleStart = holeStart[loc];
//                    newOffset = offset-1;
//
//                    //	cout<<"\n Process " <<pid[i] <<" State Changed.";
//
//                    //	output<<"\n Process " <<pid[i] <<" State Changed.";
//                    processQ.update(pid[i],"state1");
//
//
//                    for(mi=holeStart[loc];mi<offset;mi++)
//                    {
//                        mem[mi] = 1;
//                    }
//
//                }
//            }
//
//            //IF LIFE TIME HAS EXPIRED
//            exe = processQ.search(pid[i],"exeTime");
//            finish = processQ.search(pid[i],"finish");
//            if(exe == life[i] && finish == 0)
//            {
//                start = processQ.search(pid[i],"none");
//                offset = size[i] + start ;
//                //	cout<<"\n[TIMER] from FINISH= "<<timer;
//                //	cout<<" of Process: " <<pid[i];
//                for(mi=start;mi<offset;mi++)
//                {
//                    mem[mi] = 0;
//                }
//
//                if(i==0)
//                {
//                    processQ.print("fills");
//                }
//                processQ.update(pid[i],"remove");
//
//                cout<<endl;
//                output<<endl;
//                processQ.print("fills");
//
//                cout<<endl<<endl;
//                output<<endl<<endl;
//                hole(0,"showHoles");
//
//                cout<<endl;
//                output<<endl;
//            }
//
//        }// for loop close
//
//        //updating process execution time
//        processQ.update(pid[i],"updateExe");
//
//        processQ.print("finishCount");
//        if(finishCount == totalProcess)
//        {
//            break;
//        }
//
//        timer++;
//    }//while loop close
//    cout<<"\n SUMMARY \n";
//    output<<"\n SUMMARY \n";
//    processQ.print("default");
//    processQ.print("tat");
//
//    cout<<"\n________________________________________\n";
//    cout<<"Average Turnaround: ";
//    cout<<totalTat/totalProcess;
//    cout<<" (" <<totalTat <<"/" <<totalProcess <<")";
//    cout<<"\n----------------------------------------\n";
//
//    output<<"\n________________________________________\n";
//    output<<"Average Turnaround: ";
//    output<<totalTat/totalProcess;
//    output<<" (" <<totalTat <<"/" <<totalProcess <<")";
//    output<<"\n----------------------------------------\n";
//
////	cout<<"\n HOLES NEW \n";
////	hole(0,"showHoles");
//
//    cout<<endl;
//    cout<<"\n [CONTIGUOUS MEMORY ALLOCATION SIMULATION ENDS] \n BY gu...";
//
//    output<<endl;
//    output<<"\n [CONTIGUOUS MEMORY ALLOCATION SIMULATION ENDS] \n BY gu...";
//
//    output.close();
//    return 0;
//}
////MAIN FUNCTION END
//
//
//
//
//bool queue::queue_empty()		//*** QUEUE NULL CHECK ***
//{
//    if(front == NULL && rear == NULL)
//    {
//        return true;
//    }
//    else
//    {
//        return false;
//    }
//}
//
////*** EnQUEUE ***
//void queue::enqueue(int pid,int at,int life,
//                    int size,int startLoc,int endLoc,bool state)
//{
//    process *pnew = new process;
//
//    pnew->pid = pid;
//    pnew->at = at;
//    pnew->life = life;
//    pnew->size = size;
//    pnew->startLoc = startLoc;
//    pnew->endLoc = endLoc;
//    pnew->state = state;
//    pnew->exeStart = timer;
//
//
//    if(queue_empty())
//    {
//        front = pnew;
//        rear  = pnew;
//    }
//    else
//    {
//        rear->next = pnew;
//        rear = pnew;
//    }
//    count++;
//}
//
//
//
//void queue::print(string action)		//*** PRINT ***
//{
//    finishCount = 0;
//    if(queue_empty())
//    {
//        cout<<"\n _______________________________ \n";
//        cout<<"\n         QUEUE IS EMPTY \n";
//        cout<<"\n _______________________________ \n";
//    }
//    else
//    {
//        if(action == "fills")
//        {
//            cout<<"\n _______________________________ ";
//            cout<<"\n  MEMORY MAP [TIMER]= " <<timer;
//            cout<<"\n _______________________________ \n";
//
//            output<<"\n _______________________________ ";
//            output<<"\n  MEMORY MAP [TIMER]= " <<timer;
//            output<<"\n _______________________________ \n";
//        }
//        process *tmp = front;
//        //	cout<<"\n ************* ";
//        //	cout<<"\n Count= " <<count ;
//        //	cout<<"\n _____________ ";
//
//        while(tmp!=NULL)
//        {
//            if(action == "fills")
//            {
//                if((tmp->startLoc + tmp->endLoc) > 0)
//                {
//                    cout<<"\n  " <<tmp->startLoc;
//                    cout<<" - " <<tmp->endLoc;
//                    cout<<": PROCESS " <<tmp->pid ;
//                    //	cout<<endl;
//
//                    output<<"\n  " <<tmp->startLoc;
//                    output<<" - " <<tmp->endLoc;
//                    output<<": PROCESS " <<tmp->pid ;
//                }
//            }
//            if(action == "default")
//            {
//                cout<<"\n Process Number= " <<tmp->pid ;
//                cout<<"\n Arrival Time= " <<tmp->at ;
//                cout<<"\n Life Time in Memory= " <<tmp->life ;
//                cout<<"\n Address Space= " <<tmp->size ;
//                //	cout<<"\n Start Location= " <<tmp->startLoc;
//                //	cout<<"\n End Location= " <<tmp->endLoc;
//                cout<<"\n Execution Time= " <<tmp->exeTime;
//                //	cout<<"\n FINISH= " <<tmp->finish;
//                cout<<"\n Execution START Time= " <<tmp->exeStart;
//                cout<<"\n Execution END Time= " <<tmp->exeEnd;
//
//                output<<"\n Process Number= " <<tmp->pid ;
//                output<<"\n Arrival Time= " <<tmp->at ;
//                output<<"\n Life Time in Memory= " <<tmp->life ;
//                output<<"\n Address Space= " <<tmp->size ;
//                //	output<<"\n Start Location= " <<tmp->startLoc;
//                //	output<<"\n End Location= " <<tmp->endLoc;
//                output<<"\n Execution Time= " <<tmp->exeTime;
//                //	output<<"\n FINISH= " <<tmp->finish;
//                output<<"\n Execution START Time= " <<tmp->exeStart;
//                output<<"\n Execution END Time= " <<tmp->exeEnd;
//
//                tmp->tat = tmp->exeEnd - tmp->at;
//                cout<<"\n Turn Around Time= " <<tmp->tat;
//                cout<<endl;
//
//                output<<"\n Turn Around Time= " <<tmp->tat;
//                output<<endl;
//            }
//            if(action == "tat")
//            {
//                tmp->tat = tmp->exeEnd - tmp->at;
//                totalTat += tmp->tat;
//                //	cout<<"\n TAT= " <<tmp->tat;
//            }
//            if(action == "finishCount")
//            {
//                if(tmp->finish == 1)
//                {
//                    finishCount++;
//                }
//            }
//
//            tmp = tmp->next;
//        }
////		cout<<"\n ************* \n";
//        //	system("PAUSE");
//    }
//}
//
//int queue::search(int pid,string action)
//{
//    process *tmp = front;
//
//    while(tmp != NULL)
//    {
//        if(tmp->pid == pid)
//        {
//            if(action == "exeTime")
//            {
//                return tmp->exeTime;
//                break;
//            }
//            if(action == "state")
//            {
//                return tmp->state;
//                break;
//            }
//            if(action == "finish")
//            {
//                return tmp->finish;
//            }
//            if(action == "none")
//            {
//                return tmp->startLoc;
//                break;
//            }
//
//        }
//
//        tmp = tmp->next;
//    }
////	cout<<"\n Not Found \n";
//
//    return 0;
//}
//
//// ARRAY HOLE FINDER ALGORITHM
//int hole(int size,string action)
//{
//    int i,j,k;
//
//    //initializing
//    for(i=0;i<2000;i++)
//    {
//        holeStart[i] = 0;
//        holeEnd[i] = 0;
//
//        holeSize[i] = 0;
//        //	holes[i] = 0;
//    }
//
//    int freeCount = 0;
//    holeCount = 0;
//    j=k = 0;
//    for(i=0;i<2000;i++)
//    {
//        if(mem[i] == 0)
//        {
//            freeCount++;
//            if(holeSize[j] == 0)
//            {
//                holeStart[j] = i;
//            }
//
//            //	holes[k] = i;
//            //		k++;
//            holeSize[j]++;
//        }
//        else
//        {
//            holeCount++;
//            j++;
//        }
//    }
//    //if whole memory is free then
//    //there is only 1 hole
//    if(freeCount == 2000)
//    {
//        holeCount = 1;
//    }
////	cout<<"\nFree Count= " <<freeCount;
//
//
//    i=0;
//    //cout<<endl;
//    while(i <= holeCount)
//    {
//        //FOR FIRST FIT
//        if(holeSize[i] >= size && action == "none" && choice == 1)
//        {
//            holeEnd[i] = holeSize[i]+holeStart[i]-1;
//
//            return i;
//            break;
//        }
//
//
//        if(action == "showHoles" && holeSize[i] > 0)
//        {
//            holeEnd[i] = holeSize[i]+holeStart[i]-1;
//            cout<<"\t\t";//Hole Size = " <<holeSize[i];
//
//            cout<<holeStart[i] <<" - " <<holeEnd[i];
//            cout<<": HOLE \n";
//
//            output<<"\t\t";//Hole Size = " <<holeSize[i];
//
//            output<<holeStart[i] <<" - " <<holeEnd[i];
//            output<<": HOLE \n";
//
//
//            //cout<<"\nHole Start Location = " <<holeStart[i];
//            //cout<<"\nHole End Location = " <<holeEnd[i];
//            //cout<<endl;
//        }
//
//        i++;
//    }
//    //cout<<endl;
//
//    //FOR BEST FIT
//    if(choice == 2)
//    {
//        int bestSize = 0;
//        int bestLoc = 0;
//
//        i=0;
//        while(i <= holeCount)
//        {
//            if(holeSize[i] >= size && action == "none")
//            {
//                holeEnd[i] = holeSize[i]+holeStart[i]-1;
//
//                bestSize = holeSize[i];
//                bestLoc = i;
//                break;
//            }
//            i++;
//        }
//
//        i=0;
//        while(i <= holeCount)
//        {
//            if(holeSize[i] >= size && action == "none")
//            {
//                if(holeSize[i] < bestSize )
//                {
//                    bestSize = holeSize[i];
//                    bestLoc = i;
//                }
//                holeEnd[i] = holeSize[i]+holeStart[i]-1;
//
//            }
//            i++;
//        }
//        return bestLoc;
//
//    }
//
//    //FOR NEXT FIT
//    if(choice == 3)
//    {
//
//        //	int bestSize = 0;
//        //	int bestLoc = 0;
//        //	int nextSize = 0;
//        //	int nextLoc = 0;
//
//        int found = 0;
//        i=lastFit+lastSize; int chk = 0;i=0;
//        while(i<=holeCount)
//        {
//            if(holeSize[i] >= size && action == "none")
//            {
//                holeEnd[i] = holeSize[i]+holeStart[i]-1;
//                lastFit = i;
//                lastSize = holeSize[i];
//                found = 1;
//                break;
//            }
//            if(chk == 0 && i == holeCount && found == 0)
//            {
//                i=-1;
//                chk = 1;
//                holeCount = lastFit;
//            }
//            i++;
//        }
//        if(found == 1)
//        {
//            return lastFit;
//        }
//    }
//
///*	if(action == "showHoles")
//	{
//		processQ.print("fills");
//	}
//	*///cout<<"\n NOT IN IF\n";
//    return wait; //this is a lock if no hole is found
//
//}
//
//
////*** PROCESS Execution UPDATE ***
//void queue::update(int pid,string action)
//{
//    if(queue_empty())
//    {
//        cout<<"\n _______________________________ \n";
//        cout<<"\n         QUEUE IS EMPTY \n";
//        cout<<"\n _______________________________ \n";
//    }
//    else
//    {
//        process *tmp = front;
//
//        while(tmp!=NULL)
//        {
//
//            if(pid == tmp->pid && action == "remove")
//            {
//                //	cout<<"\n IN REMOVE \n";
//                if(tmp->exeTime == tmp->life)
//                {
//                    cout<<"\n---------------------------------------------\n";
//                    cout<<"\n[Timer] = " <<timer;
//                    cout<<"\n [PROCESS " <<tmp->pid;
//                    cout<<"] Completes.";
//                    cout<<"\n After Execution of ";
//                    cout<<tmp->exeTime;
//                    cout<<" Time Units.\n";
//                    cout<<"\n---------------------------------------------\n";
//
//
//                    output<<"\n---------------------------------------------\n";
//                    output<<"\n[Timer] = " <<timer;
//                    output<<"\n [PROCESS " <<tmp->pid;
//                    output<<"] Completes.";
//                    output<<"\n After Execution of ";
//                    output<<tmp->exeTime;
//                    output<<" Time Units.\n";
//                    output<<"\n---------------------------------------------\n";
//
//                    tmp->startLoc = 0;
//                    tmp->endLoc = 0;
//                    tmp->state = 0;
//                    tmp->finish = 1;
//                    tmp->exeEnd = timer;
//                    break;
//                }
//            }
//            //	cout<<"\n BEFORE UPDATING \n";
//            if(action == "updateExe" && tmp->state == 1 && tmp->finish == 0)
//            {
//                tmp->exeTime += 1;
//            }
//            // update state
//            if(pid == tmp->pid && action == "state1")
//            {
//                tmp->startLoc = newHoleStart;
//                tmp->endLoc = newOffset;
//                tmp->state = 1;
//                tmp->exeStart = timer;
//
//                cout<<"\n State Changed from Function to 1 \n";
//                break;
//            }
//            tmp = tmp->next;
//        }
//    }
//
//}//update function close
//
