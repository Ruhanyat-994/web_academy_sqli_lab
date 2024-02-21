import re
pattern = r"[A-Z]+yclone"
text= '''

Related Views

    DBA_TABLES describes all relational tables in the database.
    Cyclone 
    Cyclone 
    Dyclone
    Myclone

    USER_TABLES describes the relational tables owned by the current user. This view does not display the OWNER column.

'''

#match = re.search(pattern,text) # re.search stops in the first match
#print(match)

matchs = re.finditer(pattern,text)
for match in matchs:
    print(text[match.span()[0]:match.span()[1]])