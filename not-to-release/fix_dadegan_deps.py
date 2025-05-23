"""
* Fix "wa"s that are tagged as SUBR
* Change wrong dependencies in PARCL.
* Change VConj order.
* Convert active to passive for Shodan verbs.
* Modifiers for PRENUM
* Fixes some of obj2
"""

from dep_tree import DependencyTree, remove_semispace

changed_set = set()


def has_two_vconj_deps(tree: DependencyTree, v: int):
    num_vconjs = 0
    for ch in tree.children[v + 1]:
        if tree.labels[ch - 1] == "VCONJ":
            num_vconjs += 1
    return num_vconjs > 1


def fix_verb_conj_order(tree, v, label):
    v_head = tree.heads[v] - 1
    if v_head < v:
        return  # no need to change
    v_grand_head = tree.heads[v_head]
    tree.heads[v] = v_grand_head
    tree.labels[v] = tree.labels[v_head]
    tree.heads[v_head] = v + 1
    tree.labels[v_head] = label
    changed_set.add(tree.other_features[0].feat_dict['senID'])
    tree.rebuild_children()


def fix_cc_order(tree, cc, label):
    cc_head = tree.heads[cc] - 1

    if cc_head < cc:
        return  # No need to change

    if len(tree.children[cc + 1]) == 0:
        print("Warning: No CC children", tree.other_features[0].feat_dict['senID'])
        return

    children = sorted(list(tree.children[cc + 1]))
    cc_dep = None
    for c in children:
        child = c - 1
        if child < cc + 1 and tree.tags[child] in {"ADR", "V", "PSUS", "N", "PREM", "ADJ"}:
            cc_dep = child

    if cc_dep is None:
        print("Orphaned", tree.other_features[0].feat_dict['senID'])
        return

    cc_grand_head = tree.heads[cc_head]
    cc_grand_label = tree.labels[cc_grand_head - 1] if cc_grand_head > 0 else "root"
    tree.heads[cc_dep] = cc_grand_head
    tree.labels[cc_dep] = cc_grand_label
    tree.heads[cc_head] = cc + 1
    tree.labels[cc_head] = "POSDEP"
    tree.heads[cc] = cc_dep + 1
    tree.labels[cc] = label
    changed_set.add(tree.other_features[0].feat_dict['senID'])
    tree.rebuild_children()


def fix_vconj_order(tree):
    vconj_list = []
    for i in range(len(tree.labels) - 1, -1, -1):
        label = tree.labels[i]
        if label == "VCONJ":
            if tree.tags[i] == "CONJ":
                fix_cc_order(tree, i, tree.labels[i])
            else:
                fix_verb_conj_order(tree, i, tree.labels[i])
            vconj_list.append((i, tree.heads[i], tree.tags[i], tree.words[i]))


if __name__ == '__main__':
    input_files = ['Persian_Dependency_Treebank_(PerDT)_V1.1.1/Data/train.conll',
                   'Persian_Dependency_Treebank_(PerDT)_V1.1.1/Data//dev.conll',
                   'Persian_Dependency_Treebank_(PerDT)_V1.1.1/Data//test.conll']
    output_files = ['Persian_Dependency_Treebank_(PerDT)_V1.1.1/Data/train.conll',
                    'Persian_Dependency_Treebank_(PerDT)_V1.1.1/Data//dev.conll',
                    'Persian_Dependency_Treebank_(PerDT)_V1.1.1/Data//test.conll']

    comp_l = {26621, 30910, 31081, 31682, 47333, 38599, 38600, 38601, 38604, 39924, 41245, 41857, 46975, 51705,
              53316, 53769, 54158, 54346, 54349, 54350, 48985, 36024, 26621, 30910, 31081, 31682}
    for f_idx, inp_f in enumerate(input_files):
        parcl_trees = []
        vconj_trees = []
        tree_list = DependencyTree.load_trees_from_conll_file(inp_f)
        for i, tree in enumerate(tree_list):
            for w, (lemma, word, ftag) in enumerate(zip(tree.lemmas, tree.words, tree.ftags)):
                if tree.labels[w] == "OBJ2" and tree.sen_id in comp_l:
                    tree.labels[w] = "NVE"
                if tree.labels[w] == "ROOT":
                    tree.labels[w] = "root"
                if lemma == "گشت#گرد" and ftag == "PASS":
                    tree.ftags[w] = "ACT"
                if lemma == "شد#شو" and ftag == "PASS":
                    tree.ftags[w] = "ACT"
                if lemma in {"کرد#کن"} and ftag == "PASS":
                    if "شو" not in word and "شد" not in word:
                        tree.ftags[w] = "ACT"
                        print(word)
                    else:
                        tree.ftags[w] = "ACT"
                        tree.lemmas[w] = "شد#شو"
                if (tree.tags[w] == "PRENUM" and tree.tags[tree.heads[w] - 1] == "PREP") \
                        or (
                        tree.tags[w] == "PRENUM" and tree.tags[tree.heads[w] - 1] == "N" and tree.heads[w] - 1 < w and
                        tree.words[tree.heads[w] - 1] == "حدود"):
                    head_id = tree.heads[w] - 1
                    if (tree.tags[w] == "PRENUM" and tree.tags[head_id] == "N" and head_id < w):
                        tree.tags[head_id] = "PREP"
                        tree.ftags[head_id] = "PREP"
                    head_ftag = tree.ftags[head_id]
                    grand_head_id = tree.heads[head_id] - 1
                    grand_head_ftag = tree.ftags[grand_head_id]
                    if (grand_head_ftag == "AJCM" and tree.labels[head_id] == "COMPPP") or \
                            grand_head_ftag == "AJP" and tree.labels[head_id] == "AJPP":
                        assert len(tree.children[tree.heads[w]]) == 1
                        assert len(tree.children[tree.heads[head_id]]) == 1

                        span_head = tree.heads[grand_head_id]
                        span_label = "APREMOD"

                        tree.heads[grand_head_id] = w + 1  # assigning to the number
                        tree.labels[grand_head_id] = "PREDEP"
                        tree.heads[w] = span_head
                        tree.labels[w] = span_label
                    else:
                        span_head = grand_head_id + 1
                        span_label = "APREMOD"
                        tree.heads[head_id] = w + 1  # assigning to the number
                        tree.labels[head_id] = "PREDEP"
                        tree.heads[w] = span_head
                        tree.labels[w] = span_label

            for w, word in enumerate(tree.words):
                #     if word == "و" and tree.tags[w] == "SUBR":
                #         tree.tags[w] = "CONJ"
                #         tree.ftags[w] = "CONJ"
                # if "PARCL" in tree.labels:
                #     parcl_trees.append(tree)
                # if "VCONJ" in tree.labels:
                vconj_trees.append(tree)
                # DO NOT UNCOMMENT THIS LINE (BUG!)
                # fix_vconj_order(tree)

        for tree in parcl_trees:
            include_tree = False
            parcl_idx = [i for i, label in enumerate(tree.labels) if label == "PARCL"]
            for idx in parcl_idx:
                head_index = tree.heads[idx]
                head_id = head_index - 1

                for dep in range(0, idx):
                    if tree.heads[dep] > idx + 1:
                        if tree.labels[dep] not in {"PREDEP", "PARCL", "MOS", "NVE", "VPP", "PUNC", "OBJ", "NPP",
                                                    "VCONJ"}:
                            if tree.labels[dep] in {"SBJ", "AJUCL", "ADV"}:
                                # Change the head for SBJ/AJUCL/ADV
                                tree.heads[dep] = idx + 1

        # Fixing wrong roots due to wrong VCONJ rotation.
        # sen_changed = set()
        # for tree in tree_list:
        #     for idx, (label, head) in enumerate(zip(tree.labels, tree.heads)):
        #         if label == "root" and head != 0:
        #             tree.labels[idx] = "VCL"
        #             sen_changed.add(tree.sen_id)
        # print(len(sen_changed))

        # Fixing double VCONJS
        sen_changed = set()
        for tree in tree_list:
            for i, word in enumerate(tree.words):
                if has_two_vconj_deps(tree, i):
                    if tree.sen_id not in {31882, 31083}:
                        print("POSSIBLE PROBLEM in VCONJ", tree.sen_id)
        print(len(sen_changed))

        for tree in tree_list:
            if not tree.is_valid_tree():
                print("Malformed Dadegan tree in", inp_f, tree.other_features[0].feat_dict["senID"])
            for idx, (label, head) in enumerate(zip(tree.labels, tree.heads)):
                if label == "root" and head != 0:
                    print("Error in root", tree.sen_id)
                tree.words[idx] = tree.words[idx].replace("\u200a", "")
                tree.lemmas[idx] = tree.lemmas[idx].replace("\u200a", "")
                tree.words[idx] = remove_semispace(tree.words[idx])
        DependencyTree.write_to_conll(tree_list, output_files[f_idx])

print("\n".join(changed_set))
