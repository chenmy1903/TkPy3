# TkPy3一个升级版的TkPy IDE
# 安装TkPy3:
```
pip install tkpy3
```
# 未修复的Bug
```
激活码到期时没有弹窗（直接闪退，无法启动等情况）
有部分内容没有添加
3.6.855 版本正在制作中 敬请期待！（现在是预览版）
```

## 安装依赖

>注意: 需要安装谷歌浏览器。
```
pip install PyQt5
python -m TkPy3.tkpy3_tools.relys
```
如果上面那个无法运行，请运行这个:
```
python -m pip install --upgrade pygments PyQt5 pip pickleshare autopep8 qscintilla diff_match_patch jedi==0.15.2 uvicorn FastAPI jinja2 markdown qtconsole --timeout 1000
```
## 运行TkPy3
> 如果已安装TkPy3
```
python -m TkPy3
```

> 没有安装
```
python run_code.py
```
> ## 注意: 不要用IDLE运行

# 版本记录
#### 3.6.855
<pre>
加入Matplotlib绘图的支持
加入TkPy Web浏览器
加入部分英文支持
</pre>
#### 3.6.854
<pre>
加入托盘
修复Markdown转换器的Bug
更新图标 (源于Eric6)
支持多国语言 (现在只有中文)
加入PyShell
</pre>
##### 3.6.855预告
<pre>
加入英文支持
加入TkPy Path
加入I18n编辑器
</pre>
#### 3.6.853
<pre>
加入版权 (MIT)
加入Qt5 Ui文件预览器
Window mdi Tab可移动
修复没有高亮的Bug
加入排列Import语句
加入右键菜单
增加行号预览(右下角)
</pre>
#### 3.6.852
<pre>
修复一些小Bug
增加重新打开文件
加入文件拖动功能
修复使用pythonw运行的时候的Bug
增加IPython快捷方式
更新依赖文件
增加Python包帮助
</pre>
#### 3.6.851
<pre>
加入系统任务栏图标 (Windows系统有效)
更新了TkPy3的图标
加入文件分页功能 (像<a href="https://www.latex-project.org/">LaTex</a> (收费)一样的分页功能)
README.md加入美化
</pre>
#### 3.6.85
<pre>
修复一些小Bug
增加版权 (<a href="https://github.com/chenmy1903">chenmy1903</a> ©)
开放Web版帮助
增加Qt加载功能 （还是未开放）
自动补全有Bug (现在不开放了)
增加拓展功能 (未开放)
加入百度翻译 (未开放)
加入转到源码 (未开放)
安装依赖加入黑色主题
Markdown转换器加入pygments代码高亮
</pre>
##### 3.6.86版本预告 (做好会晚一点) (所有功能分为小版本发布)
<pre>
加入Pyshell
加入重新打开文件
加入TkPy Path管理器
加入运行功能
加入Windows Path管理器 (比较危险，不要轻易尝试，除非用虚拟机)
</pre>
#### 3.6.84
<pre>
markdown功能添加代码高亮
</pre>
#### 3.6.83
<pre>
加入重置TkPy3的设置功能
</pre>
#### 3.6.82
<pre>
对序列号功能进行改进
可以重新激活TkPy3
</pre>
#### 3.6.81
<pre>
增加了序列号功能
加入Windows 10加载动画 (未开放)
对编辑器的体验增加了完善
</pre>
#### 3.6.8
<pre>
修复pip在安装时的Bug
更新了在PyPi上上传的Bug
</pre>
#### 3.6.7
<pre>
修复一些小Bug
依赖安装窗口更人性化
加入MarkDown转换器
加入代码折叠功能
加入新功能报告
加入文件比较
加入Bug报告
加入Pyshell(未完成)
加入Web版帮助 (未完成)
加入一个飞船大战游戏 (未开放)
</pre>
#### 3.6.4
<pre>
加入安装依赖
</pre>
#### 3.4.0
<pre>
加入设置
</pre>
#### 3.0.0
<pre>
无新增 (最开始的版本)
</pre>
