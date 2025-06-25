import requests
from bs4 import BeautifulSoup



# Returns a dictionary where the keys are the athlete ids and values are their names
# Helper for the get_athlete_detail()
def get_sport_data(school_url, sport):
    soup = BeautifulSoup(requests.get(f"https://{school_url}/sports/{sport}/roster").content, "html.parser")

    profiles = [i[:len(i)] for i in str(soup.find("script", type="application/ld+json")).split('Person')][1:]

    names = [i[i.index("name\":\"") + len("name\":\""):i.index("gender") - 3] for i in profiles]
    genders = [i[i.index("gender\":\"") + len("gender\":\""):i.index("gender\":\"") + len("gender\":\"") + 1] for i in
               profiles]
    ids = [i[i.index("rp_id=") + len("rp_id="):i.index("rp_id=") + len("rp_id=") + 5] for i in profiles]

    athletes = [{"id": ids[i], "name": names[i], "gender": genders[i]} for i in range(len(ids))]


    for athlete in athletes:
        soup = BeautifulSoup(requests.get(f"https://{school_url}/sports/{sport}/roster/{athlete['name']}/{athlete['id']}").content, "html.parser")
        
        # Personal info

        player_field = soup.find("div", {"class": "sidearm-roster-player-fields"})
        
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
                print(short_image_url)
                if short_image_url.find("?") != -1:
                    short_image_url = short_image_url[short_image_url.index("'") + 1:short_image_url.index("?")]
                    athlete["images"].append(f"https://{school_url}{short_image_url}")


    return athletes



get_sport_data("gothunderbirds.ca", "cross-country")






# Gets all of the data from all of the sports offered at the given school 
def get_school_data(school):
    pass
