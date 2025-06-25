# Roadmap

### 1. Gather athlete images and info
- [x] Get the list of names from first sport page (find a better way of indexing the html element containing the info than what is currently implemented)
- [x] Retrieve relevant data from each athlete's page:
  - [x] Historical images
  - [x] Available personal data
- [ ] Repeat for other schools

### 2. Setup a Web Server
- [x] Write flask boiler plate
- [ ] Implement a page that sorts athletes by sport, gender, hometown, etc.
- [ ] Clicking on an athlete will expand them with a modal ui, showing all their data like the original website

### 3. Add CNN
- [ ] Run the facial attribute CNN on the images
- [ ] Merge these attributes with the each athlete's data
- [ ] Add to the website
