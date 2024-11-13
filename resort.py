src_path = 'beforesort.txt' # 从椒盐音乐导出的歌单
list_path = 'musiclisttime.txt' # 从网易云音乐导出的歌单
local_path = '/storage/emulated/0/KHMD/music/'
output_path = 'resorted.txt' # 输出文件
all_match = False 

banned_chars = ['/', "'", '\xa0', ':', "*", "\"","<",">",'?','\\','|']

with open(src_path, 'r', encoding='utf-8') as f:
    src = f.readlines()

src_splited = [line.strip().replace(local_path,'').replace('.mp3','').split(' - ') for line in src]
for i in range(len(src_splited)):
    src_splited[i][1] = src_splited[i][1].replace('\xa0',' ')
    if len(src_splited[i]) > 2:
        src_splited[i] = [src_splited[i][0], ' - '.join(src_splited[i][1:])]

with open(list_path, 'r', encoding='utf-8') as f:
    list_path = f.readlines()

list_split = [line.strip().split(' - ') for line in list_path]
list_splited = []
for i in range(len(list_split)):
    if len(list_split[i]) < 2:
        continue
    if len(list_split[i]) > 2:
        list_split[i] = [' - '.join(list_split[i][:-1]), list_split[i][-1]]
    try:
        list_split[i][1] = list_split[i][1].replace(' / ','、')
        for char in banned_chars:
            list_split[i][1] = list_split[i][1].replace(char,'')    
            list_split[i][0] = list_split[i][0].replace(char,'')
        if [list_split[i][1], list_split[i][0]] in list_splited:
            cnt = 1
            while [list_split[i][1], list_split[i][0]+'('+str(cnt)+')'] in list_splited:
                cnt += 1
            list_splited.append([list_split[i][1], list_split[i][0]+'('+str(cnt)+')'])
        else:
            list_splited.append([list_split[i][1], list_split[i][0]])
    except:
        pass

resorted = []
cnt = 0
for line in list_splited:
    find = False
    for i in range(len(src_splited)):
        if line[0] == src_splited[i][0] and line[1] == src_splited[i][1]:
            resorted.append(src[i])
            find = True
            break
    if not find:
        print(line[0]+ ' - ' + line[1])
        cnt += 1
print("歌单中未在本地找到的歌曲数：", cnt)
if all_match:
    cnt = 0
    for i in range(len(src_splited)):
        if src[i] not in resorted:
            cnt += 1
            print(src_splited[i])
            print("相似歌曲：")
            for line in list_splited:
                if line[0] == src_splited[i][0]:
                    print(line)
                elif line[1] == src_splited[i][1]:
                    print(line)
            print()

    print("本地未在歌单中找到的歌曲数：", cnt)

with open(output_path, 'w', encoding='utf-8') as f:
    for line in resorted:
        f.write(line+'\n' if line[-1] != '\n' else line)