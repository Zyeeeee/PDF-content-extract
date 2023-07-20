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
为了识别出一本书的目录页，由于书本的目录在绝大多数情况下都是在书本的最前面，因此在程序中只分析了PDF文件的前20页，以“chapter”为关键词进行查找并筛选，最后返回目录页的页码。
具体函数实现如下
'''
def content_page_search(pdf):  # 目录页查找
    result_nums = set()  # 创建一个空集合去储存目录页的页数
    for num in range(20):
        page = pdf.pages[num]
        search_result = page.search('chapter ', case=False)
        # case=False是让程序不区分大小写，只要出现chapter的都算，注意后面有个空格，不然会把有后缀的chapter也算进去
        if search_result:
            result_nums.add(search_result[0]['chars'][0]['page_number'])  # 这样可以提取到目录页码
        else:
            continue
    return result_nums
'''
