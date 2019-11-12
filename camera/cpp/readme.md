そのうちディレクトリごとにまとめます...


Files:
* xiApiPlusOcv.hpp - This is the header file of our OpenCV wrapper.
* xiApiPlusOcv.cpp - Contains the implementation of our OpenCV wrapper. - 関数の定義いろいろある
* cv_cap.cpp - Sample code - 調整中
* Makefile - Flagに `-lm pkg-config --libs opencv`を追加 -> opencv.hppをinclude出来るようになった

The files contain 
code merged from xiAPIplus API + created C++ wrapper for OpenCV

# 基本的にJetson上での使用を考えて作りました。

How to Use
---
On Host PC
1. ssh接続を行う。(cygwin使ってます)
`$ ssh xavier@133.68.35.175`

2. 所定のディレクトリへ
`$ cd sanada/work/ML_biped/camera/cpp`

3. ファイル編集
`$ vim FILENAME`

4. コンパイル
`$ make`

5. 実行
`$ ./cv_cap`
