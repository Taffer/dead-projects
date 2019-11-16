/* Monte Carlo Simulation */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIDES 6
#define R_SIDE (rand() % SIDES + 1)

int main(void)
{
	int trials;
	int j;
	int d1, d2;
	int outcomes[13];  /* 2-12 used */
	int n_dice;

	n_dice = 2;

	for(j = 0; j < 13; j++)
	{
		outcomes[j] = 0;
	}
	
	srand(clock());

	printf("\nEnter number of trials: ");
	scanf("%d", &trials);
	for(j = 0; j < trials; ++j)
	{
		outcomes[(d1 = R_SIDE) + (d2 = R_SIDE)]++;
	}
	
	printf("probability\n");
	for(j = 2; j < n_dice * SIDES + 1; ++j)
	{
		printf( "j = %d p = %lf\n", j, (double)(outcomes[j])/(double)trials);
	}
	
	return(EXIT_SUCCESS);
}
