import sys
import threading

import search_scrape as sc
import ise

def print_usage_help():
    print("python3 -m iterative_set_expansion <r> <t> <q> <k>")
    print("r - int with values 1 - Schools_Attended 2 - Work_For 3 - Live_In 4 - Top_Member_Employees")
    print("t - float between 0 and 1 indicating extraction confidence threshold")
    print("q - string seed query of plausible tuple")
    print("k - int greater than 0 indicating number of tuples wanted")

def main():
    if len(sys.argv) < 5 or len(sys.argv) > 5:
        print_usage_help()
        return
    else:
        r, t, q, k = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3], int(sys.argv[4])
        try:
            assert (1 <= int(r) <= 4)
            assert 0 < float(t) < 1
            assert 0 < int(k)
        except:
            print_usage_help()

    print("Query tuple: ", q)
    results = sc.search(q)
    sc.extract_content(results)

    ise.process(results)


if __name__ == '__main__':
    main()