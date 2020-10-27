from bs4 import BeautifulSoup
from tabulate import tabulate
import numpy as np
import os


def writeHtml(mat, mat2, img, imgafter=""):
    path = os.path.abspath(os.getcwd())
    html = open(path+"/ressources/rapport/index.html").read()

    soup = BeautifulSoup(html, 'lxml')
    vec = soup.find('div', {"id": "vec"})
    image2Div = soup.find('div', {"id": "image2"})
    imageDiv = soup.find('div', {"id": "image"})
    tableauxDiv = soup.find('div', {"id": "tableaux"})
    tableaux2Div = soup.find('div', {"id": "tableaux2"})
    #vec = soup.find('div', {"id": "vec"})

    image = soup.new_tag('img', src=img, alt="this is an image of my desktop")
    image2 = soup.new_tag('img', src=img, alt="this is an image of my desktop")
    image3 = soup.new_tag('img', src=img, alt="this is an image of my desktop")
    image4 = soup.new_tag('img', src=img, alt="this is an image of my desktop")

    # 1 ere Etape :
    imageDiv.append(image)
    imageDiv.append(BeautifulSoup(
        '<span style="font-size:20px">====|></span>', "lxml"))
    imageDiv.append(image2)

    # 1 ere Etape :
    image2Div.append(image3)
    image2Div.append(BeautifulSoup(
        '<span style="font-size:20px">====|></span>', "lxml"))
    image2Div.append(image4)

    # 2 eme Etape :
    tableauxDiv.append(BeautifulSoup(tabulate(mat, tablefmt='html'), "lxml"))
    tableauxDiv.append(BeautifulSoup(
        '<span ><br><br><br>====|></span>', "lxml"))
    tableauxDiv.append(BeautifulSoup(tabulate(mat2, tablefmt='html'), "lxml"))

    # 3 eme Etape :
    tableaux2Div.append(BeautifulSoup(tabulate(mat, tablefmt='html'), "lxml"))
    tableaux2Div.append(BeautifulSoup(
        '<span ><br><br><br>====|></span>', "lxml"))
    tableaux2Div.append(BeautifulSoup(tabulate(mat2, tablefmt='html'), "lxml"))

    # test
    test2 = '0.0'*64
    vec.append(BeautifulSoup(
        '<div style ="text-align:center">'+'0.0'*64+' <div> ', "lxml"))
    # vec.append(BeautifulSoup(
    #    tabulate(np.zeros((1, 64)), tablefmt='html'), "lxml"))
    with open(path+"/ressources/rapport/example_modified.html", "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))

    return (path+"/ressources/rapport/example_modified.html")
