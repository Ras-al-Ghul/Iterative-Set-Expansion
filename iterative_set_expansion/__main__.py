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


    no_of_extracted_tuples = 0
    visited_url = set()
    iter_count = 0;
    while(no_of_extracted_tuples < k):
        print("Query tuple: ", q)
        print("Iteration :", iter_count)
        results = sc.search(q)
        results = [result for result in results if result['url'] not in visited_url]

        sc.extract_content(results)

        for result in results:
            visited_url.add(result['url'])

        ise_results = ise.process(results, r, t)
        for result in ise_results:
            print(result)

        # TODO filter results to remove repeated data
        no_of_extracted_tuples = len(ise_results)

        if(no_of_extracted_tuples < k):
            #TODO extract the top tuple
            q = ise_results[0]['Subject']+ ' ' + ise_results[0]['Object']

        iter_count += 1


if __name__ == '__main__':
    main()