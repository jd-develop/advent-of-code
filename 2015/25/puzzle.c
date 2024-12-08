// C to gotta go fast
#include <stdio.h>

int main() {
    long long int number = 20151125;
    int row = 1;
    int column = 1;
    int target_row;
    int target_column;
    printf("Enter row and column: ");
    scanf("%d %d", &target_row, &target_column);

    while (row != target_row || column != target_column) {
        row--;
        column++;
        if (row == 0) {
            row = column;
            column = 1;
        }
        number *= 252533;
        number %= 33554393;
    }

    printf("%lld\n", number);

    return 0;
}
