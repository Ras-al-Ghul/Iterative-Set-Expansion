import sys
import threading

import search_scrape as sc
import ise
import operator

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
    iter_count = 0
    final_result = dict()
    used_queries = []
    #used_queries.append(q)

    while(no_of_extracted_tuples < k):
        print("===============Iteration :", iter_count,"=====================")
        print("Query tuple: ", q)
        results = sc.search(q)
        results = [result for result in results if result['url'] not in visited_url]

        if(len(results) == 0):
            print("All urls visited");
            break;

        print("Extracting and truncating the content to 20,000 characters.")
        sc.extract_content(results)

        for result in results:
            visited_url.add(result['url'])

        ise_results = ise.process(results, r, t)

        for result in ise_results:
            key = (result['Subject'], result['Object'])
            if key in final_result.keys():
                if final_result[key] < result['Confidence']:
                    final_result[key] = result['Confidence']
            else:
                final_result[key] = result['Confidence']


        #print(final_result)
        final_result_sorted = dict(sorted(final_result.items(), key=operator.itemgetter(1), reverse=True))
        no_of_extracted_tuples = len(final_result_sorted)

        #print(final_result_sorted.keys())

        used_queries.append(q)
        for result in final_result_sorted.keys():
            query = ' '.join(result)
            if query not in used_queries:
                q = query
                break

        iter_count += 1

        for result in final_result_sorted:
            print(result, final_result_sorted[result])

if __name__ == '__main__':
    main()