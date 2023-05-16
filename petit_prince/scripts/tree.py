import csv
from treelib import Node, Tree

treeLang = Tree()

with open('tree.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    treeLang.create_node("root", 1)
    for row in reader:
        treeLang.create_node(row['grp'], int(row['i']), parent=int(row['parent']))

treeLang.show()
