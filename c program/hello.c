#include<stdio.h>
int main(){
	int i=121,temp, r, rev=0;
	while(temp!=0){
		temp =i;
		r=temp%10;
		rev=rev*10+r;
		temp=temp/10;
	}	
	if(i==rev){
		printf("yes");
	}
	else{
		printf("no");
	}
	return 0;
}
