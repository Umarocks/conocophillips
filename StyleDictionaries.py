#Kyle K
#holds dictionaries assigning styles to certain sustainability levels
#ReserveEstimates hold the sustainability levels
#as well as the colors for the specific projects by conocophillips

#colors for borders representing sustainability
sustainColor = {
    "Immediate Action" : "red",
    "Not Sustainable" : "orange",
    "Somewhat Sustainable" : "yellow",
    "Sustainable" : "green",
    "Very Sustainable" : "blue"
}

#returns a border style using a sustainability grade from ReserveEstimates
def getSustainBorderStyle(sustainGrade):
    return {
        "color" : sustainColor[sustainGrade],
        "fillOpacity" : 0.2,
        "weight" : 4,
        "dashArray" : "4, 4"
    }

#colors of the specific icons of the sustainability projects tabbed
#colors must be in lowercase
conoconColor = {
    "Climate Change" : "#e40015",
    "Water" : "#0b2cd9",
    "Biodiversity" : "#21af90",
    "Stakeholder Engagement" : "#ff7100"
}
