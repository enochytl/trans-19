# Trans-19

Trans-19 is a knowledge management tool for recording confirmed cases and their history of visited locations, used by CHP.

## Major Features

Trans-19-1: 
1.	The ability to maintain (create, modify, delete, view) records of all patients confirmed with COVID-19 in Hong Kong, the record includes the patient’s name, identity document number, date of birth, the date on which the case was confirmed.

2.	The ability to maintain (create, modify, delete, view) records of locations, buildings and specific places within those buildings visited by patients in the 14-day period prior to being confirmed with COVID-19. The attributes of a record include the name of the location visited, address, grid coordinates, dates between the patient was present, details of a specific place, category of the location with respect to patient movements. 



## Usage

Run the Django project within the project root, where manage.py is present.

```bash
python manage.py runserver
```

## Records Page
The records page list all patients out in table format. Only the patient's information will be listed. 

## Full Profile Page
The full profile page list all the information of a particular patient, including the history of locations visited. 

## UI Usage Description

The table in the record page is clickable and will redirect user to the full profile of the patient. 

There is a back button below the title of the full profile of a patient, for redirecting the user back to the record page.



## License
[HKU](https://cs.hku.hk)