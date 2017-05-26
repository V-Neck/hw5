from collections import Counter
from sys import argv

DELIMIT = " => "

for document in argv[1:]:
    rules = open(document, "r").readlines()
    doc_counts = open("counts/" + document, "w+")
    print document

    rewrite_rules = {}
    rules_of_interest = ["subjh", "extracomp", "nadj_rc", "extradj_i_vp", "frag_np", "imper"]
    rewrite_rules_of_interest = {}

    symbol_count = Counter()

    for rule in rules:
        try:
            symbol, rewrite = rule.split(DELIMIT)
        except:
            rewrite = rule
        if symbol:
            symbol_count[symbol] += 1
            if not symbol in rewrite_rules:
                rewrite_rules[symbol] = []
            rewrite_rules[symbol].append(rewrite)

    for rule in rules_of_interest:
        rewrite_rules_of_interest[rule] = rewrite_rules[rule]

    cnts = {}
    for rule in rewrite_rules_of_interest:
        cnt = Counter()
        for rewrite in rewrite_rules_of_interest[rule]:
            cnt[rewrite] += 1
        cnts[rule] = cnt

    for rule in cnts:
        total = float(sum(cnts[rule].values()))
        for rewrite in cnts[rule]:
            cnts[rule][rewrite] /= total

    for rule in cnts:
        h_line = "%s %f" % (rule, symbol_count[rule] / float(sum(symbol_count.values())))
        print h_line
        doc_counts.write(h_line + "\n")
        for rewrite in cnts[rule].keys():
            values = (rewrite.rstrip(), 100 * cnts[rule][rewrite])
            d_line = "\t%s : %f%%" % (values)
            print d_line
            doc_counts.write(d_line + "\n")
    doc_counts.close()
