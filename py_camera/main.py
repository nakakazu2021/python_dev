import pyautogui
import cv2
import numpy as np
import time

def capture_screen(screen_size, output_file, fps=60, codec="XVID"):
    fourcc = cv2.VideoWriter_fourcc(*codec)
    output = cv2.VideoWriter(output_file, fourcc, fps, screen_size)

    start_time = time.time()
    try:
        while True:
            # 画面をキャプチャしてOpenCVの画像に変換
            screenshot = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # 動画にフレームを追加
            output.write(frame)

            # キャプチャ終了の条件（例: 'q'キーを押したとき）
            if cv2.waitKey(1) == ord("q"):
                break

            # 実際の経過時間を計算
            elapsed_time = time.time() - start_time

            # 10秒ごとに"/"マークを表示
            if elapsed_time >= 10:
                print("/", end="", flush=True)
                start_time = time.time()

    except KeyboardInterrupt:
        pass

    # 動画ファイルを保存する
    output.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 画面キャプチャの準備
    screen_size = (1920, 1080)  # キャプチャする画面のサイズ
    output_file = "captured_video.avi"
    capture_screen(screen_size, output_file)
