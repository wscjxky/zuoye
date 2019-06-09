//
// Created by xky on 19-5-18.
//
#include "function.h"

int tables_num_arr[PAGE_SIZE];  //用于存页表号的数组
int tables_frame_arr[PAGE_SIZE];   // 用于存页帧的数组
int phy_mem_matrix[FRAMES_COUNT][FRAME_SIZE]; // 物理地址是个二维矩阵，行数为frame数，列数为每个frame大小
int page_faults_count = 0;   // 缺页终端数
int TLB_hit_count = 0;
int TLB_num_arr[TLB_ENTRIES];  // ＴＬＢ中用于存页表号的数组
int TLB_frame_arr[TLB_ENTRIES]; // ＴＬＢ中用于存页帧的数组
int first_free_frame = 0;
int trans_count = 0; //转换次数，也就是行数
int first_free_num = 0;
int TLB_entries = 0;
FILE *input_file = fopen("addresses.txt", "r");;
FILE *backing_store = fopen("BACKING_STORE.bin", "rb");
char address[BUFFER_SIZE];
int logic_address;
char buffer[READ_BUF];


//获取逻辑地址所在的页面
void get_page(int add) {
    // 通过按位于运算得到页序和偏移量，页序取后八位．
    int page_no = ((add & 0xFFFF) >> 8);
    int offset = (add & 0xFF);
    int frame_no = -1;
    int i;
    //先查找ＴＬＢ中是否缓存了该页，如果有就取出，并且ｈｉｔ+1;
    for (i = 0; i < TLB_ENTRIES; i++) {
        if (TLB_num_arr[i] == page_no) {
            frame_no = TLB_frame_arr[i];
            TLB_hit_count++;
        }
    }
    //如果没有就开始去ｔａｂｌｅ中查找．
    if (frame_no == -1) {
        for (i = 0; i < first_free_num; i++) {
            if (tables_num_arr[i] == page_no) {
                frame_no = tables_frame_arr[i];
            }
        }
        if (frame_no == -1) {                   //如果找不到就缺页终端就加１
            get_backstore(page_no);
            page_faults_count++;
            frame_no = first_free_frame - 1;
        }
    }

    insertIntoTLB(page_no, frame_no);  //把新查出的page和frame加入ＴＬＢ中
    cout << "页号：" << page_no << "\t";
    cout << "偏移量：" << offset << "\t";
    cout << "逻辑地址: " << logic_address << "\t";
    //由specfic 可知　offset在低八位，frame_no在高八位
    cout << "物理地址: " << ((frame_no << 8) | offset) << "\t";
    cout << "值: " << phy_mem_matrix[frame_no][offset] << "\n";
}

//采用的是ＦＩＦＯ置换策略
void insertIntoTLB(int page_no, int frame_no) {
    int i;
//    如果已经在ＴＬＢ中存在则退出
    for (i = 0; i < TLB_entries; i++) {
        if (TLB_num_arr[i] == page_no) {
            break;
        }
    }
//    如果表中有就更新
    if (i == TLB_entries) {
        if (TLB_entries < TLB_ENTRIES) {  //　如果有空间则加入
            TLB_num_arr[TLB_entries] = page_no;
            TLB_frame_arr[TLB_entries] = frame_no;
        } else {
            for (i = 0; i < TLB_ENTRIES - 1; i++) {
                TLB_num_arr[i] = TLB_num_arr[i + 1];
                TLB_frame_arr[i] = TLB_frame_arr[i + 1];
            }
            TLB_num_arr[TLB_entries - 1] = page_no;
            TLB_frame_arr[TLB_entries - 1] = frame_no;
        }
    }
//    如果没有就置换添加
    else {
        for (i = i; i < TLB_entries - 1; i++) {
            TLB_num_arr[i] = TLB_num_arr[i + 1];
            TLB_frame_arr[i] = TLB_frame_arr[i + 1];
        }
        if (TLB_entries < TLB_ENTRIES) {
            TLB_num_arr[TLB_entries] = page_no;
            TLB_frame_arr[TLB_entries] = frame_no;
        } else {
            TLB_num_arr[TLB_entries - 1] = page_no;
            TLB_frame_arr[TLB_entries - 1] = frame_no;
        }
    }
    if (TLB_entries < TLB_ENTRIES) {
        TLB_entries++;
    }
}

//产生缺页终端就从ｂａｃｋ.bin中获取匹配的页表．填充这一页的所有frame;
void get_backstore(int page_no) {
//使用ｃ语言自带的ｆｓｅｅｋ函数，定位到页表位置．
    int seek_status = fseek(backing_store, page_no * READ_BUF, SEEK_SET);
    int value = fread(buffer, sizeof(char), READ_BUF, backing_store);
    int i;
//    cout<<page_no;
    for (i = 0; i < READ_BUF; i++) {
        phy_mem_matrix[first_free_frame][i] = buffer[i];

    }
//    cout<<phy_mem_matrix[0][20];
    tables_num_arr[first_free_num] = page_no;
    tables_frame_arr[first_free_num] = first_free_frame;
    first_free_frame++;
    first_free_num++;
}

int main() {
    while (fgets(address, BUFFER_SIZE, input_file) != nullptr) {
//        字节转３２位数字．
        logic_address = atoi(address);
        get_page(logic_address);
        trans_count++;
//        exit(0);
    }
    double page_fault_radio = (double) page_faults_count / (double) trans_count;
    double TLB_hit_radio = (double) TLB_hit_count / (double) trans_count;
    cout << "转换的地址次数：" << trans_count << endl;
    cout << "缺页终端的次数：" << page_faults_count << endl;
    cout << "缺页终端率：" << page_fault_radio << endl;
    cout << "TLB命中次数：" << TLB_hit_count << endl;
    cout << "TLB命中率：" << TLB_hit_radio << endl;
    return 0;
}

