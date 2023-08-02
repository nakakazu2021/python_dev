import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 日本語フォントの設定
# フォントファイル（.ttfファイル）のパスを指定してください
font_path = 'C:/Windows/Fonts/meiryo.ttc'
japanese_font = fm.FontProperties(fname=font_path)

# CSVファイルの読み込み
df = pd.read_csv('data.csv', parse_dates=['日付'], index_col='日付')

# 発生数と対応数の累計を計算
df['発生数累計'] = df['発生数'].cumsum()
df['対応数累計'] = df['対応数'].cumsum()

# グラフを作成
fig, ax1 = plt.subplots(figsize=(10, 6))

# 折れ線グラフを描画
ax1.plot(df.index, df['発生数累計'], color='blue', label='発生数累計', marker='o', linestyle='--')
ax1.plot(df.index, df['対応数累計'], color='red', label='対応数累計', marker='x', linestyle='--')
ax1.set_xlabel('日付', fontproperties=japanese_font)
ax1.set_ylabel('累計', fontproperties=japanese_font)
ax1.set_title('発生数と対応数の累計', fontproperties=japanese_font, fontsize=14)
ax1.legend(loc='upper left', prop=japanese_font)

# 棒グラフを描画
ax2 = ax1.twinx()
width = 0.4
ax2.bar(df.index, df['発生数'], width=width, alpha=0.5, label='発生数', color='lightblue')
ax2.bar(df.index + pd.Timedelta(days=width), df['対応数'], width=width, alpha=0.5, label='対応数', color='lightcoral')
ax2.set_ylabel('発生数と対応数', fontproperties=japanese_font)
ax2.legend(loc='upper right', prop=japanese_font)

# y軸の目盛りを動的に変更（発生累計数の最大値に設定）
yticks_max = max(df['発生数累計'].max(), df['対応数累計'].max())
yticks_interval = 1  # 目盛りの間隔を指定（例: 1ごとに目盛りを表示）
ax2.set_yticks(range(0, yticks_max + 1, yticks_interval))

# グラフの表示
plt.tight_layout()
plt.show()
