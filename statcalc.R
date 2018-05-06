statcalc <- function(x, size = 120){
  library(TTR)
  library(stats)
  x <- ts(x)
  arima <- arima(x, c(0,0,0))
  rsi <- RSI(x, size - 1)[size]
  list <- c(arima$coef, rsi)
  return(as.array(list))
}