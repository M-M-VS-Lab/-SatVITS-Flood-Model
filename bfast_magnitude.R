setwd('C:/Users/Owner/Desktop/rstudio/msavi')
df = read.csv(file = "avh_roi_msavi.csv")
df[is.na(df)] = 0
sp_vector <- as.vector(df['msavi'])
vec1 <- df$msavi
sp_ts <- ts(vec1,start=c(1981,7),frequency=365.1)

fit <- bfast(sp_ts, h=0.06 , season = "harmonic", max.iter = 1)
plot(fit)
library(tidyverse)
fit[["output"]][[1]][["Tt"]]
fit[["output"]][[1]][["St"]]
fit[["output"]][[1]][["Nt"]]
fit[["output"]][[1]][["Vt"]]
fit[["output"]][[1]][["bp.Vt"]][["breakpoints"]]


dat = fit[["output"]][[1]][["Tt"]]
Tt = data.frame(Y=as.matrix(dat), date=time(dat))
dat = fit[["output"]][[1]][["St"]]
St = data.frame(Y=as.matrix(dat), date=time(dat))
dat = fit[["output"]][[1]][["Nt"]]
Nt = data.frame(Y=as.matrix(dat), date=time(dat))
dat = fit[["output"]][[1]][["Vt"]]
Vt = data.frame(Y=as.matrix(dat), date=time(dat))
dat = fit[["output"]][[1]][["bp.Vt"]][["breakpoints"]]
Bt = data.frame(Y=as.matrix(dat), date=time(dat))

Tt_l =Tt["Y"]#Tt
St_l = St["Y"]#St
Nt_l = Nt["Y"]#et
Vt_l = Vt["Y"]#Vt
Bt_l = Bt["Y"]#Bt
Dt_l= df['date']

length(Dt_l) <- length(St_l)


df_csv<-data.frame(Dt_l,Tt_l,St_l,Nt_l,Vt_l)

#df %>%
#  rename(
#    Tt_l = Y,
#    St_l = Y.1,
#    et_l = Y.2,
#    ndvi_l = Y.3
#  )

write.csv(df_csv,"C:/Users/Owner/Desktop/rstudio/msavi/avh/avh_roi_msavi_bfast.csv", row.names = FALSE)
mags <- fit[["Mags"]]
df_csv<-data.frame(mags,Bt_l)
write.csv(df_csv,"C:/Users/Owner/Desktop/rstudio/msavi/avh/avh_roi_msavi_mags.csv", row.names = FALSE)
