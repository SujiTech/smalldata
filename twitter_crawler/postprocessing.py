import csv

kol_set = set()
with open('data/all-kol.csv', 'r') as in_file , open('data/kol.csv','w') as out_file:
    out_file.write('\ufeff')
    kol_writer = csv.writer(out_file)
    kol_writer.writerow(['昵称', '用户名', '简介', '粉丝', '关注', '推文数', '喜欢数'])
    kol_reader = csv.reader(in_file)
    for row in kol_reader:
        if row[2] not in kol_set:
            kol_writer.writerow(row)
            kol_set.add(row[2])