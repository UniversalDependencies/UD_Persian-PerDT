import os

print("fix_dadegan_deps.py")
os.system("python3 -u fix_dadegan_deps.py")

print("convertNERtoPrn.py")
os.system("python3 -u convertNERtoPrn.py")

print("process_Dadegan_PROPN.py")
os.system("python3 -u process_Dadegan_PROPN.py")

print("dep_tree.py")
os.system("python3 -u dep_tree.py")

print("merge_stanza.py")
os.system("python3 -u merge_stanza.py")

print("tree_checker.py")
os.system("python3 -u tree_checker.py")

print("FINISHED!")