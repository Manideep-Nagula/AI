#include <iostream> //cout.
#include <list> //List Container.

using namespace std; 
const int n = 3; // rows + columns size.

// State Class Definition.
class State {
public:
int A[n][n], g; // State Array, General Cost
State *parent; //Parent Pointer.
State(){}//Constructor

bool is_goal(); // true: state is goal. // false: state is not goal.
bool operator==(const State &) const; //Logical equality Operator.
void print(); //State Array Printing function.
};

int Goal[n][n] = { { 1,2,3 },{ 4,5,6 },{ 7,8,0 } }; //Goal Array


list< State > closed, fringe; // Tested States, Active States Lists.
State start, cur, temp; // Start, Current, Temporary States.
void IDS(); // IDS Search function.

void Expand(); // State space Expander function.
void PrintPath(State *s); // Solution Path Print function.
bool InClosed(State &s); // to search for state in the Closed List.
bool isSolvable(int A[n][n]); // to check if the given 8-tile is solvable or not
int getInvCount(int arr[]); // calculates the inversion count of the 8-tile 


int main() {
//initializing the start state.
start.g = 0; // start cost

start.parent = NULL; // no parent for the start state.

cout << "Enter the initial State:\n";
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            cin >> start.A[i][j];
        }
    }
    
    /* not solvable
    	8 1 2
    	0 4 3
    	7 6 5
    */
if(isSolvable(start.A)){
	
	IDS(); // executing the ids algorithm.
}
else{
	cout<<"\nThe Given 8-tile is not solvable";
}

getchar();
return 0;
}


// A utility function to count inversions in given array 'arr[]'
int getInvCount(int arr[])
{
    int inv_count = 0;
    for (int i = 0; i < 9 - 1; i++)
        for (int j = i+1; j < 9; j++)
             // Value 0 is used for empty space
             if (arr[j] && arr[i] &&  arr[i] > arr[j])
                  inv_count++;
                  
    printf("Inverse count : %d",inv_count);
    return inv_count;
}
 
// This function returns true if given 8 puzzle is solvable.
bool isSolvable(int A[3][3])
{
    // Count inversions in given 8 puzzle
    int invCount = getInvCount((int *)A);
 
    // return true if inversion count is even.
    return (invCount%2 == 0);
}

// state goal tester.
bool State::is_goal() {

int i, j;
for (i = 0; i < n; i++) {
for (j = 0; j < n; j++) {
// if any two same positioned items not equal.
if (A[i][j] != Goal[i][j])
// this state is not the goal.
return false;
}
}

//this state is the goal state.
return true;
}
// state array printer.
void State::print() {
int i, j;
for (i = 0; i < n; i++) {
for (j = 0; j < n; j++)
cout << A[i][j] << ' ';
cout << endl;
}
cout << endl;
}
// state logical equality operator.
bool State::operator==(const State &r) const {
int i, j;
for (i = 0; i < n; i++) {
for (j = 0; j < n; j++) {
// if any two same positioned items not equal.
if (A[i][j] != r.A[i][j])
// states are not equal
return false;
}
}
//reaching this point means all items in both states are equal.
// states are equal
return true;
}
// 

// Iterative deepning search.
void IDS() {

int depth=0; // Depth cost.
cout << "\nStarting IDS Algorithm... \n";
while(true){
cur = start;
fringe.push_front(cur);
while (!fringe.empty())
{
// process the fringe states .
cur = fringe.front();
// if the front is goal.
if (cur.is_goal()) {

//print the solution path.
cout << "Path:\n";
PrintPath(&cur);
// exit the function
return;
} //if state not the goal and in the search depth.
else if (depth > cur.g)
{
//expand the state.
Expand();
}
else { //not useable state.
//pop it out
fringe.pop_front();
}
}
// clear both lists for the next round.
fringe.clear();
closed.clear();
// increase the search depth.
depth++;
}
}

// State space Expanding Function.
void Expand() {

//add current state to the closed list.
closed.push_back(cur);
int i, j;
for (i = 0; i < n; i++) {
for (j = 0; j < n; j++) {
//finding the 0 element in the state array.
if (cur.A[i][j] == 0) {
// if the 0 not in the first row.
if (i > 0) {
// set the child basic elements
temp = cur;
temp.parent = &(closed.back());
// shift the zero element UP..
swap(temp.A[i][j], temp.A[i - 1][j]);
// search for the child in the closed list.
// if the child not found in the closed list.
if (!InClosed(temp)) {
//set remaining elements
temp.g += 1;

fringe.push_front(temp); //push the child into the fringe list

}
}
//if the 0 is not in the last row.
if (i < n-1) {
temp = cur;
temp.parent = &(closed.back());
//shift the zero element DOWN.
swap(temp.A[i][j], temp.A[i + 1][j]);
if (!InClosed(temp)) {
temp.g += 1;

fringe.push_front(temp);

}
}// if the 0 element not in the first column.
if (j > 0) {
temp = cur;
temp.parent = &(closed.back());
// shift it LEFT.
swap(temp.A[i][j], temp.A[i][j - 1]);
if (!InClosed(temp)) {
temp.g += 1;

fringe.push_front(temp);

}
}// if the zero elemnt not in the last column.
if (j < n-1) {
temp = cur;
temp.parent = &(closed.back());
// shift it RIGHT.
swap(temp.A[i][j], temp.A[i][j + 1]);
if (!InClosed(temp)) {
temp.g += 1;

fringe.push_front(temp);

}
}
}
}
}
// remove the expanded state from the firinge list.
fringe.remove(cur);
}
// Recursive Solution Path Printing Function.
void PrintPath(State *s)
{
// if the start state not reached.
if (s != NULL) {
//recursively call printing its parent.
PrintPath((*s).parent);
// print current state.
(*s).print();
}
}
// Closed List Searching Function.
bool InClosed(State &s)
{
for (list<State>::iterator it = closed.begin(); it != closed.end(); ++it) {
if ((*it) == s) { //using the State == Operator.
return true;
}
}
return false;
}

