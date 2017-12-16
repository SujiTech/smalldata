mongoexport --db kol --collection info --type=csv --fieldFile fields.txt --out data/kol.csv
sed -i "1 s/^.*$/昵称, 用户名, 简介, 粉丝, 关注, 推文数, 喜欢数/" data/kol.csv
sed -i '1s/^\(\xef\xbb\xbf\)\?/\xef\xbb\xbf/' data/kol.csv
