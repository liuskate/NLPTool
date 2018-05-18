/**************************************************************************
	> File Name: a.cpp
	> Author: liubing
	> Created Time: 四  5/17 17:03:43 2018
 ************************************************************************/

#include<iostream>
#include<vector>
using namespace std;

struct time_unit {
    int start;
    int end;
    string tag;
};



void align_ner_time_tag(const vector<time_unit>& ner_res,  const vector<time_unit>& time_res) {
    vector<time_unit> res;

    size_t ner_idx = 0;
    size_t time_idx = 0;

    size_t ner_res_size = ner_res.size();
    size_t time_res_size = time_res.size();
    cout << "sizes: " << ner_res_size << "  "<< time_res_size << endl;

    for (; ner_idx < ner_res.size(); ner_idx++) {
        //cout << "ner_idx: " << ner_idx << "  "<< res.size() << endl;
        if (ner_res[ner_idx].tag != "O") {
            time_unit unit = ner_res[ner_idx];
            //cout << "11 " << unit.tag << endl;
            res.push_back(unit);
            continue;
        }
        int ner_start = ner_res[ner_idx].start;
        int ner_end = ner_res[ner_idx].end;
        
        // 找到第一个start ≥ ner_start 的item
        while (time_idx < time_res_size && time_res[time_idx].start < ner_start) {
            ++time_idx;
        }
        // 已经到达了time_res结尾 or start ≥ ner_start
        if (time_res[time_idx].start > ner_start || time_idx >= time_res_size) {
            res.push_back(ner_res[ner_idx]);
            continue;
        }
        // start end对齐的情况
        if (ner_end == time_res[time_idx].end) {
            time_unit unit = ner_res[ner_idx];
            unit.tag = "time";
            res.push_back(unit);
            continue;
        }

        // ner_start == time_start && ner_end != time_end
        int time_end = time_res[time_idx].end;
        if (ner_end > time_end) {
            // e.g.  ner: 1号2号  time: 1号/2号
            bool find = false;
            // 发现向后组合time_res，能否达到
            size_t time_i = time_idx + 1;
            for (; time_i < time_res_size; ++time_i) {
                if (time_res[time_i].start != time_res[time_i-1].end
                    || time_res[time_i].end > ner_end) {
                    break;
                } else if (time_res[time_i].end == ner_end) {
                    find = true;
                    break;
                }
            }
            if (find) {
                for (size_t i = time_idx; i <= time_i; ++i) {
                    time_unit unit = time_res[i];
                    res.push_back(unit);
                }
            } else {
                time_unit unit = ner_res[ner_idx];
                res.push_back(unit);
            }
        } else {
            // e.g.  ner: 1号/2号  time: 1号2号
            bool find = false;
            size_t ner_i = ner_idx + 1;
            for (; ner_i < ner_res_size; ++ner_i) {
                if (ner_res[ner_i].tag != "O" ||
                    ner_res[ner_i].end > time_end) {
                    break;
                } else if (ner_res[ner_i].end == time_end) {
                    find = true;
                    break;
                }
            }
            if (find) {
                string text = "";
                for (size_t i = ner_idx; i <= ner_i; i++) {
                    text += "";
                }
                time_unit unit;
                unit.start = ner_res[ner_idx].start;
                unit.end = ner_res[ner_i].end;
                unit.tag = "time";
                res.push_back(unit);
                ner_idx = ner_i;
            } else {
                time_unit unit = ner_res[ner_idx];
                res.push_back(unit);
            }
        }
    }
    // output
    for (size_t i = 0; i < res.size(); i++) {
        cout << res[i].start << " : " << res[i].end << "  " << res[i].tag << endl;
    }
}


int main() {
    vector<time_unit> ner_res;
    vector<time_unit> time_res;
    time_unit t1;
    t1.start = 0;
    t1.end = 1;
    t1.tag = "per";
    ner_res.push_back(t1);

    time_unit t2;
    t2.start = 1;
    t2.end = 3;
    t2.tag = "O";
    ner_res.push_back(t2);

    time_unit t3;
    t3.start = 3;
    t3.end = 5;
    t3.tag = "O";
    ner_res.push_back(t3);

    time_unit t4;
    t4.start = 5;
    t4.end = 6;
    t4.tag = "fm";
    ner_res.push_back(t4);

    time_unit tt1;
    tt1.start = 1;
    tt1.end = 3;
    tt1.tag = "time";
    time_res.push_back(tt1);

    time_unit tt2;
    tt2.start = 3;
    tt2.end = 5;
    tt2.tag = "time";
    time_res.push_back(tt2);

    align_ner_time_tag(ner_res, time_res);
    return 0;
}
