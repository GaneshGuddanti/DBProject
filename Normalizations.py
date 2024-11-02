import csv
def check_normal_form(csv_filePath, FD, Key, MVD):
    # List of normal form checks in order
    normal_form_checks = [
        ("Not in any Normal Form", lambda: check_1NF(csv_filePath)),
        ("In 1NF", lambda: check_2NF(FD, Key)),
        ("In 2NF", lambda: check_3NF(FD, Key)),
        ("In 3NF", lambda: check_BCNF(FD, Key)),
        ("In BCNF", lambda: check_4NF(FD, Key, MVD)),
        ("In 4NF", lambda: check_5NF(FD, Key, MVD)),
        ("In 5NF", lambda: True)
    ]
    
    # Sequentially check each normal form level
    for form, check in normal_form_checks:
        if not check():
            return form
    return "In 5NF"  # If all checks pass, the table is in 5NF


# Function used to identify if the given table is in First Normal Form (1NF)
def check_1NF(csv_filePath):
    # Opening the csv filepath in read mode
    with open(f'{csv_filePath}', mode ='r')as file:
        csvFile = csv.reader(file)
        res=[]
        # Storing all the data into res Array
        for row in csvFile:
            for i in row:
                res.append(i.split(","))
        # Checking if each value is atomic or not
        for i in res:
            x = str(i)
            # If any element of the list, that is any cell value contains more than a value that means it has a "," the below if statement would be executed.
            if("," in x[2:-2]):
                # The given table NOT in 1NF that is the cell has multiple values for an attribute
                return False 
    # The given table is in 1NF that is all are atomic values
    return True 

# Function used to identify if the given table is in Second Normal Form (2NF)
def check_2NF(FD, Key):
    for i in FD:
        # splitting the functional dependency
        F = i.split("->")
        # if the F[0] has more than 1 element then there is no partial dependency as the attributes is dependent on more than one attribute
        if("," in F[0]):
            continue
        # in A->B if A is not in Key then there would be no partial dependencies
        elif(F[0] not in Key):
            continue
        # in A->B if A is a subset of Key and not the key itself then partial dependency exists 
        elif((F[0] in Key) and (len(F[0]) != len(Key))):
            return False # Partial dependency exists
    return True # No Partial dependency exists

# Function used to identify if the given table is in Third Normal Form (3NF)
def check_3NF(FD, Key):
        
    c_key = ""
    for i in Key:
        c_key += i
    # Outer loop to tranverse through each functional dependency
    for x in FD:
        # Splitting each functional dependency to FD_l and FD_r 
        lhs, rhs = x.split('->')
        l = lhs.strip().split(',')
        FD_l = []
        for i in l:
            FD_l.append(i.strip())
        r = rhs.strip().split(',')
        FD_r = []
        for i in r:
            FD_r.append(i.strip())
        # Inner for loop to traverse through each functional dependency to check if there is a transitive dependency
        for fd in FD:
            # Splitting each functional dependency to FD_ll and FD_rr
            lhs1, rhs1 = fd.split('->')
            l1 = lhs1.strip().split(',')
            FD_ll = []
            for i in l1:
                FD_ll.append(i.strip())
            r1 = rhs1.strip().split(',')
            FD_rr = []
            for i in r1:
                FD_rr.append(i.strip())
            # in the main FD A->B, if A is part of X->A in the second for-each loop and 
            # X is part of key then the transitive dependency exists
            if(FD_l in FD_rr) and (FD_ll in c_key):
                return False # A transitive dependency exists
    return True  # No transitive dependency exists

# Function used to identify if the given table is in Boyce-Codd Normal Form (BCNF)
def check_BCNF(FD, Key):
    for fd in FD:
        l, r = fd.split("->")
        l = l.strip().split(',')
        # checking whether the left hand side of FD is a super key or not
        # return False if not superkey else continue to next iteration of FD
        if set(l).issubset(set(Key)):
            continue
        else:
            return False

    # final return when all the FDs have super keys.
    return True

# Function used to identify if the given table is in Fourth Normal Form (4NF)
def check_4NF(FD, Key, MVD):
    FDs = []
    MVDs = []
    # iterating through each functional dependency
    for fd in FD:
        lhs,rhs = fd.split("->")
        l = lhs.strip().split(',')
        k = []
        for i in l:
            k.append(i.strip())
        r = rhs.strip().split(',')
        for i in r:
            k.append(i.strip())
        # All the elements of a functional dependency are appended to FDs list
        FDs.append(sorted(k))
    mvd_dic = {}
    # Iterating though each Multi-Valued Dependency
    for mvd in MVD:
        lhs,rhs = mvd.split("->>")
        l = lhs.strip().split(',')
        kl = []
        for i in l:
            kl.append(i.strip())
        r = rhs.strip().split(',')
        kr = []
        for i in r:
            kr.append(i.strip())
        if(mvd_dic.get(kl[0])==None):
            mvd_dic[kl[0]] = []
            mvd_dic[kl[0]].extend(kl + kr)
        else:
            mvd_dic[kl[0]].extend(kr)
    for table, attributes in mvd_dic.items():
        # if A->> B and A->> C then [A,B,C] is added to MVDs list
        MVDs.append(sorted(list(set(attributes))))
    # Iterating though each Multi-Valued Dependency in MVDs
    for i in MVDs:
        # Iterating though each Functional Dependency in FDs
        for j in FDs:
            # If MVD is in FD then that means the given MVD is invalid as there is a relation between B and C
            # Else if it is not a subset return False
            if(not set(i).issubset(set(j))):
                return False # Multi-valued dependency exists
    return True # No multi-valued dependency exists

# Function to check if a relation is in Fifth Normal Form (5NF)
def check_5NF(FD, Key, MVD):
    # A table is in 5NF if it is already in 4NF and does not have any additional join dependencies
    # which means all the dependencies in MVD are covered
    if not check_4NF(FD, Key, MVD):
        return False    
    # Check if any join dependencies exist in the MVDs that are not covered by functional dependencies
    for mvd in MVD:
        lhs, rhs = mvd.split("->>")
        l = lhs.strip().split(',')
        r = rhs.strip().split(',')

        # Check if there is a join dependency that requires decomposition
        if not any(set(r).issubset(set(dep_rhs.split(','))) for dep_lhs, dep_rhs in [fd.split("->") for fd in FD] if set(l).issubset(dep_lhs.split(','))):
            return False  # Join dependency requires further decomposition
    
    return True  # No join dependency found, in 5NF

# Function used to convert the given table to First Normal Form (1NF)
def convert_to_1NF(csv_filePath):  
    # Reading the input Database file
    with open(f'{csv_filePath}', mode ='r')as file:
        csvFile = csv.reader(file)
        res = []
        res.append(next(csvFile))
        c = 0
        for row in csvFile:
            x = row
            # storing all the elements of a row into a list.
            # identifies if there is any multiple value
            each_index = [item.split(',') for item in x]
            # identifies the length of each cell, that is the length of each attribute is stored 
            # if atomic then 1, if 2 values then 2 and so on...
            num_elements = [len(sublist) for sublist in each_index]
            # assuming that originally we have 1 value
            total_combinations = 1
            # identifying the total number of combinations that will be formed from the given table.
            # if there are 4 values in a cell then total 4 combinations would be formed.
            for num in num_elements:
                total_combinations *= num
            for i in range(total_combinations):
                # each new row of the table
                new_item = []
                for j in range(len(each_index)):
                    element_index = i % num_elements[j]
                    new_item.append(each_index[j][element_index])
                    i //= num_elements[j]
                res.append(new_item)
        return res

# Function used to convert the given table to Second Normal Form (2NF)
def convert_to_2NF(FD, Key):
    tables = {}
    # travering through each fd
    for fd in FD:
        # Splitting FD to lhs and rhs i.e., left hand side and right hand side of the FD
        lhs, rhs = fd.split('->')
        l = lhs.strip().split(',')
        lhs = []
        for i in l:
            lhs.append(i.strip())
        r = rhs.strip().split(',')
        rhs = []
        for i in r:
            rhs.append(i.strip())
        # If the left hand side of fd is equivalent to Key
        if(sorted(lhs)==sorted(Key)):
            # Create a new table candidate and add all the attributes of Key to it.
            if(tables.get('Candidate')==None):
                tables["Candidate"] = lhs
                tables["Candidate"].extend(rhs)
            else:
                tables["Candidate"].extend(rhs)
        # if lhs is only part of Key then partial dependency exists
        if((len(lhs)==1) and (lhs[0] in Key)):
            # Create a new table - attrobute pair for lhs and it's respective rhs
            if(tables.get(lhs[0])==None):
                tables[lhs[0]] = []
                tables[lhs[0]].extend(lhs + rhs)
            else:
                tables[lhs[0]].extend(rhs) 
            # Append lhs to Candidate so that a relation/common attribute exists between both tables 
            if(tables.get('Candidate')==None):
                tables["Candidate"] = []
                tables["Candidate"].extend(Key + lhs)
            else:
                tables["Candidate"].extend(lhs)
        # if lhs is not part of candidate key, then there is no question of partial dependency
        if((len(lhs)==1) and (lhs[0] not in Key)):
            # adding the fd to Candidate table
            if(tables.get('Candidate')==None):
                tables["Candidate"] = []
                tables["Candidate"].extend(Key + lhs + rhs)
            else:
                tables["Candidate"].extend(lhs + rhs)
        # if lhs is a combination of part of Candidate Key and other attributes
        # there is no partial dependency as the rhs is uniquely identified from lhs
        if(len(lhs)>1):
            if(tables.get('Candidate')==None):
                tables["Candidate"] = []
                tables["Candidate"].extend(Key + lhs + rhs)
            else:
                tables["Candidate"].extend(lhs + rhs)
    check_key = 0
    for table, attributes in tables.items():
        tables[table] = list(set(attributes))
        if(set(sorted(Key)).issubset(set(sorted(attributes)))):
            check_key = 1
    if(check_key == 0):
        tables["Candidate"] = Key
    return tables
# Function used to convert the given table to Third Normal Form (3NF)
def convert_to_3NF(FD, Key, tables):
    new_tables = {}
    lhs_fd = []
    for fd in FD:
        # splitting the left hand side and right hand side elements from each FD.
        lhs, rhs = fd.split('->')
        l = lhs.strip().split(',')
        k = []
        for i in l:
            k.append(i.strip())
        lhs_fd.extend(k)

    for tname, attr in tables.items():
        # checking whether each table name is present in lhs_fd
        # if not present, we check each Functional dependency whether it requires new decomposition or not
        if(tname not in lhs_fd):
            for fd in FD:
                l, r = fd.split("->")
                lhs = l.strip().split(",")
                rhs = r.strip().split(",")
                if(len(lhs) == 1):
                    # checking whether a transitive dependency exists or not
                    if((set(lhs).issubset(set(attr))) and (set(rhs).issubset(set(attr))) and (not set(lhs).issubset(set(Key)))):
                        new_attr = attr
                        for i in rhs:
                            new_attr.remove(i)
                        if(new_tables.get(tname) == None):
                            new_tables[tname] = []
                            new_tables[tname].extend(new_attr)
                        else:
                            new_tables[tname].extend(new_attr)
                        if(new_tables.get(lhs[0]) == None):
                            new_tables[lhs[0]] = []
                            new_tables[lhs[0]].extend(lhs + rhs)
                        else:
                            new_tables[lhs[0]].extend(rhs)

        # if table name is present then adding table directly to a new table.
        elif(tname in lhs_fd):
            new_tables[tname] = attr

    # removing duplicate attributes for each new table.
    for table, attributes in new_tables.items():
        new_tables[table] = list(set(attributes))
    return new_tables

# Function used to convert the given table to Boyce-Codd Normal Form (BCNF)
def convert_to_BCNF(FD, Key, tables):
    new_tables = {}
    count = 0
    #traversing through each functional dependency
    for fd in FD:
        lhs_fd = []
        rhs_fd = []
        lhs, rhs = fd.split('->')
        l = lhs.strip().split(',')
        for i in l:
            lhs_fd.append(i.strip())
        r = rhs.strip().split(',')
        for i in r:
            rhs_fd.append(i.strip())
        # if fd has only 1 attribute on left hand side
        if(len(lhs_fd) == 1):
            # if the table is already available in original table
            if(lhs_fd[0] in tables.keys()):
                # add the same table_name-attribute pair to the new table 
                new_tables[lhs_fd[0]] = tables.get(lhs_fd[0])
            # if the table is not available in original table
            else:
                # create a new table_name-attribute pair and add to the new table
                new_tables[lhs_fd[0]] = []
                new_tables[lhs_fd[0]].extend(rhs_fd)
        elif(len(lhs_fd)>1):
            # if left hand side of the functional dependency is equvivalent to key
            if(sorted(lhs_fd) == sorted(Key)):
                # Add the rhs to the "Candidate" table
                if(new_tables.get('Candidate') == None):
                    new_tables["Candidate"] = []
                    new_tables["Candidate"].extend(Key + rhs_fd)
                else:
                    new_tables["Candidate"].extend(rhs_fd)
            # if left hand side of the functional dependency is not equvivalent to key
            else:
                # Add the lhs to the "Candidate" table so that the relation between new decomposed table and candidate table exists
                if(new_tables.get('Candidate') == None):
                    new_tables["Candidate"] = []
                    new_tables["Candidate"].extend(Key + lhs_fd)
                else:
                    new_tables["Candidate"].extend(lhs_fd)
                # Create a new table-attribute pair denoting a decomposition
                new_tables[count] = []
                new_tables[count].extend(lhs_fd + rhs_fd)
            count += 1
    # travering through each table-attribute pair, to get only distinct attribute pairs in the table
    for table, attributes in new_tables.items():
        c = set()
        for i in attributes:
            c.add(i)
        new_tables[table] = list(c)
    # returning the new resultant table
    return new_tables

# Function used to convert the given table to Fourth Normal Form (4NF)
def convert_to_4NF(FD, Key, MVD, tables):
    # highest integer value in keys in given tables dictionary
    # to get the next integer value for a table name in new tables
    highest_int = 0
    for key in tables.keys():
        if(isinstance(key, int)):
            if(key>highest_int):
                highest_int = key
    new_tables = {}
    mvds = {}
    #traversing through each MVD
    for mvd in MVD:
        # splitting each mvd of MVD to lhs and rhs
        lhs,rhs = mvd.split('->>')
        l = lhs.strip().split(',')
        lhs = []
        for i in l:
            lhs.append(i.strip())
        r = rhs.strip().split(',')
        rhs = []
        for i in r:
            rhs.append(i.strip())
        # Appending all MVDs to mvds dictionary
        if(lhs[0] in mvds.keys()):
            mvds[lhs[0]].extend(rhs)
        else:
            mvds[lhs[0]] = []
            mvds[lhs[0]].extend(lhs+rhs)
    # traversing through each value of MVD dictionary
    for items in mvds.values():
        flag = 0
        # traversing through each relation of tables dictionary
        for attr in tables.values():
            # if the mvd exists in attr that is X->A and X->B if there is a relation (X,A,B) then the MVD is invalid
            if(set(items).issubset(set(attr))):
                flag = 1
    # Merging both original and new dictionary
    merged_dict = {**tables, **new_tables}    

    # travering through each table-attribute pair, to get only distinct attribute pairs in the table
    for table, attributes in merged_dict.items():
        c = set()
        for i in attributes:
            c.add(i)
        merged_dict[table] = list(c)
        
    return merged_dict
# Function to convert the table to Fifth Normal Form (5NF)
def convert_to_5NF(FD, Key, MVD, tables):
    # If the table is already in 5NF, no further decomposition is required.
    if check_5NF(FD, Key, MVD):
        return tables

    # Otherwise, decompose further based on multi-valued dependencies that require decomposition
    new_tables = {}
    table_index = len(tables)
    
    for mvd in MVD:
        lhs, rhs = mvd.split("->>")
        lhs = lhs.strip().split(',')
        rhs = rhs.strip().split(',')

        # Check if there exists a decomposition for this MVD
        for table_name, attrs in tables.items():
            if set(lhs).issubset(set(attrs)) and set(rhs).issubset(set(attrs)):
                # Create a new table for the MVD
                new_table_name = f"Decomposed_{table_index}"
                new_tables[new_table_name] = lhs + rhs
                table_index += 1

                # Remove the decomposed attributes from the original table
                tables[table_name] = [attr for attr in attrs if attr not in rhs]

    # Merge the new decomposed tables with the original tables
    tables.update(new_tables)

    # Remove duplicate attributes in each table
    for table_name, attrs in tables.items():
        tables[table_name] = list(set(attrs))

    return tables
