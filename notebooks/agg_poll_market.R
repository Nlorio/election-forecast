## loading the necessary packages
library(stringr)
library(pracma)
library(xml2)
library(rvest)
##
## read csv
clean_touchdown <- read.csv('clean_touchdown.csv',stringsAsFactors = FALSE)
DailymarketData = read.csv('Dailymarketdata_Fixed.csv', header=TRUE, sep='|', stringsAsFactors = FALSE)
##
## remove useless data
clean_touchdown <- clean_touchdown[,2:7]
clean_touchdown$Poll <- NULL
clean_touchdown$Spread <- NULL
DailymarketData$MarketSymbol <-NULL
DailymarketData$ContractSymbol <-NULL
DailymarketData<- DailymarketData[,1:4]
##
## get unique market id and name
unique_marketID = unique(DailymarketData$MarketId, incomparables = FALSE)
##
## divide the string to obtain all candidates names and topic in the cleantouch.csv
temp <- as.data.frame(str_split_fixed(clean_touchdown$Race.Topic..Click.to.Sort., "-", 2))
for (i in 1:100){
  # spilt all the candidates from xxx vs. xxx vs. xxx vs. xxx.......
  candidate_clean_touchdown <- as.data.frame(str_split_fixed(clean_touchdown$Results, ", ", i),stringsAsFactors = FALSE)
  if (dim(table(candidate_clean_touchdown[,i]))==1){
    candidate_clean_touchdown <- as.data.frame(str_split_fixed(clean_touchdown$Results, ", ", (i-1)),stringsAsFactors = FALSE)
    break
  }
}
## first row as topic
type <- temp[,1]
clean_touchdown$Race.Topic..Click.to.Sort.<- type
clean_touchdown$Results <-NULL
## joint clean touchdown and the processed candidate names
clean_touchdown<- cbind.data.frame(clean_touchdown,candidate_clean_touchdown,stringsAsFactors = FALSE)
##

## obtain useful data from clean touchdown to build the df_ct
date <- as.character(clean_touchdown[,1])
## this is raw data of topic without catagorizing
topic <- as.character(clean_touchdown[,2])
raw_topic <- as.character(clean_touchdown[,2])
year <- as.character(clean_touchdown[,3])
candidate <- matrix(NA, nrow = nrow(candidate_clean_touchdown), ncol = ncol(candidate_clean_touchdown))
col_n <- ncol(candidate)
for (i in 1:col_n){
  candidate[,i] <- as.character(clean_touchdown[,(3+i)])
  candidate[,i] <- gsub('[0-9]+','',candidate[,i])
  candidate[,i] <- str_trim(candidate[,i], side = c("both", "left", "right"))
}
##
#transforming topic different catagories
mayor <- grepl('mayor', topic,ignore.case = TRUE)
topic <- cbind.data.frame(topic,mayor,stringsAsFactors = FALSE)
topic$topic[topic$mayor==TRUE] <- 'mayor'
topic <- topic[,1]

senate_ornot <- grepl('Senate', topic,ignore.case = TRUE)
topic <- cbind.data.frame(topic,senate_ornot,stringsAsFactors = FALSE)
topic$topic[topic$senate_ornot==TRUE] <- 'Senate'
topic <- topic[,1]
presidential_app <- grepl('Approval', topic,ignore.case = TRUE)
topic <- cbind.data.frame(topic,presidential_app,stringsAsFactors = FALSE)
topic$topic[topic$presidential_app==TRUE] <- 'approval'
topic <- topic[,1]
governor <- grepl('governor', topic,ignore.case = TRUE)
topic <- cbind.data.frame(topic,governor,stringsAsFactors = FALSE)
topic$topic[topic$governor==TRUE] <- 'governor'
topic <- topic[,1]
direction <- grepl('direction', topic,ignore.case = TRUE)
topic <- cbind.data.frame(topic,direction,stringsAsFactors = FALSE)
topic$topic[topic$direction==TRUE] <- 'direction'
topic <- topic[,1]
congressional <- grepl('congressional', topic,ignore.case = TRUE)
topic <- cbind.data.frame(topic,congressional,stringsAsFactors = FALSE)
topic$topic[topic$congressional==TRUE] <- 'congression'
topic <- topic[,1]
district <- grepl('district', topic,ignore.case = TRUE)
topic <- cbind.data.frame(topic,district,stringsAsFactors = FALSE)
topic$topic[topic$district==TRUE] <- 'house'
topic <- topic[,1]

general <- grepl('general', topic,ignore.case = TRUE)
topic <- cbind.data.frame(topic,general,stringsAsFactors = FALSE)
topic$topic[topic$general==TRUE] <- 'election'
topic <- topic[,1]
state_list <- read.csv('state_list.csv',stringsAsFactors = FALSE)
for (i in 1:nrow(state_list)){
  state <- grepl(state_list[i,1], topic,ignore.case = TRUE)
  topic <- cbind.data.frame(topic,state,stringsAsFactors = FALSE)
  topic$topic[topic$state==TRUE] <- 'election'
  topic <- topic[,1]
}
Presidential_Nomination <- grepl('Presidential Nomination', topic,ignore.case = TRUE)
topic <- cbind.data.frame(topic,Presidential_Nomination,stringsAsFactors = FALSE)
topic$topic[topic$Presidential_Nomination==TRUE] <- 'election'
topic <- topic[,1]

Democratic_Presidential <- grepl('Democratic Presidential', topic,ignore.case = TRUE)
topic <- cbind.data.frame(topic,Democratic_Presidential,stringsAsFactors = FALSE)
topic$topic[topic$Democratic_Presidential==TRUE] <- 'election'
topic <- as.data.frame(topic,stringASFactors= FALSE)
topic <- topic[,1]

## 
## combine year and date in df_ct
df_ct <- cbind.data.frame(topic,year,date,candidate,stringsAsFactors = FALSE)
date <- paste(df_ct$year, df_ct$date, sep=" ")
df_ct[,2:3] <-NULL
df_ct <- cbind.data.frame(df_ct,date,stringsAsFactors = FALSE)
df_ct[df_ct==''] <-NA
df_ct[is.na(df_ct)]<-'None'
##

## df_ct and DailymarketData
DailymarketData$topic <- NA
DailymarketData$polling_date <- NA
for (i in 1:length(unique_marketID)){
  ct_temp <- df_ct
  dmd_temp <- subset(DailymarketData,DailymarketData$MarketId==unique_marketID[i])
#  dmd_temp <- subset(DailymarketData,DailymarketData$MarketId==id)
  dmd_n <- as.data.frame(unique(dmd_temp$ContractName),stringsAsFactors = FALSE)
  temp <- as.data.frame(str_split_fixed(dmd_n$`unique(dmd_temp$ContractName)`,' ', 2), stringsAsFactors = FALSE)
  firstName <- temp[,1]
  LastName <- temp[,2]
  if (all(grepl("^\\s*$", LastName,ignore.case = TRUE))){
    LastName <- firstName
  }
  ct_temp <- ct_temp[rowSums(ct_temp == LastName) != 0, ]
  if (nrow(ct_temp)==0){
    next
  }
  ct_temp$no_calls <- 0 
  for (j in 1:length(LastName)){
    stringname <- LastName[j]
    ct_temp$no_calls <- ct_temp$no_calls + rowSums(ct_temp == stringname)
  }
  max_temp <- max(ct_temp$no_calls)
  ct_temp <- subset(ct_temp,ct_temp$no_calls==max_temp)
  name_temp <- unique(dmd_temp$MarketName,incomparables = FALSE)
  #for (j in nrow(ct_temp):1){
  #    print(name_temp)
  #    if (!grepl(ct_temp$topic[j], name_temp, ignore.case = TRUE)){
  #      ct_temp <- ct_temp[-j,]
  #    }
  #  }
  DailymarketData$topic[DailymarketData$MarketId == unique_marketID[i]] <- ct_temp$topic[1]
  DailymarketData$polling_date[DailymarketData$MarketId == unique_marketID[i]] <- ct_temp$date[1]
}

DailymarketData <- subset(DailymarketData,!is.na(DailymarketData$topic))
rownum <- nrow(DailymarketData)
for (i in (nrow(DailymarketData):1)){
  if (!grepl(DailymarketData$topic[i], DailymarketData$MarketName[i],ignore.case = TRUE)){
    DailymarketData <- DailymarketData[-i,]
  }
}

write.csv(DailymarketData, file = "market+poll.csv")

