#include<stdio.h>
#include <stdlib.h>
#include <time.h>
void main(){
	int num;
	while(1){
		printf("����������Ĵ���,�ԡ�-1���˳�����Ҫ���ڵ���1����");
		scanf("%d",&num);
		if(num<1 && num!= -1){
			printf("����������m�������أ�");
			return;
		}
		if(num == -1)
			break;
		double result;
		double total = 0;
		int*Lucky,*Bouns;
		Lucky = (int*)malloc(sizeof(int)*100000);
		Bouns = (int*)malloc(sizeof(int)*100000);
		srand(time(NULL));
		for(int i=0;i<num;i++){ 
			Lucky[i] = rand()% 5 + 1;
			Bouns[i] = rand()% 5 + 1;
		}
		for(int i=0;i<num;i++){				
			switch(Lucky[i]){
				case 1:
					result = -2.11;
					break;
				case 2:
					if(Bouns[i]<6)
						result = -1.11;
					else
						result = -2.99;
					break;
				case 3:
					if(Bouns[i]<5)
						result = 0.89;
					else
						result = -2.99;
					break;
				case 4:
					if(Bouns[i]<4)
						result = 8.88 - 2.99;
					else
						result = -2.99;
					break;
				case 5:
					if(Bouns[i]<3)
						result = 12.88 - 2.99;
					else
						result = -2.99;
					break;
				case 6:
					if(Bouns[i]<2)
						result = 28.88 - 2.99;
					else
						result = -2.99;
					break;
				default:
					break;
			}
			total += result;
			printf("��%d�����˵���Ϊ%d���н�����Ϊ%d,������������ǣ�%f\n",i+1,Lucky[i],Bouns[i],result);
			result = 0;
		}
		
		printf("\n��ʦ�������ܹ������ǣ�%f",total);
		if(total>0)
			printf("  ����˵�̫�磬������׬�ˣ��Ȼ���͵����ϵ׿�\n\n");
		else
			printf("  ���������ң�������\n\n");
	}
	system("pause");
	return;
}