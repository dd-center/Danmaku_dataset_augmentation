# Danmaku_dataset_augmentation
爬取b站vtuber视频的弹幕
- vtuber.txt： 存有vtuber名称以及其对应的mid
- av_data_list： 存有每个vtuber发过的视频av号
- danmuku.py From：https://github.com/qq519043202/BILI.git
- danmaku_dataset： 🎉视频弹幕🎉

用法：

运行
```
python3 dataset_augment.py
```    

⚠️注意⚠️
- 在爬弹幕的过程中，程序可能因为【不明原因】卡顿。按control+c跳过正在爬的视频即可
- 由于danmuku.py并不十分的robust【甩锅】，有很少一部分av号出现了以下错误，所以弹幕没有爬下来。
  update: 原因找到了，这玩意不能爬分p的视频的弹幕。不过鉴于大多数vtuber都不传分p的视频，这点事情就忽视掉吧...
  ```
  Traceback (most recent call last):
    File "danmuku.py", line 81, in <module>
      main()
    File "danmuku.py", line 77, in main
      cid = get_cid(aid, mode)
    File "danmuku.py", line 55, in get_cid
      cid = match_list[0][match_list[0].index('cid')+5:-1]
  IndexError: list index out of range
  ```
