This was a course project from the Complete SQL Mastery course from Coding with Mosh.

The prompt was an airline flight booking receipt (see bottom of this document), and the problem was to design a database model that could be used to populate the fields of such a receipt (nothing more and nothing less!) and support an Online Transaction Processing System. 

The first step was to identify the entities and the relationship involved. To do this I drew up a conceptual model using draw.io. The next step was to flesh things out more in a logical model which defined the specific data types involved, and added a few more entity tables to normalize the data and avoid repetition. 

See the models here:
https://drive.google.com/file/d/1xdcGjdEhYdo4EjGjD6T5LQGjFegXS7wd/view

The third step was to implement the logical model into a physical one. For this, I went with MySQL and diagrammed the model there and had the software generate the SQL script to establish a database that would be ready to use. The transition into a physical model is where the primary and foreign keys are designated, the specifics of the data types and constraints are assigned, and a final review is made to ensure attributes are normalized, i.e. no data is needlessly repeated. A conscious choice was made to de-normalize city and state information listed in the airport entity, since these fields will conceivably always be paired, and to not introduce a new table. Similarly, the tickets table was set to have an auto-incremented primary key, as opposed to a composite key. This is to allow the option for a single customer to book multiple seats. These were practical choices made, but it could have been done differently. Of course, in a real world scenario, when in doubt about design choices like these–- ask the business! 



**************************************************************************
Los Angeles, CA -> San Francisco, CA
San Francisco, CA -> Los Angeles, CA
Fri Apr 05 2019 -> Sun Apr 07 2019
2 Tickets
Airline Confirmation Numbers
Alaska Airline: TAEGKX
Passengers and Ticket Numbers:
John Smith
Ticket Number: 0177200658
Jennifer Smith
Ticket Number: 0178410326

Fri Apr 05
Los Angeles -> San Francisco
LAX -> SFO
08:20 AM - 09:35 AM
Alaska Airlines Flight 1490
1h 15m, 236 miles
Depart: Los Angeles Intl Airport (LAX)
Arrive: San Francisco Intl Airport (SFO)
Economy Class

Sun Apr 07
San Francisco -> Los Angeles
SFO -> LAX
02:00 PM - 03:15 PM
Alaska Airlines Flight 1473
1h 15m, 236 miles
Depart: San Francisco Intl Airport (SFO)
Arrive: Los Angeles Intl Airport (LAX)
Economy Class
**********************************************************************
