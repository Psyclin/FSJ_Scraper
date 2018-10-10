#---------------------------------------------------------------------------------------------------------------
# This project is for Christian Pearson, it scraps the FSJnow website for job postings and organizes the data (edit it as you please)
# - luv Darren
#----------------------------------------------------------------------------------------------------------------
import requests
import datetime
from bs4 import BeautifulSoup as bs


class Job:
    def __init__(self, job_info):
        self.job_info = job_info
        
    def get_info(self):
        return self.job_info

 
        
class Category:
    def __init__(self, name, URL):
        self.name = name
        self.URL = URL
        self.sub_categories = []
        self.job_list = []
   
    def get_URL(self):
        return self.URL
    
    def get_name(self):
        return self.name
    
    def get_info(self):
        return self.name, self.URL
    
    def add_new_category(self, category):
        self.sub_categories.append(category)
        
    def get_categories(self):
        site_html = bs(requests.get(self.URL).content, 'html.parser')
        try:            
            categories_html = site_html.find("div", class_="sub-category").find_parent("ul").find_all("a")
            for category in categories_html:
                if len(category) > 0:
                    name = category.find("b").get_text()
                    url = "http://" + site_name + category.get("href")
                    self.add_new_category(Category(name, url))             
        except AttributeError:
            print("No categories!!")
            self.get_jobs(site_html)
            
    def get_jobs(self, site_html):
        jobs_list = []
        jobs_html = site_html.find_all("div", class_="ads_descripstion")
        for job in jobs_html:
            bs(requests.get("http://fsjnow.com/classifieds/catId/53").content, 'html.parser')
            jobs_list.append("http://" + site_name + job.find("a").get("href"))
        for job in jobs_list:
            job_info = ""
            site_html = bs(requests.get(job).content, 'html.parser')
            job_html = site_html.find_all("td")
            job_info = [details.get_text().strip() for details in job_html]
            self.job_list.append(Job(job_info))
            print(job_info)
    
    def has_categories(self):
        if len(self.sub_categories) > 0:
            return True
        else:
            return False
        
    def has_jobs(self):
        if len(self.job_list) > 0:
            return True
        else:
            return False    
            
    def export_info(self):
        info = "Category: " + self.get_name() + "\n" + ("*"*20) + "\n"
        if self.has_categories():
            for category in self.sub_categories:
                info += "sub-category: " + category.get_name() + "\n" + ("*"*20) + "\n"
                for job in category:
                    for job_info in job.get_info:
                        info += job_info
                    info += "\n\n"
        else:
            for job in self.job_list:
                for job_info in job.get_info():
                    info += job_info
                info += "\n\n"                
                
        return info
                
                
                                                
class Job_Tree:
    
    def __init__(self):
        self.category_list = []
    
    def add_new_category(self, category):
        self.category_list.append(category)
   
    def display_categories(self):
        for category in self.category_list:
            print(category.get_info())
            
    def get_category_list(self):
        return self.category_list
    
    def get_categories(self, URL):
        site_html = bs(requests.get(URL).content, 'html.parser')
        categories_html = site_html.find("div", class_="sub-category").find_parent("ul").find_all("a")
    
        for category in categories_html:
            if len(category) > 0:
                name = category.find("b").get_text()
                url = "http://" + site_name + category.get("href")
                self.add_new_category(Category(name, url))
    
    def export_info(self):
        filename = "jobs - " + str(datetime.datetime.now().date()) + ".txt"
        with open(filename, "w") as file:
            for category in self.category_list:
                file.write(category.export_info())
                
                        
    

job_tree = Job_Tree()
site_name = "fsjnow.com"
main_URL = "http://fsjnow.com/classifieds/catId/39"


job_tree.get_categories(main_URL)
job_tree.display_categories()

for category in job_tree.category_list:
    category.get_categories()
    
    
#job_tree.category_list[0].get_categories()

for category in job_tree.category_list:
    if category.has_categories():
        for sub_category in category.sub_categories:
            sub_category.get_categories()

job_tree.export_info()

