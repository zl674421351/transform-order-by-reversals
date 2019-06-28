import sys
import subprocess
import itertools

def skeleton():
    # input parsing for only P2 now
    raw_list = sys.argv[1:]
    if len(raw_list) == 0 or len(raw_list) == 1 or len(raw_list) == 2:
        print("Please enter a destination list of more than 2 integers.")
        return
    if set([str(i) for i in list(range(1,len(raw_list)+1))]) != set(raw_list):
        print("Your destination list is not valid.")
        return
    dest_list = [int(i) for i in raw_list]
    n = len(dest_list)
    # creating the cnf file.
    cnf_path = 'temp.cnf'
    cnf_file = open(cnf_path,'x')
    cnf_file.close()
    num_of_lines = 0
    num_of_lines += f1(dest_list,cnf_path)
    num_of_lines += f2(dest_list,cnf_path)
    num_of_lines += f3(dest_list,cnf_path)
    num_of_lines += f4(dest_list,cnf_path)
    num_of_lines += f5(dest_list,cnf_path)
    num_of_lines += f6(dest_list,cnf_path)
    num_of_lines += f7(dest_list,cnf_path)
    num_of_lines += f8(dest_list,cnf_path)
    num_of_lines += f9(dest_list,cnf_path)
    header(dest_list,cnf_path,num_of_lines + 1)
    if nop_k(1,dest_list,cnf_path):
        print ("No operation needed (min).")
    else:
        if not nop_k(n-1,dest_list,cnf_path):
            print (str(n-1) + " operations needed (max).")
        else:
            print(str(search_k(1,n-1,dest_list,cnf_path)) + " operations needed.")
    subprocess.run(["rm","temp.cnf"])


def header(dest_list,cnf_path,num_of_clauses):
    n = len(dest_list)
    num_of_vars = 0
    # X[k : 1 to n-1][i : 1 to n][p : 1 to n][q : 1 to n]
    num_of_vars += pow(n,4)-pow(n,3)
    # R[p : 1 to n][q : 1 to n][k : 1 to n-1]
    num_of_vars += pow(n,3)-pow(n,2)
    # NOP : 1 to n-1
    num_of_vars += n - 1
    line_prepender(cnf_path,"p cnf "+str(num_of_vars)+" "+str(num_of_clauses))


def line_prepender(cnf_path, line):
    # https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
    with open(cnf_path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def x_index(k,i,p,q,n):
    return (k-1)*pow(n,3) + (i-1)*pow(n,2) + (p-1)*n + q


def r_index(p,q,k,n):
    return (p-1)*(n*n-n) + (q-1)*(n-1) + k + pow(n,4)-pow(n,3)


def nop_index(k,n):
    return pow(n,4)-pow(n,2) + k


def f1(dest_list,cnf_path):
    n = len(dest_list)
    cnf_file = open(cnf_path,'a')
    #cnf_file.write("f1_line\n")
    clause_count = 0
    for k in range(1,n):
        var_list = []
        var_list.append(nop_index(k,n))
        for p in range(1,n):
            for q in range(p+1,n+1):
                var_list.append(r_index(p,q,k,n))
        # all items in the first line
        for elem in var_list:
            cnf_file.write(str(elem)+" ")
        cnf_file.write("0\n")
        clause_count += 1
        # all pairs of neg elem
        for pair in itertools.combinations(var_list,2):
            cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
            clause_count += 1
    cnf_file.close()
    return clause_count


def f2(dest_list,cnf_path):
    n = len(dest_list)
    cnf_file = open(cnf_path,'a')
    #cnf_file.write("f2_line\n")
    clause_count = 0
    for i in range(1,n+1):
        var_list = []
        for q in range(1,n+1):
            var_list.append(x_index(1,i,i,q,n))
        # all items in the first line
        for elem in var_list:
            cnf_file.write(str(elem)+" ")
        cnf_file.write("0\n")
        clause_count += 1
        # all pairs of neg elem
        for pair in itertools.combinations(var_list,2):
            cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
            clause_count += 1
    cnf_file.close()
    return clause_count


def f3(dest_list,cnf_path):
    n = len(dest_list)
    cnf_file = open(cnf_path,'a')
    #cnf_file.write("f3_line\n")
    clause_count = 0
    for i in range(1,n+1):
        var_list = []
        for p in range(1,n+1):
            var_list.append(x_index(n-1,i,p,dest_list.index(i)+1,n))
        # all items in the first line
        for elem in var_list:
            cnf_file.write(str(elem)+" ")
        cnf_file.write("0\n")
        clause_count += 1
        # all pairs of neg elem
        for pair in itertools.combinations(var_list,2):
            cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
            clause_count += 1
    cnf_file.close()
    return clause_count


def f4(dest_list,cnf_path):
    n = len(dest_list)
    cnf_file = open(cnf_path,'a')
    #cnf_file.write("f4_line\n")
    clause_count = 0
    for k in range(2,n):
        for q in range(1,n+1):
            var_list = []
            for p in range(1,n+1):
                for i in range(1,n+1):
                    var_list.append(x_index(k-1,i,p,q,n))
            # all items in the first line
            for elem in var_list:
                cnf_file.write(str(elem)+" ")
            cnf_file.write("0\n")
            clause_count += 1
            # all pairs of neg elem
            for pair in itertools.combinations(var_list,2):
                cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
                clause_count += 1
    cnf_file.close()
    return clause_count


def f5(dest_list,cnf_path):
    n = len(dest_list)
    cnf_file = open(cnf_path,'a')
    #cnf_file.write("f5_line\n")
    clause_count = 0
    for k in range(2,n):
        for p in range(1,n+1):
            var_list = []
            for q in range(1,n+1):
                for i in range(1,n+1):
                    var_list.append(x_index(k,i,p,q,n))
            # all items in the first line
            for elem in var_list:
                cnf_file.write(str(elem)+" ")
            cnf_file.write("0\n")
            clause_count += 1
            # all pairs of neg elem
            for pair in itertools.combinations(var_list,2):
                cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
                clause_count += 1
    cnf_file.close()
    return clause_count


def f6(dest_list,cnf_path):
    n = len(dest_list)
    cnf_file = open(cnf_path,'a')
    #cnf_file.write("f6_line\n")
    clause_count = 0
    for k in range(2,n):
        for i in range(1,n+1):
            for p in range(1,n+1):
                var_list_1 = []
                var_list_2 = []
                for q in range(1,n+1):
                    var_list_1.append(x_index(k-1,i,q,p,n))
                    var_list_2.append(x_index(k,i,p,q,n))
                # first part
                first_string = ""
                for var in var_list_1:
                    first_string += str(var) + " "
                for var in var_list_2:
                    cnf_file.write(first_string+" -"+str(var)+" 0\n")
                    clause_count += 1
                # second part
                second_string = ""
                for var in var_list_2:
                    second_string += str(var) + " "
                for var in var_list_1:
                    cnf_file.write(second_string+" -"+str(var)+" 0\n")
                    clause_count += 1
    cnf_file.close()
    return clause_count


def f7(dest_list,cnf_path):
    n = len(dest_list)
    cnf_file = open(cnf_path,'a')
    #cnf_file.write("f7_line\n")
    clause_count = 0
    for k in range(1,n):
        for w in range(1,n+1):
            var_list_1 = []
            var_list_2 = []
            for i in range(1,n+1):
                var_list_1.append(x_index(k,i,w,w,n))
            var_list_2.append(nop_index(k,n))
            for p in range(1,n):
                for q in range(p+1,n+1):
                    if 2*w == p + q:
                        var_list_2.append(r_index(p,q,k,n))
                    if p < w and q < w:
                        var_list_2.append(r_index(p,q,k,n))
                    if p > w and q > w:
                        var_list_2.append(r_index(p,q,k,n))
            second_string = ""
            for var in var_list_2:
                second_string += str(var) + " "
            for var in var_list_1:
                cnf_file.write(second_string+" -"+str(var)+" 0\n")
                clause_count += 1
    cnf_file.close()
    return clause_count


def f8(dest_list,cnf_path):
    n = len(dest_list)
    cnf_file = open(cnf_path,'a')
    #cnf_file.write("f8_line\n")
    clause_count = 0
    for k in range(1,n):
        for w in range(1,n+1):
            for z in range(1,n+1):
                if z == w:
                    continue
                var_list_1 = []
                var_list_2 = []
                for i in range(1,n+1):
                    var_list_1.append(x_index(k,i,w,z,n))
                a = min(w,z)
                b = max(w,z)
                for p in range(1,n):
                    for q in range(p+1,n+1):
                        if a-p == q-b and a-p <= min(a-1,n-b):
                            var_list_2.append(r_index(p,q,k,n))
                second_string = ""
                for var in var_list_2:
                    second_string += str(var) + " "
                for var in var_list_1:
                    cnf_file.write(second_string+" -"+str(var)+" 0\n")
                    clause_count += 1
    cnf_file.close()
    return clause_count


def f9(dest_list,cnf_path):
    n = len(dest_list)
    cnf_file = open(cnf_path,'a')
    #cnf_file.write("f9_line\n")
    for k in range(1,n-1):
        cnf_file.write(str(nop_index(k+1,n))+" -"+str(nop_index(k,n))+" 0\n")
    cnf_file.close()
    return n-2


def search_k(start,end,dest_list,cnf_path):
    if end - start == 2:
        if nop_k(start + 1,dest_list,cnf_path) and nop_k(end,dest_list,cnf_path):
            return start
        else:
            return start + 1
    if end - start == 1:
        return start
    left_one = nop_k(int((start+end)/2),dest_list,cnf_path)
    right_one = nop_k(int((start+end)/2)+1,dest_list,cnf_path)
    if left_one == False and right_one == True:
        return int((start+end)/2)
    if left_one == False and right_one == False:
        return search_k(int((start+end)/2)+1,end,dest_list,cnf_path)
    if left_one == True and right_one == True:
        return search_k(start,int((start+end)/2),dest_list,cnf_path)
    print("Should not get here.")
    return "Nothing"


def nop_k(k,dest_list,cnf_path):
    subprocess.run(["cp","temp.cnf","temp_ongoing.cnf"])
    n = len(dest_list)
    cnf_file = open("temp_ongoing.cnf",'a')
    cnf_file.write(str(nop_index(k,n))+" 0\n")
    cnf_file.close()
    result = subprocess.run(["../sat_solver/lingeling","temp_ongoing.cnf"],capture_output=True).stdout
    subprocess.run(["rm","temp_ongoing.cnf"])
    if b'UNSATISFIABLE' in result:
        return False
    else:
        return True


def k_result_parser():

    return 1


skeleton()
