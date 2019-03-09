library(readr)
library(vegan)
library(dplyr)
library(tidyverse)

large_stock = c("002554","000059","002221","600759","600583","601808","600256","600339","600688","600871","600028","601857")

print_clust = function(df, name){
  pdf(paste0(name,".pdf"))
  hc = hclust(as.dist(df))
  height.vec = hc$height
  cat("clust",name, min(height.vec), max(height.vec), mean(height.vec), median(height.vec), var(height.vec), "\r\n")
  plot(hc, ann=FALSE, col="blue", cex=1.5)
  dev.off()
}

print_mst = function(df,name){
  pdf(paste0(name,"-mst.pdf"))
  sp = spantree(as.dist(df))
  degree = table(sp$kid)
  # cat("mst", name, min(degree), max(degree), mean(degree), var(degree), "\r\n")
  sp %>% plot(cex=0.7,type = "p", xaxt='n', yaxt='n', ann=FALSE, col="blue")
  dev.off()
}

print_dp = function(df_up, df_down, name){
  
  len = 26
  #df.up.small = select(df_up[!(row.names(df_up) %in% large_stock),], -large_stock)
  #df.up.large = select(df_up[(row.names(df_up) %in% large_stock),], large_stock)
  #df.dn.small = select(df_down[!(row.names(df_down) %in% large_stock),], -large_stock)
  #df.dn.large = select(df_down[(row.names(df_down) %in% large_stock),], large_stock)

  df_large.plot = data.frame(UP = numeric(), DOWN = numeric())
  df_small.plot = data.frame(UP = numeric(), DOWN = numeric())
  df_mix.plot = data.frame(UP = numeric(), DOWN = numeric())
  # stock_names = names(df_up)
  #print(stock_names)
  for (i in 1:(len-1)){
    for (j in (i+1):len){
      #print(stock_names[i] %in% large_stock)
      #print(stock_names[j] %in% large_stock)
      if ((names(df_up)[i] %in% large_stock) && (row.names(df_up)[j] %in% large_stock)){
        df_large.plot = rbind(df_large.plot, data.frame(UP = 1- df_up[j,i]^2 / 2, DOWN = 1- df_down[j,i]^2 / 2))
      } 
      else if (!(names(df_up)[i] %in% large_stock) && !(row.names(df_up)[j] %in% large_stock)){
        df_small.plot = rbind(df_small.plot, data.frame(UP = 1- df_up[j,i]^2 / 2, DOWN = 1- df_down[j,i]^2 / 2))
      }
      else {
        df_mix.plot = rbind(df_mix.plot, data.frame(UP = 1- df_up[j,i]^2 / 2, DOWN = 1- df_down[j,i]^2 / 2))
      }
    }
  }

  pdf(paste0(name,"-dplarge.pdf"))
  plot(x=df_large.plot$UP, y=df_large.plot$DOWN, xlab="Upturn", ylab="Ressesion", col="blue",xlim=c(-0.5, 1.0), ylim=c(-0.5, 1.0), pch=19,cex=.3) 
  segments(-3,-3,3,3)
  dev.off()

  pdf(paste0(name,"-dpsmall.pdf"))
  plot(x=df_small.plot$UP, y=df_small.plot$DOWN, xlab="Upturn", ylab="Ressesion", col="blue",xlim=c(-0.5, 1.0), ylim=c(-0.5, 1.0), pch=19,cex=.3) 
  segments(-3,-3,3,3)
  dev.off()

  len = length(df_mix.plot$UP)
  d.vec = numeric()
  dl.vec = numeric()
  for (i in 1:(len-1)){
    for (j in (i+1):len){
      d.vec = c(d.vec, sqrt((df_mix.plot$UP[i]-df_mix.plot$UP[j])^2+(df_mix.plot$DOWN[i]-df_mix.plot$DOWN[j])^2))
    }
  }
  
  for (i in 1:len){
    dl.vec = c(dl.vec, (df_mix.plot$DOWN[i]-df_mix.plot$UP[i])/sqrt(2))
  }
  
  cat("dpmix", name, min(d.vec), max(d.vec), mean(d.vec), median(d.vec), var(d.vec), "\r\n")
  cat("dpmix-dl", name, min(dl.vec), max(dl.vec), mean(dl.vec), median(dl.vec), var(dl.vec), "\r\n")
  
  pdf(paste0(name,"-dpmix.pdf"))
  plot(x=df_mix.plot$UP, y=df_mix.plot$DOWN, xlab="Upturn", ylab="Ressesion", col="blue",xlim=c(-0.5, 1.0), ylim=c(-0.5, 1.0), pch=19,cex=.3) 
  segments(-3,-3,3,3)
  dev.off()
}


col_names=c("000059","000096","000159","000554","000637","000819","002207","002221","002377","002554","002629","300084","300157","300164","300191","600028","600256","600339","600387","600583","600688","600759","600871","601808","601857","603003")

up_dist_files = list.files(pattern="*-up-dpxa")
dn_dist_files = list.files(pattern="*-dn-dpxa")

print(up_dist_files)
print(dn_dist_files)

tbl_dcca = lapply(up_dist_files, function(x) read.csv(x))
tbl_dpxa = lapply(dn_dist_files, function(x) read.csv(x))
names(tbl_dcca) = up_dist_files
names(tbl_dpxa) = dn_dist_files

for (i in 1:length(tbl_dpxa)){
  tbl_dcca[[i]][[1]] = NULL
  tbl_dpxa[[i]][[1]] = NULL
  names(tbl_dcca[[i]]) = col_names
  row.names(tbl_dcca[[i]]) = col_names
  names(tbl_dpxa[[i]]) = col_names
  row.names(tbl_dpxa[[i]]) = col_names

  #print(names(tbl_dcca[[i]]))
  #print(names(tbl_dpxa[[i]]))

  print_clust(tbl_dcca[[i]], names(tbl_dcca)[i])
  print_clust(tbl_dpxa[[i]], names(tbl_dpxa)[i])
  print_mst(tbl_dcca[[i]], names(tbl_dcca)[i])
  print_mst(tbl_dpxa[[i]], names(tbl_dpxa)[i])
  print_dp(tbl_dcca[[i]], tbl_dpxa[[i]], names(tbl_dpxa)[i])
}

#lapply(tbl_dcca, function(x) print_clust(x,names(x)[1]))
#lapply(tbl_dpxa, function(x) print_clust(x,names(x)[1]))

