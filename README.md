# PDF-content-extract
This is a solution for a written examination question
## 目录
* 一：设计思路
* 二：需求分析
* 三：具体实现和挑战
* 四：后续展望

### 一：设计思路
在拿到这个问题之后，根据我所应聘的岗位图像算法实习生来说，我首先想到的是利用图像识别的技术去完成这个任务。
但是由于时间有限，自主搭建并训练一个神经网络也许时间不足。因此，我花了不少时间在收集并学习了很多有关PDF处理的资料，并学习了如Py2PDF，pymupdf，pdfplumber的PDF处理库。
最终，因为时效的要求，我选择了运行时间更快的基于C语言实现的pdfplumber库而不是全python实现的Py2PDF，基于pdfplumber库的页面信息提取等功能去解决这个问题。

### 二：需求分析
* 首先，由于pdfplumber可以提取出PDF页面的信息，因此我想到要先识别出一本书当中的目录页，所以第一个需求就是目录页的识别。
* 在识别出目录页之后，就是要想办法找出目录页当中的书本页码所对应的PDF页码，所以第二个需求为页码分析
* 然后，是要将分析后的页码和结果输出，就是输出模块
* 为了实现让用户自定义输入文件，还要加入输入模块，可以让用户自定义PDF路径。

### 三：具体实现和挑战
#### 3.1 目录页识别
为了识别出一本书的目录页，由于书本的目录在绝大多数情况下都是在书本的最前面，因此在程序中只分析了PDF文件的前20页，以“chapter”为关键词进行查找并筛选，最后返回目录页的页码。在仔细分析了pdfplumber的多重嵌套输出方式后，终于找到了输出页码的正确方法
具体函数实现如下
```python
def content_page_search(pdf):  # 目录页查找
    result_nums = set()  # 创建一个空集合去储存目录页的页数防止重复
    for num in range(20):
        page = pdf.pages[num]
        search_result = page.search('chapter ', case=False)
        # case=False是让程序不区分大小写，只要出现chapter的都算，注意后面有个空格，不然会把有后缀的chapter也算进去
        if search_result:
            result_nums.add(search_result[0]['chars'][0]['page_number'])  # 这样可以提取到目录页码
        else:
            continue
    return result_nums
```
此函数可以很好地识别出目录页的PDF页码并返回。
#### 3.2 页码识别
##### 3.2.1 偏移量计算
在找出目录页之后，就迎来了新的问题，怎么把目录所展示的书本中的页码与PDF文件的页码相匹配。
对于这个问题，我利用了偏移量的想法，因为我发现PDF的一页其实是跟书本的一页所相对应的，只不过由于前言等部分的存在，导致PDF页码和书本页码出现了偏移，要计算出这个偏移量，我选择了全PDF文件中最中间的那一页，并以这一页的书本页码和PDF页码来计算出偏移量，偏移量会在后续用于计算目录书本页码和PDF页码的对应。
对于中间那一页的书本页码，由于页数一般都是在一页的最低端，因此我直接提取了最低端的页码作为书本页码。
偏移量计算函数如下所示
```python
def offset_calculate(pdf):  # 偏移量计算
    mid_page_num = int(len(pdf.pages) / 2)  # 计算中间页码数字
    mid_page = pdf.pages[mid_page_num]  # 获取中间页
    book_num = int(mid_page.extract_text_lines()[-1]['text'])  # 获取中间页对应书本的页码
    offset = mid_page_num - book_num + 1  # 计算偏移量
    return offset
```
##### 3.2.2 对应页码识别
在有了 3.2.1 中计算出来的偏移量之后，就可以回到目录页去计算目录页的书本页码对应的PDF页码，只需将书本页码加上偏移量就是所对应的PDF的页码了，为了保证提取到正确的书本页码，我利用了正则表达式去匹配，用于匹配以字母开头并以数字结尾的行，并提取出这个数字去做偏移量计算，以此得到所对应的PDF页码，并直接输出。
具体代码如下
```python
ef content_output(pdf):  # 输出结果
    content_page = content_page_search(pdf)  # 目录页数
    offset = offset_calculate(pdf)  # 偏移量
    print('正在输出目录')
    for num in content_page:
        page = pdf.pages[num - 1]
        text = page.extract_text_lines()
        # 下面用正则表达式去提取目录页当中以字母开头数字结尾的行，并将此行最后连续的数字提取出来，加上偏移量就是这一个书本页码在pdf中对应的页码
        for lines in text:
            line = lines['text']
            last_digits = re.findall(r'^[a-zA-Z].*\d+$', line)
            if last_digits:
                last_digits = int(re.findall(r'\d+', last_digits[0])[0])
                print(line, '|pdf page -->', last_digits + offset)
            else:
                print(line)
```
#### 3.3 输入模块
此模块用于给用户在控制台自定义输入PDF文件路径
```python
def load_pdf():  # pdf文件读取函数
    print('请输入pdf文件路径')
    load = input()
    try:
        pdf = pdfplumber.open(load)
        print("已读取文件")
        return pdf
    except Exception as e:
        print("文件路径有误请重试", e)
        load_pdf()
```

### 四：后续展望
这个项目做的还不是十分完善，虽然直接提取了目录页做分析免去了很多麻烦，但是后续还有很多需要完善的地方，比如页码识别的准确性，偏移量的合理性，中英文的结合模块。
当然了，这个问题还可以交由机器学习去完成，可以利用一些比如CNN，RNN去解决这个问题，训练一个神经网络去识别目录。我也会持续完善这个项目。
