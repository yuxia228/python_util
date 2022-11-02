import win32com.client
import datetime
import time
import os # for calling cls command

# Resize console
required_consle_size = 7 + 10 + 1
os.system("mode 60,"+str(required_consle_size))

def show_schedule():
    # 調べたい日付範囲を定義
    dt_now = datetime.datetime.now()
    #print(dt_now)
    #print(dt_now.strftime('%Y-%m-%d %H:%M:%S'))
    start_date = datetime.datetime(dt_now.year, dt_now.month, dt_now.day,  6, 00,00)
    end_date   = datetime.datetime(dt_now.year, dt_now.month, dt_now.day, 22, 00, 00)

    # Outlookの予定表へのインタフェースオブジェクトを取得
    Outlook = win32com.client.Dispatch("Outlook.Application").GetNameSpace("MAPI")
    CalendarItems = Outlook.GetDefaultFolder(9).Items

    # 定期的な予定の二番目以降の予定を検索に含める
    CalendarItems.IncludeRecurrences = True

    # 開始時間でソート
    CalendarItems.Sort("[Start]")

    # "mm/dd/yyyy HH:MM AM"の形式に変換し、フィルター文字列を作成
    strStart = start_date.strftime('%m/%d/%Y %H:%M %p')
    strEnd = end_date.strftime('%m/%d/%Y %H:%M %p')
    sFilter = f"[Start] >= '{strStart}' And [End] <= '{strEnd}'"

    FLAG =  False
    next_schd = None
    # フィルターを適用し表示
    os.system('cls')
    print("----------------------------")
    print("Today's schedule")
    FilteredItems = CalendarItems.Restrict(sFilter)
    for item in FilteredItems:
        if FLAG is False and dt_now.hour < int(item.start.Format("%H")):
            print(dt_now.strftime('%Y/%m/%d %H:%M'), " ~ ", "xx:xx", " : ", "**NOW**")
            FLAG = True
            next_schd = item
        print(item.start.Format("%Y/%m/%d %H:%M"), " ~ ", item.end.Format("%H:%M"), " : ", item.subject)
        #print(str(item.Start.Format("%Y/%m/%d %H:%M")) + " : " + str(item.Subject))
    print("----------------------------")
    print("Next schedule is:")
    if next_schd is None:
        print("Nothing")
    else:
        print(next_schd.start.Format("%Y/%m/%d %H:%M"), \
              " ~ ", next_schd.end.Format("%H:%M"), \
              " : ", next_schd.subject)
    print("----------------------------")


while True:
    show_schedule()
    time.sleep(60)
