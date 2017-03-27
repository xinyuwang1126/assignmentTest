setwd("/Users/xinyuwang/Desktop/CSE6740ML/homework3_data")
data=read.csv("OPCA.csv",header=FALSE)
v=read.csv("True_eigvector.csv",header=FALSE)
v=data.matrix(v)
d=20
w=matrix(1/sqrt(d),d,1)
eta=0.01
i=1
dist_wi_v<-NULL
iter<-NULL
while(i<1001)
{
  A<-data[((i-1)*20+1):(i*20),1:20]
  A<-data.matrix(A)
  w_new<-w+eta*A%*%w
  w_new<-w_new/norm(w_new,type="2")
  w<-w_new
  dist<-1-(t(w)%*%v)*(t(w)%*%v)
  dist_wi_v<-c(dist_wi_v,dist)
  iter<-c(iter,i)
  i<-i+1
}
plot(iter,dist_wi_v)


