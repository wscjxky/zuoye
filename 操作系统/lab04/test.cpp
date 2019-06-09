///// COP3503 Progamming Assignment 2:
//
//#include <iostream>
//using namespace std;
//
//struct node{
//    int number;
//    int count;
//    string name;
//    node * next;
//
//};
//
//class LinkedList{			//creating linked list and calling functions
//
//private:
//    node * head;
//
//public:
//    LinkedList(){
//        head = nullptr;
//    }
//
//    void createMemory();
//    void print();
//    void insertion(int numb, int numbPages);
//    void removal(int number, int numbPages);
//    int counter();
//
//};
//
//void LinkedList::createMemory(){			//make 32 free nodes
//
//    head = new node;
//    node * temp = head;
//    for(int i = 0; i < 32; i++){
//        temp->name = "FREE";
//        temp->next = new node;
//        temp = temp->next;
//    }
//    temp->next = nullptr;
//}
//
//void LinkedList::print(){					//print out 32 free nodes to start
//
//    node * temp = head;
//    string t;
//    for(int i = 0; i < 32; i++){
//        t = temp->name;
//        cout << t << '\t';
//        temp = temp->next;
//        if((i+1)%8 == 0) {					//if there are 8 values in a row then create a new row
//            cout << endl;
//        }
//    }
//}
//
//int menu(){
//
//    int choice;								//creating menu to dispay options to be selected
//
//    cout << "\nMenu:\n";
//    cout << "1. Add Program\n";
//    cout << "2. Kill Program\n";
//    cout << "3. Fragmentation\n";
//    cout << "4. Print\n";
//    cout << "5. Exit";
//    cout << "\nChoice: ";
//
//    cin >> choice;
//    return choice;
//
//}
//
//int LinkedList::counter(){
//
//    int count = 0;							//setting the count(fragment) = to 0
//    bool fragment = true;
//    node * temp = head;
//    while(temp != nullptr){					// index whole linked list
//        if(temp -> name == "FREE" && fragment){
//            count++;
//            fragment = false;				//if the node is free and boolean is true then add one to count
//
//        }
//
//        if(temp -> name != "FREE" && !fragment){
//            fragment = true;				//if the node value is not free then do not add to count, move to next node
//        }
//
//        temp = temp -> next;				//move to next value in list
//    }
//    return count;
//    cout << count;
//}
//
//void LinkedList::insertion(int number, int numbPages){
//
//    node * temp = head;
//    while(temp -> name != "FREE"){				//if node alrady contains a program, move to next
//        temp = temp->next;
//    }
//    string nodeName = "P" + to_string(number);
//
//    for(int i = 0; i < numbPages; i++){
//
//        temp -> name = nodeName;				//set the node = program name when input is received
//        temp = temp -> next;
//    }
//};
//
//void LinkedList::removal(int number, int numbPages){
//
//    node * temp = head;
//    while(temp -> name != ("P" + to_string(number))){		//if the node is not equal to program then move to the next
//        temp = temp->next;
//    }
//    string nodeName = "FREE";
//
//    for(int i = 0; i < numbPages; i++){						//replace the node with free if program is found then move to next
//
//        temp->name = nodeName;
//        temp = temp -> next;
//    }
//}
//
//int main(){
//
//    node * head = NULL;
//    node * last = NULL;
//
//    LinkedList program;					//creating/naming linked list
//    LinkedList FREE;
//    program.createMemory();
//    FREE.createMemory();
//
//    int choice = 0;
//    int number;
//    int numbPages;
//
//    while(choice != 5){					//what to do if input is not quit
//
//        choice = menu();				//create the menu
//
//        switch(choice){
//            case 1:	cout << "\nProgram Name: P";			//if input is to add call the insertion method add programs
//                cin >> number;
//                cout << "Program Size (KB): ";
//                int programSize;
//                cin >> programSize;
//                if(programSize % 4 == 0){				//if progarm size is divisible by 4 then add that many pages
//                    numbPages = programSize / 4;
//                }
//                else{
//                    numbPages = (programSize / 4) + 1;		//if program size is not divisible by 4 then round up to create whole pages
//                }
//                FREE.insertion(number, numbPages);
//                cout << "Program P" << number << " added succesfully: " << numbPages << " page(s) used.\n";
//                break;
//
//            case 2:	cout << "Program Name: P";				//if input is to kill program then call removal
//                cin >> number;
//                FREE.removal(number, numbPages);
//                cout << "Program P" << number << " succesfully killed, " << numbPages << " page(s) reclaimed.\n";
//                break;
//
//            case 3:	cout << "There are " << FREE.counter() << " fragment(s)\n";  //call counter to determine fragemnt(s)
//                break;
//
//            case 4:	FREE.print();			//call print function
//                break;
//
//            case 5:	cout << "Program Exit\n";   //end program
//                break;
//        }
//
//    }
//
//    return(0);
//}