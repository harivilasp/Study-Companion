from googlesearch import search
q = "apple iphone news 2019"

#my_results_list = []
def gsearch(query=q):
    my_results_list=search(query,        # The query you want to run
                    tld = 'com',  # The top level domain
                    lang = 'en',  # The language
                    num = 10,     # Number of results per page
                    start = 0,    # First result to retrieve
                    stop = 10,  # Last result to retrieve
                    pause = 2.0,  # Lapse between HTTP requests
                   )
    return my_results_list
#my_results_list.append(i)

