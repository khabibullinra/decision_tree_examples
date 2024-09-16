import dtreevoi
import json 
import matplotlib.pyplot as plt


with open('notebooks/tree_3.json', 'r', encoding='utf-8') as f:
    tree = json.load(f)

dtreevoi.solve_tree(tree)
print('===========================')
#dtreevoi.print_tree(tree)


fig, ax = plt.subplots()

fig.set_figwidth(4)
fig.set_figheight(3)

dtreevoi.plot_tree(tree, ax, 4, 3)

#fig.savefig('test.png')
plt.show()