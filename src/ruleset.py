from resume_converter import resume_to_str
import json
import PyPDF2

"""
Top level function that will be called from API endpoint.
Performs all checks on resume and returns a single dictionary
that will be sent as JSON to frontend
"""
def is_resume_pdf(filename):
    try:
        PyPDF2.PdfFileReader(open("saved-resumes/"+ filename, "rb"))
    except PyPDF2.utils.PdfReadError:
        return False
    else:
        return True

def is_resume_scannable(filename):
    string = resume_to_str(filename, path="saved-resumes/")
    if string == "":
        return False
    else:
        return True
    
def scan_resume(filename, resume_as_dict):
    checklist_list = checklist(filename, resume_as_dict)
    is_pdf = is_resume_pdf(filename)
    is_scannable = is_resume_scannable(filename)
    points = calculate_points(checklist_list, is_pdf, is_scannable)
    return {
        "checklist": checklist_list,
        "isFilePDF": is_pdf,
        "isFileScannable": is_scannable,
        "points": points
    }

def calculate_points(checklist_list, is_pdf, is_scannable):
    
    points = 100
    
    if checklist_list["name"] == False:
        points = points - 10
    if checklist_list["emails"] == False:
        points = points - 10
    if checklist_list["phoneNumber"] == False:
        points = points - 2
    if checklist_list["linkedin"] == False:
        points = points - 2
    if checklist_list["degree"] == False:
        points = points - 10
    if checklist_list["gpa"] == False:
        points = points - 5
    if checklist_list["startYear"] == False:
        points = points - 3
    if checklist_list["startMonth"] == False:
        points = points - 3
    if checklist_list["endYear"] == False:
        points = points - 3
    if checklist_list["endMonth"] == False:
        points = points - 3

    if not is_pdf:
        points = points - 20
    if not is_scannable:
        points = points - 15
    
    return points


def checklist(filename, resume_as_dict):
    flag = 0

    d = resume_as_dict
    response = {}

    response["name"] = not(d.get("names") == None)      #checks name
    
                      
    response["emails"] = not(d.get("emails") == None)   #checks email
    

    response["phoneNumber"] = not(d.get("phones") == None)   #checks phone number
    
    for add in d["links"]:
        if add.get("domain") == "linkedin.com":
            flag = flag + 1
    if flag == 0:
        response["linkedin"] = False           #checks linkedin account
    else:
        response["linkedin"] = True

    for edu in d["schools"]:
        if edu.get("degree") == None:
            response["degree"] = False               #checks degree
        else:
            response["degree"] = True 
        
        if edu.get("gpa") == None:
            response["gpa"] = False                   #checks GPA
        else:
            response["gpa"] = True 

    for time in d["positions"]:                                 #checks dates 
        if time.get("isCurrent") != None:
            if time.get("start").get("year") == None:
                response["startYear"] = False
            else:
                response["startYear"] = True
            if time.get("start").get("month") == None:
                response["startMonth"] = False
            else:
                response["startMonth"] = True
        else:
            if time.get("start").get("year") == None:
                response["startYear"] = False
            else:
                response["startYear"] = True
            if time.get("start").get("month") == None:
                response["startMonth"] = False
            else:
                response["startMonth"] = True
            if time.get("end").get("year") == None:
                response["endYear"] = False
            else:
                response["endYear"] = True
            if time.get("end").get("month") == None:
                response["endMonth"] = False
            else:
                response["endMonth"] = True
    
    return response












    
    



