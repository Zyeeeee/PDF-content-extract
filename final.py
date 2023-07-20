import re
import pdfplumber


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


def offset_calculate(pdf):  # 偏移量计算
    mid_page_num = int(len(pdf.pages) / 2)  # 计算中间页码数字
    mid_page = pdf.pages[mid_page_num]  # 获取中间页
    book_num = int(mid_page.extract_text_lines()[-1]['text'])  # 获取中间页对应书本的页码
    offset = mid_page_num - book_num + 1  # 计算偏移量
    return offset


def content_output(pdf):  # 输出结果
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


if __name__ == '__main__':
    extract_pdf = load_pdf()
    content_output(extract_pdf)
