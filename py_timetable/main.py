def show_csv_file(input_path):
    try:
        # CSVファイル読み込み
        with open(input_path, "r") as csv_file:
            print(csv_file.read())

    except Exception as e:
        print("ERROR", e)

def show_last_time(hour, input_path):
    try:
        # CSVファイル読み込み
        with open(input_path, "r") as csv_file:
            # ファイルの先頭から１行ずつ読み込む
            for line in csv_file:
                if line.startswith(hour):
                    times = line.replace("\n","").split(",")
                    print(hour + ":" + times[len(times)-1])
                    break

    except Exception as e:
        print("ERROR", e)

def show_next_time(hour, minute, input_path):
    try:
        # CSVファイル読み込み
        with open(input_path, "r") as csv_file:
            # ファイルの先頭から１行ずつ読み込む
            first_train = ""
            first_flg = True
            hour_find_flg = False
            minute_find_flg = False
            for line in csv_file:
                # 始発以前なら始発を出力
                if first_flg:
                    first_flg = False
                     # 始発を取得
                    first_train = line[:5].replace(",",":")
                    if (hour <= line[:2]):
                        print(first_train)
                        break
                # 始発以降の場合で、合致する時間帯があれば
                if line.startswith(hour):
                    times = line.replace("\n","").split(",")
                    for time in times:
                        # 時間帯部分をスキップ
                        if hour_find_flg == False:
                            hour_find_flg = True
                            continue
                        # 時刻を調べ出力
                        if time >= minute:
                           minute_find_flg = True
                           print(hour + ":" + time)
                           break
                # 時刻が合致しなければ、次の時間帯の最初を出力
                elif hour_find_flg and (minute_find_flg == False):
                    print(line[:5].replace(",",":"))
                    break
            # 終電後であれば、始発を出力
            if minute_find_flg == False:
                print(first_train)

    except Exception as e:
        print("ERROR", e)

if __name__== "__main__":
    input_path = "data/tosabori_1.csv"
    hour = "24"
    minute = "00"

    # show_csv_file(input_path)
    # show_last_time(hour, input_path)
    show_next_time(hour, minute, input_path)
