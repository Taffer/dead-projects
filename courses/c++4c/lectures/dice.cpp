// C++ version

#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

const int sides = 6;

inline int r_sides()
{
	return (rand() % sides + 1);
}

int main(void)
{
	srand(clock());
	
	cout << endl << "Enter number of trials: ";
	int trials = 0;
	cin >> trials;
	
	int n_dice = 2;
	int *outcomes = new int[n_dice * sides + 1];
	for(int j = 0; j < trials; j++)
	{
		outcomes[r_sides() + r_sides()]++;
	}
	
	cout << "probability" << endl;
	for(int j = 2; j < n_dice * sides + 1; j++)
	{
		cout << "j = " << j
			 << " p = " << static_cast<double>(outcomes[j])/trials
			 << endl;
	}

	delete[] outcomes;
	
	return(EXIT_SUCCESS);
}
