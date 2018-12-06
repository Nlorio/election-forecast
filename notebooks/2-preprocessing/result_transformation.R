library(stringr)
library(pracma)
library(xml2)
library(rvest)
## direction 
RCP_direction <- read.csv('RCP_direction.csv',stringsAsFactors = FALSE)
direction <- as.data.frame(str_split_fixed(RCP_direction$Spread, ' ', 3),stringsAsFactors = FALSE)
direction$V2 <- NULL
direction$V3 <- str_extract_all(direction$V3, "[0-9]+")
direction$V3 <- strtoi(direction$V3)
direction$V3[direction$V1=='Wrong'] <- direction$V3[direction$V1=='Wrong']*-1
direction$V3[direction$V1=='Tie'] <- 0
direction$V1 <- NULL 
RCP_direction$Spread <- direction$V3
write.csv(RCP_direction, file = "RCP_direction.csv")
##############

## RCP_c_approval.csv
RCP_c_approval <- read.csv('RCP_c_approval.csv',stringsAsFactors = FALSE)
c_approval <- as.data.frame(str_split_fixed(RCP_c_approval$Spread, ' ', 2),stringsAsFactors = FALSE)
c_approval$V2 <- str_extract_all(c_approval$V2, "[0-9]+")
c_approval$V2 <- strtoi(c_approval$V2)
c_approval$V2[c_approval$V1=='Disapprove'] <- c_approval$V2[c_approval$V1=='Disapprove']*-1
c_approval$V2[c_approval$V1=='Tie'] <- 0
c_approval$V1 <- NULL
RCP_c_approval$Spread <- c_approval$V2
write.csv(RCP_c_approval, file = "RCP_c_approval.csv")
######################

## RCP_p_approval.csv
RCP_p_approval <- read.csv('RCP_p_approval.csv',stringsAsFactors = FALSE)
p_approval <- as.data.frame(str_split_fixed(RCP_p_approval$Spread, ' ', 2),stringsAsFactors = FALSE)
p_approval$V2 <- str_extract_all(p_approval$V2, "[0-9]+")
p_approval$V2 <- strtoi(p_approval$V2)
p_approval$V2[p_approval$V1=='Disapprove'] <- p_approval$V2[p_approval$V1=='Disapprove']*-1
p_approval$V2[p_approval$V1=='Tie'] <- 0
p_approval$V1 <- NULL
RCP_p_approval$Spread <- p_approval$V2
write.csv(RCP_p_approval, file = "RCP_p_approval.csv")
#######################

## RCP_house.csv
RCP_house <- read.csv('RCP_house.csv',stringsAsFactors = FALSE)
house <- as.data.frame(str_split_fixed(RCP_house$Spread, ' ', 2),stringsAsFactors = FALSE)
house$V2 <- str_extract_all(house$V2, "[0-9]+")
house$V2 <- strtoi(house$V2)
house$V2[house$V1=='Tie'] <- 0
house$V1 <- NULL
RCP_house$Spread <- house$V2
write.csv(RCP_house, file = "RCP_house.csv")
#######################

## RCP_approval.csv
RCP_approval <- read.csv('RCP_approval.csv',stringsAsFactors = FALSE)
approval <- as.data.frame(str_split_fixed(RCP_approval$Spread, ' ', 2),stringsAsFactors = FALSE)
approval$V2 <- str_extract_all(approval$V2, "[0-9]+")
approval$V2 <- strtoi(approval$V2)
approval$V2[approval$V1=='Disapprove'] <- approval$V2[approval$V1=='Disapprove']*-1
approval$V2[approval$V1=='Tie'] <- 0
approval$V1 <- NULL
RCP_approval$Spread <- approval$V2
write.csv(RCP_approval, file = "RCP_approval.csv")
#######################

## RCP_senate.csv
RCP_senate <- read.csv('RCP_senate.csv',stringsAsFactors = FALSE)
senate <- as.data.frame(str_split_fixed(RCP_senate$Spread, ' ', 2),stringsAsFactors = FALSE)
senate$V2 <- str_extract_all(senate$V2, "[0-9]+")
senate$V2 <- strtoi(senate$V2)
senate$V2[senate$V1=='Tie'] <- 0
senate$V1 <- NULL
RCP_senate$Spread <- senate$V2
write.csv(RCP_senate, file = "RCP_senate.csv")
#######################

## RCP_generic.csv
RCP_generic <- read.csv('RCP_generic.csv',stringsAsFactors = FALSE)
generic <- as.data.frame(str_split_fixed(RCP_generic$Spread, ' ', 2),stringsAsFactors = FALSE)
generic$V2 <- str_extract_all(generic$V2, "[0-9]+")
generic$V2 <- strtoi(generic$V2)
generic$V2[generic$V1=='Democrats'] <- generic$V2[generic$V1=='Democrats']*-1
generic$V2[generic$V1=='Tie'] <- 0
generic$V1 <- NULL
RCP_generic$Spread <- generic$V2
write.csv(RCP_generic, file = "RCP_generic.csv")
#######################

## RCP_governor.csv
RCP_governor <- read.csv('RCP_governor.csv',stringsAsFactors = FALSE)
governor <- as.data.frame(str_split_fixed(RCP_governor$Spread, ' ', 2),stringsAsFactors = FALSE)
governor$V2 <- str_extract_all(governor$V2, "[0-9]+")
governor$V2 <- strtoi(governor$V2)
governor$V2[governor$V1=='Tie'] <- 0
governor$V1 <- NULL
RCP_governor$Spread <- governor$V2
write.csv(RCP_governor, file = "RCP_governor.csv")
#######################

