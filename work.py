from PyPDF2 import PdfReader, PdfWriter
import os
import img2pdf
from io import BytesIO
import re

def imgs2pdf_pages(img_list, size=None):
    if size == None:
        size = (img2pdf.mm_to_pt(148), img2pdf.mm_to_pt(210))
    layout_fun = img2pdf.get_layout_fun(size)
    pdf_file = BytesIO()
    pdf_file.write(img2pdf.convert(img_list, layout_fun=layout_fun))
    reader = PdfReader(pdf_file)
    return reader.pages
    
def split_title(s:str):
    i = s.find("#")
    if i == -1:
        return None, s
    return s[:i], s[i+1:]

def solve(root:str, p:int, writer:PdfWriter, parent=None):
    file_lists = os.listdir(root)
    try:
        file_lists.sort(key=lambda x: int(re.findall(r"^\s*(\d+)", x)[0]))
    except:
        print('文件夹"{}"中的文件名未以数字开头，按照windows默认排序'.format(root))
    for file_title in file_lists:
        file_path = os.path.join(root, file_title)
        _, file_name = split_title(file_title)
        
        if not os.path.isdir(file_path):
            writer.add_page(imgs2pdf_pages([file_path])[0])
            p+=1
        else:
            subParent = writer.add_outline_item(file_name, p, parent=parent)
            p = solve(file_path, p, writer, parent=subParent)
    return p

if __name__ == '__main__':

    work_dir = "./工作区"
    output_dir = "./输出"
    print('请在"工作区"文件夹里面放入需要处理的文件，pdf输出放在"输出"文件夹里面')
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    for pdf_title in os.listdir(work_dir):
        _, pdf_name = split_title(pdf_title)
        pdf_writer = PdfWriter()
        pdf_dir = os.path.join(work_dir, pdf_title)
        solve(pdf_dir, 0, pdf_writer)
        with open(os.path.join(output_dir, "{}.pdf").format(pdf_name), "wb") as f:
            pdf_writer.write(f)