library(plyr)
library(stringr)
library(robustHD)
## read csv and extra useful info and rename
header.true <- function(df) {
  names(df) <- as.character(unlist(df[1,]))
  df[-1,]
}
pollster <- read.csv('pollster.csv',header = TRUE,stringsAsFactors = FALSE)
pollster <- header.true(pollster)
pollster <- cbind(pollster[,2],pollster[,11])
pollster <- as.data.frame(pollster, stringsAsFactors = FALSE)
col_name <- colnames(pollster)
names(pollster)[names(pollster)==col_name[1]] <- "pollster"
names(pollster)[names(pollster)==col_name[2]] <- "grade"
pollster$pollster <- str_replace(pollster$pollster, 'Public Policy Polling', 'PPP')
gradetoscore <- read.csv('gradetoscore.csv',stringsAsFactors = FALSE)
pollster <- as.data.frame(pollster, stringAsFactors=FALSE)
for (i in 1:nrow(gradetoscore)){
  pollster$grade[pollster$grade==gradetoscore[i,1]]<-(gradetoscore[i,2])
}
pollster$grade <- as.numeric(pollster$grade)
#####################

## assign grade for the pollster
assign_grade <- function(df,pollster){
  poll <- gsub("\\s*\\([^\\)]+\\)","",as.character(df$Poll))
  poll <- gsub("\\*","",poll)
  poll <- as.data.frame(poll,stringsAsFactors = FALSE)
  t <- 1
  while (TRUE){
    temp <- as.data.frame(str_split_fixed(poll$poll, "/", t),stringsAsFactors = FALSE)
    if (dim(table(temp[,t]))==1){
      t <- t - 1
      break
    }
    t <- t + 1
  }
  poll <-cbind.data.frame(poll, as.data.frame(str_split_fixed(poll$poll, "/", t),stringsAsFactors = FALSE))
  poll$grade <- NA
  pollster$TF <- NA
  for (i in 1:nrow(poll)){
    num <- 0
    for (j in 1:(ncol(poll)-1)){
      if (poll[i,j]==''){
        next
      }
      temp <- grepl(poll[i,j],pollster[,1],ignore.case=TRUE)
      pollster$TF <- as.numeric(temp)
      temp <- pollster$grade[pollster$TF==TRUE]
      if (!isempty(temp)){
        if(max(temp)>num){
          num <- max(temp)
          }
        if (j == 1){
          break
        }
      }
    }
    num <- num
    poll$grade[i] <- num
  }
  df$poll_grade <- poll$grade
  res <- df
}
gradetoscore[14,1] <- 'unknown'
gradetoscore[14,2] <- 0

## 
## direction 
df <- read.csv('RCP_direction.csv',stringsAsFactors = FALSE)
df <- assign_grade(df,pollster)
for (i in 1:14){
  df$poll_grade[df$poll_grade==gradetoscore$Score[i]] <- gradetoscore$Grade[i]
}
write.csv(df, file = "RCP_direction.csv")
##############

## RCP_c_approval.csv
df <- read.csv('RCP_c_approval.csv',stringsAsFactors = FALSE)
df <- assign_grade(df,pollster)
for (i in 1:14){
  df$poll_grade[df$poll_grade==gradetoscore$Score[i]] <- gradetoscore$Grade[i]
}
write.csv(df, file = "RCP_c_approval.csv")
######################

## RCP_p_approval.csv
df <- read.csv('RCP_p_approval.csv',stringsAsFactors = FALSE)
df <- assign_grade(df,pollster)
for (i in 1:14){
  df$poll_grade[df$poll_grade==gradetoscore$Score[i]] <- gradetoscore$Grade[i]
}
write.csv(df, file = "RCP_p_approval.csv")
#######################

## RCP_house.csv
df <- read.csv('RCP_house.csv',stringsAsFactors = FALSE)
df <- assign_grade(df,pollster)
for (i in 1:14){
  df$poll_grade[df$poll_grade==gradetoscore$Score[i]] <- gradetoscore$Grade[i]
}
write.csv(df, file = "RCP_house.csv")
#######################

## RCP_approval.csv
df <- read.csv('RCP_approval.csv',stringsAsFactors = FALSE)
df <- assign_grade(df,pollster)
for (i in 1:14){
  df$poll_grade[df$poll_grade==gradetoscore$Score[i]] <- gradetoscore$Grade[i]
}
write.csv(df, file = "RCP_approval.csv")
#######################

## RCP_senate.csv
df <- read.csv('RCP_senate.csv',stringsAsFactors = FALSE)
df <- assign_grade(df,pollster)
for (i in 1:14){
  df$poll_grade[df$poll_grade==gradetoscore$Score[i]] <- gradetoscore$Grade[i]
}
write.csv(df, file = "RCP_senate.csv")
#######################

## RCP_generic.csv
df <- read.csv('RCP_generic.csv',stringsAsFactors = FALSE)
df <- assign_grade(df,pollster)
for (i in 1:14){
  df$poll_grade[df$poll_grade==gradetoscore$Score[i]] <- gradetoscore$Grade[i]
}
write.csv(df, file = "RCP_generic.csv")
#######################

## RCP_governor.csv
df <- read.csv('RCP_governor.csv',stringsAsFactors = FALSE)
df <- assign_grade(df,pollster)
for (i in 1:14){
  df$poll_grade[df$poll_grade==gradetoscore$Score[i]] <- gradetoscore$Grade[i]
}
write.csv(df, file = "RCP_governor.csv")

