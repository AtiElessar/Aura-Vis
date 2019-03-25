# Aura-Vis
AURA-Vis (AUthoritzation gRAph Visualizer) is a Python tool which allows users to view the authorization graph (/grant diagram) for some given SQL statements.

## Downloading the script
Clone the repository and install the dependencies.
Dependencies are : [Matplotlib](https://matplotlib.org/users/installing.html) and [NetworkX](https://networkx.github.io/)

## Running the script
Run AuraVis.py (by command line, IDLE etc.)

1. The first input you will be asked is a file path to the file which stores the SQL statements. These SQL statements will be of the following format:
    `<user writing the statement> <A valid grant/revoke statement>`

    For example, if the user "A" is writing the statement `grant select on DB to  B;` then the corresponding statement in the input file will be:
    `A grant select on DB to  B;`

    Your input file should just be a bunch of these semi-colon seperated statements (may or may not be on different lines).
    Example - 
    `A grant select on DB to B,C;
    B grant select on DB to D,E;
    D grant select on DB to F,G;
    C grant select on DB to H;
    A revoke select on DB from B restrict;`

2. After entering the input file path, you will be asked the details of the graph you want to see. 
    * Database name - The name of the database
    * Priviledge type - The priviledge types are select, update etc.
    * Column/attribute name - For certain priviledges (like update) you can specify an attribute as well (assuming that you have used attributes in your input file as well).
        * If you do not want to specify an attribute, just hit enter when asked for it.

3. After this it will output the required graph.

### Note
1. The script assumes that your input statements follow proper SQL syntax. If they don't then the script will cause an error or give a wrong output.
2. Since the script is not taking the schemas of the relations, it does not know the attributes of each relation. Therefore cases like the following example do not work properly:
    `A grant update on DB to B; 
     A revoke update(att1) on DB from B restrict;` 
     In the statements, A grants update access on all attributes to B but only revokes on one attribute. The program will not be able to handle such cases for any combination of grant and/or revoke statements. Therefore, if you are granting/revoking over only one attribute (or the entire relation), please be consistent.
3. The code is case-insensitive for user, relation and attribute names.
