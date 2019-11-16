// Simple program converted to C++ from C.

#include <iostream>
#include <vector>
using namespace std;

const int N = 40;  // Number of values we'll sum.

// Sum the numbers in the vector "input", and store the result in "output".
//
// Works for any type T that supports a += operator.
template <class T>
inline void sum(T& output, vector<T> input)
{
    output = 0;  // Initialize output to 0.

    // Add up all the numbers in d.
    for(typename vector<T>::const_iterator it = input.begin(); it != input.end(); ++it)
    {
        output += *it;
    }
}

int main(void)
{
    // Initialize the data we're going to sum, stored in a vector.
    vector<int> data;
    data.resize(N);  // Set the vector size explicitly.
    for(unsigned i = 0; i < data.capacity(); ++i)
    {
        // Initial values are just the index in the vector.
        data[i] = i;
    }

    int accum = 0;
    sum<int>(accum, data);

    cout << "sum is " << accum << endl;

    return(0);
}
