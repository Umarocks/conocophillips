#Kyle K
#basic arithmetic, use known resource reserve and production to generate run out year
#if not yearly (= false), then divide resulting year by 12
#reserves should be in the same unit

prodTimeframe = {"yearly":1, "quarterly":4, "monthly":12}

def dryReserveEstimate(reserve, production, prodTime, currentYear):
    #prodTime should either be yearly, quarterly, or monthly
    dryTime = reserve / production #integer that's times bigger than year
    dryYear = dryTime / prodTimeframe[prodTime]      #to get it to a normal year
    dryYear += currentYear

    #note: should be formatted to have different decimal places (none, to 3)
    # print(dryYear)
    return dryYear


#compare with deadlineYear using dry. If dry before deadline, then poor grade
#returns grade as string, may need to define new dictionary
def immediateSustainableConsumption(dryYear, deadlineYear, currentYear):
    currentDifference = dryYear - currentYear #positive, then dry after current
    dryDifference = dryYear - deadlineYear #if positive, then dry after dead
    if(currentDifference < 5): #5 years after current
        return "Immediate Concern"
    elif(currentDifference < 10):
        return "Not Sustainable"
    elif(dryDifference < 10):
        return "Somewhat Sustainable"
    elif(dryDifference < 20):
        return "Sustainable"
    else:
        return "Very Sustainable"

#use proper casing for boolean constants
# drY = dryReserveEstimate(500, 20, "monthly", 201)
#get 226 for yearly, 207 for quarterly, and 203 monthly
# print( immediateSustainableConsumption(drY, 211, 201) )
