Rtallyer <- function(x){
  library(TTR)
  library(lattice)
  library(stats)
  
  gainloss <- 0
  newgainloss <- 0
  algo <- 0
  comparer <- 0
  x <- unique(x)
  x <- x[,1]
  x <- x[!is.na(x)]
  rsiholder <- vector()
  arimaholder <- vector()
  xholder <- vector()
  newholder <- vector()
  compareholder <- vector()
  for (i in 1:length(x)){
    if(i > 2){
      rsi <- (RSI(x[1:i], i-1 ))
      rsi <- rsi[!is.na(rsi)]
      rsiholder <- c(rsiholder, rsi)
      Arima <- arima(x[1:i])$coef
      arimaholder <- c(arimaholder, unname(Arima))
      delta <- (x[i] - x[i-1])
      gainloss <- gainloss + delta
      xholder <- c(xholder, gainloss)
      rsi_indicator <- rsi
      arima_indicator <- 0
      if(rsi < 35){
        rsi_indicator <- 1
      }
      if(rsi > 80){
        rsi <- 0
      }
      rsioverall <- RSI(x, length(x)-1)
      rsioverall <- rsioverall[!is.na(rsioverall)]
      arimaoverall <- arima(x)$coef
      arimaoverall <- unname(arimaoverall)
      arimacoef1 <- 0
      arimacoef2 <- 0
      arimacoef3 <- rsioverall / 5
      if(Arima - x < 0){
        arimacoef1 <- 0.5
      }
      if(arimaoverall - x < 0){
        arimacoef2 <- 0.5
      }
      
      arimacoeff <- arimacoef1 + arimacoef2 + arimacoef3
      indicator <- (rsi_indicator / 2 + arimacoeff /2) 
      newdelta <- delta
      if(indicator > 0.5){
        newdelta <- delta * -1
      }
      if(indicator < 0.75){
        newdelta <- delta * 2
      }
      
      newgainloss <- newgainloss + newdelta
      newholder <- c(newholder, newgainloss)
      comparer <- comparer + (newgainloss - gainloss)
      compareholder <- c(compareholder, comparer)
      
    }
  }
  
  tsr<- ts(rsiholder)
  tsa<- ts(arimaholder)
  tsx<- ts(xholder)
  tsg<- ts(newholder)
  tsc<- ts(compareholder)
  plot(tsc)
  par(mfrow=c(2,2))
  plot(tsr)
  plot(tsa)
  plot(tsx)
  plot(tsg)
  
}