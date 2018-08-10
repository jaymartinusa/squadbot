import re

# Consts for map bot
LAYER_FILENAME = "squadlayers.txt"

def searchLayers(terms, request, platform):
    if terms == "help":
        if platform == "discord":
            output = """The search command is used to find layers that meet certain parameters, or find information about particular layers.\n
Usage follows this format:\n
<>?search \"[term term]\" \"[type of information (optional)]\"</>\n
To find the mini-map of a certain layer type: \n
<>?search \"Al Basrah PAAS v1\" \"Minimap\"</>\n
To list all layers with armored SPG vs British faction type:\n
<>?search \"SPG-A GBR\"</>
Terms to search for include:
<>All maps (Al Basrah, Belaya, etc.)\n
All gamemodes (AAS, PAAS, Insurgency, Invasion)\n
All Factions (GBR, INS, MIL, RU, US)\n
All Vehicles (British Transport - Warrior, CROWS MRAP - OT MRAP, Techie Logistics - DShK-AS - AA Truck, MTLB - BTR-30mm)</>\n
Types of information include: <>
Map, Layer, Gamemode, Minimap, BLUFOR, BLUFOR Tickets, BLUFOR Spawn (Map), BLUFOR Spawn (Aerial), BLUFOR Secondary Spawn (Map), BLUFOR Secondary Spawn (Aerial), BLUFOR Vehicles, OPFOR    OPFOR Tickets, OPFOR Spawn (Map), OPFOR Spawn (Aerial), OPFOR Secondary Spawn (Map), OPFOR Secondary Spawn (Aerial), OPFOR Vehicles</>"""
        if platform == "reddit":
            output = """
The ?squadbotsearch command is used to find squad layers that meet certain parameters and find information about particular layers.

Usage follows this format:

>?squadbotsearch \"[term term]\" \"[type of information (optional)]\"

To find the mini-map of a certain layer type:

>?squadbotsearch \"Al Basrah Invasion V2\" \"Minimap\"

To list all layers with armored SPG and the British faction on Al Basrah type:

>?squadbotsearch \"Al Basrah GBR SPG-A\"

To list all conquest mode layers type:

>?squadbotsearch "conquest"

Terms to search for include:

+ All gamemodes (AAS, PAAS, Insurgency, Invasion)

+ All Factions (GBR, INS, MIL, RU, US)

+ All Vehicles (British Transport - Warrior, CROWS MRAP - OT MRAP, Techie Logistics - DShK-AS - AA Truck, MTLB - BTR-30mm)

Types of information include:

> Map, Layer, Gamemode, Minimap, BLUFOR, BLUFOR Tickets, BLUFOR Spawn (Map), BLUFOR Spawn (Aerial), BLUFOR Secondary Spawn (Map), BLUFOR Secondary Spawn (Aerial), BLUFOR Vehicles, OPFOR, OPFOR Tickets, OPFOR Spawn (Map), OPFOR Spawn (Aerial), OPFOR Secondary Spawn (Map), OPFOR Secondary Spawn (Aerial), OPFOR Vehicles
"""
        return output

    #print(terms)
    termList = terms.split(" ")
    #print(termList)
    file = open(LAYER_FILENAME, "r")
    i = 0;
    meetTerms = [];
    for line in file:
        if "".join(termList).lower() == (getSpecific(i,"Map")+getSpecific(i,"Layer")).replace(" ", "").lower():
            print("Meets exact layer")
            meetTerms = [i]
            break
        doesMeet = termsInLine(termList, removeLinks(line))
        #print(doesMeet)
        if doesMeet:
            meetTerms.append(i)
        i+=1
    if len(meetTerms) == 0:
        output = "There were no layers that met your search. Try again with less restrictive terms."

    elif len(meetTerms) == 1:
        output = ""
        if request:
            #print ("Request(sqdbot): "+ request[0])
            #print ("Request[0]: "+str(request[0]))
            output += getSpecific(meetTerms[0], "Map") + " " + getSpecific(meetTerms[0], "Layer") +" " + request[0] + ":\n"
            result = getSpecific(meetTerms[0], request[0])
            if re.match(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', result):
                if platform == "discord":
                    output += result
                elif platform == "reddit":
                    output += "["+request[0]+"]("+result+")"
            else:
                if platform == "discord":
                    output += "```" + result + "```"
                elif platform == "reddit":
                    output += ">"+result
        else:
            if platform == "discord":
                output += "**"+getSpecific(meetTerms[0], "Map") + " " + getSpecific(meetTerms[0], "Layer") + "**\n"
                output += getSpecific(meetTerms[0], "BLUFOR") + " vehicles:\n"
                output += "<>" + getSpecific(meetTerms[0], "BLUFOR Vehicles") + "</>"
                output += getSpecific(meetTerms[0], "OPFOR") + " vehicles:\n"
                output += "<>" + getSpecific(meetTerms[0], "OPFOR Vehicles") + "</>"
                output += getSpecific(meetTerms[0], "Minimap")
            elif platform == "reddit":
                output += "**"+getSpecific(meetTerms[0], "Map") + " " + getSpecific(meetTerms[0], "Layer") + "**\n\n"
                output += getSpecific(meetTerms[0], "BLUFOR") + " vehicles:\n\n"
                output += ">" + getSpecific(meetTerms[0], "BLUFOR Vehicles") + "\n\n"
                output += getSpecific(meetTerms[0], "OPFOR") + " vehicles:\n\n"
                output += ">" + getSpecific(meetTerms[0], "OPFOR Vehicles") + "\n\n"
                output += "[Minimap]("+getSpecific(meetTerms[0], "Minimap")+")"
                
    elif len(meetTerms) > 1:
        output = "There are " + str(len(meetTerms)) + " layers that meet your terms: "+terms
        if platform == "discord":
            output += "```"
        elif platform == "reddit":
            output += "\n\n"
        for lineNumber in meetTerms:
            if platform == "discord":
                output += getSpecific(lineNumber, "Map") + " " + getSpecific(lineNumber, "Layer") + " " + getSpecific(lineNumber, "BLUFOR") + "v" + getSpecific(lineNumber, "OPFOR") + "\n"
            elif platform == "reddit":
                output += ">+ "+getSpecific(lineNumber, "Map") + " " + getSpecific(lineNumber, "Layer") + " " + getSpecific(lineNumber, "BLUFOR") + "v" + getSpecific(lineNumber, "OPFOR")+"\n"
        if platform == "discord":
            output += "```"
        elif platform == "reddit":
            output += "\n\n"
        output += "Try to narrow down your search."
    return output
    
# Function to check if a layer meets the search terms            
def termsInLine(terms, line):
    for term in terms:
        if term.lower() not in line.lower():
            return False
    return True

# Pulls a specific function from a specific layer
def getSpecific(lineNumber, prop):
    lines = []
    file = open(LAYER_FILENAME, "r")
    for line in file:
        lines.append(line)

    currentLine = lines[lineNumber]
    props = currentLine.split("\t")

    i=0
    for colTitle in lines[0].split("\t"):
        if re.sub(r'[\n]', '', colTitle.lower()) == prop.lower():
            return props[i]
        i+=1
    output = "The information of the requested type was not found. Options are: "
    for colTitle in lines[0].split("\t"):
        output += colTitle + ", "
    return output

# Gets a line from the file except for the image links
def removeLinks(inputString):
    outputString = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', inputString)
    return(outputString)
