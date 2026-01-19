#!/bin/bash

# 1. 确保在 static 目录下下载 CHTML 引擎
wget -O tex-mml-chtml.js https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

# 2. 创建存放字体的目录结构
mkdir -p output/chtml/fonts/woff-v2
cd output/chtml/fonts/woff-v2

# 3. 定义基础 URL
base_url="https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2"

# 4. 定义字体列表
fonts=(
  "MathJax_Main-Regular.woff"
  "MathJax_Main-Bold.woff"
  "MathJax_Main-Italic.woff"
  "MathJax_Math-Italic.woff"
  "MathJax_Size1-Regular.woff"
  "MathJax_Size2-Regular.woff"
  "MathJax_Size3-Regular.woff"
  "MathJax_Size4-Regular.woff"
  "MathJax_AMS-Regular.woff"
  "MathJax_Caligraphic-Regular.woff"
  "MathJax_Caligraphic-Bold.woff"
  "MathJax_Fraktur-Regular.woff"
  "MathJax_Fraktur-Bold.woff"
  "MathJax_SansSerif-Regular.woff"
  "MathJax_SansSerif-Bold.woff"
  "MathJax_SansSerif-Italic.woff"
  "MathJax_Script-Regular.woff"
  "MathJax_Typewriter-Regular.woff"
  "MathJax_Vector-Regular.woff"
  "MathJax_Vector-Bold.woff"
  "MathJax_Zero.woff"
)

# 5. 循环下载
echo "开始下载字体文件..."
for font in "${fonts[@]}"; do
  echo "正在下载: $font"
  wget -O "$font" "$base_url/$font"
done

echo "✅ 所有字体下载完成！"