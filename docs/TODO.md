# Roadmap

### Gather athlete images and info
- [x] Get the list of names from first sport page (find a better way of indexing the html element containing the info than what is currently implemented)
- [x] Retrieve relevant data from each athlete's page:
  - [x] Historical images
  - [x] Available personal data
- [ ] List all universities that are made by Sidearm Sports and get their links from [here](https://cusn.ca/u-sports-map/)
- [ ] Add all of scraped data to a json file for fast reading
- [ ] Download all headshots
- [ ] Add the local directory location of the images to each athlete's dictionary
- [ ] Create a model.py file and a sqlalchemy schema
- [ ] Store in database
- [ ] Ensure that the code can be run again if needed

### Add CNN
- [ ] Figure out how to run the CNN code properly
- [ ] Run the facial attribute CNN on the images
- [ ] Merge these attributes with the each athlete's data
- [ ] Ensure that the code can be run again if needed

### Setup the Web Server
- [x] Write flask boiler plate
  - [x] Front/back end
  - [x] Database
- [ ] Implement a page that sorts athletes by sport, gender, hometown, etc.
- [ ] Clicking on an athlete will expand them with a modal ui, showing all their data like the original website
