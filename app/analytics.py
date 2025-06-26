import requests
from bs4 import BeautifulSoup
import json


# A dictionary of all the schools that use Sidearm Sports to write their website
schools = {

    "University of Alberta Golden Bears & Pandas": "bearsandpandas.ca",
    "Brandon UniversityBobcats": "gobobcats.ca",
    "University of British Columbia Thunderbirds": "gothunderbirds.ca",
    "University of British Columbia – Okanagan Heat": "goheat.ca",
    "University of Calgary Dinos": "godinos.com",
    "University of Lethbridge Pronghorns": "gohorns.ca",
    "University of Manitoba Bisons": "gobisons.ca",
    "Mount Royal University Cougars": "mrucougars.com",
    "University of Northern British Columbia Timberwolves": "unbctimberwolves.com",
    "University of Regina Cougars & Rams": "reginacougars.com",
    "University of Saskatchewan Huskies": "huskies.usask.ca",
    "Trinity Western University Spartans": "gospartans.ca",
    "University of Winnipeg Wesmen": "wesmen.ca",
    "University of Victoria Vikes": "govikesgo.com",

    "Algoma University Thunderbirds": "algomathunderbirds.ca",
    "Brock University Badgers": "gobadgers.ca",
    "University of Guelph Gryphons": "gryphons.ca",
    "McMaster University Marauders": "marauders.ca",
    "Nipissing University Lakers": "nulakers.ca",
    "Ontario Tech Ridgebacks": "goridgebacks.com",
    "Queen’s University Gaels": "gogaelsgo.com",
    "TMU Bold": "tmubold.ca",
    "University of Toronto Varsity Blues": "varsityblues.ca",
    "University of Waterloo Warriors": "athletics.uwaterloo.ca",
    "Western University Mustangs": "WesternMustangs.ca",
    "Wilfrid Laurier University Golden Hawks": "laurierathletics.com",
    "University of Windsor Lancers": "golancers.ca",
    "York University Lions": "yorkulions.ca",

    "Bishop’s University Gaiters": "gaiters.ca",
    "McGill University Redmen & Martlets": "mcgillathletics.ca"

}


# Returns a dictionary where the keys are the athlete ids and values are their names
# Helper for the get_athlete_detail()
def get_sport_data(school_url, sport):
    soup = BeautifulSoup(requests.get(f"https://{school_url}/sports/{sport}/roster").content, "html.parser")

    profiles = [i[:len(i)] for i in str(soup.find("script", type="application/ld+json")).split('Person')][1:]

    names = [i[i.index("name\":\"") + len("name\":\""):i.index("gender") - 3] for i in profiles]
    genders = [i[i.index("gender\":\"") + len("gender\":\""):i.index("gender\":\"") + len("gender\":\"") + 1] for i in
               profiles]
    ids = [i[i.index("rp_id=") + len("rp_id="):i.index("rp_id=") + len("rp_id=") + 5] for i in profiles]

    athletes = [{"id": ids[i], "name": names[i], "gender": genders[i], "school_url": school_url, "sport": sport} for i in range(len(ids))]


    for athlete in athletes:
        soup = BeautifulSoup(requests.get(f"https://{school_url}/sports/{sport}/roster/{athlete['name']}/{athlete['id']}").content, "html.parser")
        
        # Personal info
        player_field = soup.find("div", {"class": "sidearm-roster-player-fields"})
        if player_field is not None:
            span_eles = [span.get_text() for span in list(player_field.find_all("span"))]

            detail_dict = dict(zip(span_eles[::2], span_eles[1::2]))
            for key, val in detail_dict.items():
                athlete[key] = val
            
        # Image(s) (if any)
        athlete["images"] = []

        # No historical images; get from the main image pane
        if soup.find("section", {"class": "sidearm-roster-player-historical"}) is None:
            player_image = soup.find("div", {"class": "sidearm-roster-player-image"})
            if player_image is not None:
                short_image_url = player_image.find("img").attrs["src"]
                short_image_url = short_image_url[:short_image_url.index("width") - 1]
                athlete["images"].append(f"https://{school_url}{short_image_url}")
        else:    
            historical_imgs = soup.find_all("div", {"class": "sidearm-roster-player-image-historical"})    
            for img in historical_imgs:
                short_image_url = img.attrs["style"]
                if short_image_url.find("?") != -1:
                    short_image_url = short_image_url[short_image_url.index("'") + 1:short_image_url.index("?")]
                    athlete["images"].append(f"https://{school_url}{short_image_url}")

        print(f"name: {athlete["name"]}, sport: {athlete["sport"]}, school: {athlete["school_url"]}")

    return athletes


# Gets all of the data from all of the sports offered at the given school 
def get_school_data(school_url):

    soup = BeautifulSoup(requests.get(f"https://{school_url}/index.aspx", 
                                      headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content, "html.parser")  

    sports = list()

    for a in soup.find_all("a"):
        href = a.get("href")
        if href and href.find("/sports/") != -1 and href.count("/") == 2:
            sports.append(a["href"][a["href"].rfind("/") + 1:])

    sports = list(set(sports))

    print(sports)

    school_data = dict()
    for sport in sports:
        school_data[sport] = get_sport_data(school_url, sport)
        print(f"\n\n\nDONE {sport}\n\n\n")

    return school_data


def get_schools_data():
    schools_data = dict()
    for school, url in schools.items():
        schools_data[school] = get_school_data(url)
    return schools_data




# scrapes all of the available data from every school in the 'schools' dictionary
def scrape_all_schools():
    with open("data/all_schools_data.json", "w") as f:
            json.dump(get_schools_data(), f, indent=4)



# Reads the json file generated by the data scraped from the available schools
def get_school_json_data():
    with open("data/all_schools_data.json", "r") as f:
        return json.load(f)


print(get_school_json_data())
