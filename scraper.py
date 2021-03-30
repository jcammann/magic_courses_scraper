#!/usr/bin/env python3

import mechanize
import http.cookiejar
import os
from bs4 import BeautifulSoup
from getpass import getpass

email = "j.cammann@lboro.ac.uk"
pw = ""
semester = "2020-2021"
courses = ["magic099", "magic014", "magic102"]
reload_all = False


print("email: ", email)
if not pw:
    pw = getpass("Password: ")

cj = http.cookiejar.CookieJar()
br = mechanize.Browser()

br.set_cookiejar(cj)
br.open("https://maths-magic.ac.uk/login")

br.select_form(nr=0)

br.form['email'] = email
br.form['password'] = pw
br.submit()

for course in courses:
    course_url = "https://maths-magic.ac.uk/courses/"+semester+"/"+course
    r = br.open(course_url)
    content = br.response().read()
    soup = BeautifulSoup(content, features="lxml")
    t = soup.find('title') #<td>My home address</td>
    title = t.contents[0][1:] #My home address
    title = title.replace(" ","_")
    remove_from_title_end = "_|__MAGIC_Maths"
    remove_from_title_start = "MAGICXXX:_"
    title = title[:-len(remove_from_title_end)]
    title = title[len(remove_from_title_start):]
    print(course,title)

    folder = course+"_"+title
    if not os.path.exists(folder):
        os.makedirs(folder)
    urls = set()

    links = br.links()

    for link in links:
        key = "/downloads/course-file/"
        if link.url[:len(key)] == key:
            if link.absolute_url not in urls:
                urls.add(link.absolute_url)
                # print(link.absolute_url)
                response = br.open(link.absolute_url)
                info = response.info()
                cd = info.get('Content-Disposition')
                key = "attachment; filename="
                filename = cd[len(key):]
                filename = filename.strip('"')
                # print(filename)
                if reload_all or not os.path.isfile(folder+"/"+filename):
                    print("Downloading: ", folder+"/"+filename, " from: ",
                          link.absolute_url)
                    br.retrieve(link.absolute_url, folder+"/"+filename)
    print()
