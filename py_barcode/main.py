import cv2
import requests
from bs4 import BeautifulSoup
from pyzbar.pyzbar import decode
import isbnlib

# 検出されたバーコードの情報を保持するセットを初期化する
detected_barcodes = set()  

def read_barcodes(frame, output_file):

    # フレームからバーコードをデコードする
    barcodes = decode(frame)   
    
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        if barcode_info not in detected_barcodes:
            detected_barcodes.add(barcode_info)
            if isbnlib.is_isbn10(barcode_info) or isbnlib.is_isbn13(barcode_info):
                # ISBN情報を表示する
                print("ISBN:", barcode_info) 
                # バーコード情報を解析して書籍情報を表示する
                display_book_info(barcode_info, output_file)  
        
        # バーコードの位置に矩形を描画する
        x, y, w, h = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  
        
        # バーコード情報を描画する
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 0.5, (255, 255, 255), 1)  

    return frame

def display_book_info(isbn, output_file):
    try:
        response = requests.get(f"https://www.kinokuniya.co.jp/disp/CSfDispListPage_001.jsp?qsd=true&ptk=01&gtin={isbn}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # 商品名を取得する
            h3_tag = soup.find('h3')
            product_name = h3_tag.text.strip() if h3_tag else "商品名が取得できませんでした。"

            # 著者を取得する
            div_details = soup.find('div', class_='details')
            p_1 = div_details.find('p') if div_details else None
            author = p_1.text.strip() if p_1 else "著者が取得できませんでした。"

            # 出版社を取得する
            div_details2 = soup.find('div', class_='details2')
            li = div_details2.find('li') if div_details2 else None
            publisher = li.text.strip() if li else "出版社が取得できませんでした。"

            # ジャンルを取得する
            div_other_box = soup.find('div', class_='other_box')
            div_other_box_inner = div_other_box.find_all('div', class_='other_box_inner') if div_other_box else None
            a_tag = div_other_box_inner[1].find('a') if div_other_box_inner and len(div_other_box_inner) > 1 else None
            genre = a_tag.text.strip() if a_tag else "ジャンルが取得できませんでした。"

            # 各情報をファイルに書き込む
            output_file.write("商品名:" + product_name + "\n")
            output_file.write("著者:" + author + "\n")
            output_file.write("出版社:" + publisher + "\n")
            output_file.write("ジャンル:" + genre + "\n\n")
        else:
             # HTTPエラーをログに記録する
            output_file.write(f"HTTPエラー：{response.status_code}\n") 

    except requests.exceptions.RequestException as e:
        # HTTPリクエストエラーをログに記録する
        output_file.write("HTTPリクエストエラー:" + str(e) + "\n")  

if __name__ == "__main__":
    # ファイルを追記モードでオープンする
    output_file = open("barcode_list.txt", "a")  
    # カメラを起動する
    cap = cv2.VideoCapture(0)  

    while True:
        # フレームをキャプチャする
        ret, frame = cap.read()  
        if not ret:
            # フレームのキャプチャに失敗した場合はエラーメッセージを表示してループを抜ける
            print("Failed to capture frame")  
            break

        # バーコードを読み取り、フレームに描画する
        frame = read_barcodes(frame, output_file)  

        # フレームを表示する
        cv2.imshow('Barcode reader', frame)  

        # キーボード入力を待ち、'q'が押されたらループを抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

    # カメラを解放する
    cap.release()  
    # ウィンドウを閉じる
    cv2.destroyAllWindows()  
    # ファイルをクローズする
    output_file.close()  
