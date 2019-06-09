//
// Created by xky on 19-5-18.
//

#ifndef LAB05_FUNCTION_H
#define LAB05_FUNCTION_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <alloca.h>
#include <iostream>

using namespace std;
//定义实验的标准参数
const int FRAME_SIZE = 256;
const int FRAMES_COUNT = 256;
const int TLB_ENTRIES = 16;
const int PAGE_SIZE = 256;
const int BUFFER_SIZE = 10;
const int READ_BUF = 256;

void get_page(int logic_address);

void get_backstore(int page_no);

void insertIntoTLB(int page_no, int frame_no);

#endif //LAB05_FUNCTION_H
