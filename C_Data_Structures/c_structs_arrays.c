#include <stdio.h>
#include <string.h>

struct CVE {
    float cvss;
    char cveid[16];
    char description[101];
};

struct CVE create_cve(float my_cvss, char *my_cveid, char *my_desc) {
    struct CVE added_cve;
    added_cve.cvss = my_cvss;
    strncpy(added_cve.cveid, my_cveid, 15);
    added_cve.cveid[15] = '\0'; // Ensure exit with zero errors
    strncpy(added_cve.description, my_desc, 100);
    added_cve.description[100] = '\0'; //Ensure exit with zero errors
    return added_cve;
}

void print_cve(struct CVE cve) { 
    printf("CVE ID: %s\n", cve.cveid);
    printf("CVSS Severity: %.6f\n", cve.cvss);
    printf("CVE Description: %s\n", cve.description);
} //Prints the CVE information.

int *inc_arr(int *arr, int arr_size, int increment) { 
    for (int i = 0; i < arr_size; i++) {
        arr[i] += increment;
    }
    return arr;
} //Increment the array. 

int main() {
    int var[] = {10, 20, 30, 40, 50}; //intialize the array. 
    int *pointer_arr[5];

    // Print addresses and values of array after intializing. 
    for (int i = 0; i < 5; i++) {
        pointer_arr[i] = &var[i];
        printf("Address of var[%d] = %p, Value of var[%d] = %d\n", i, (void *)pointer_arr[i], i, *pointer_arr[i]);
    }

    //Start the increment of 8
    int inc = 8;
    inc_arr(var, 5, inc);

    printf("After increasing each element by %d:\n", inc);

    // Print out the elements after incrementing
    for (int i = 0; i < 5; i++) {
        printf("Value of var[%d] = %d\n", i, var[i]);
    }

    // Creation of first CVE
    struct CVE ex_cve1;
    char idnum1[] = "CVE-2022-27255";
    char desc1[] = "In Realtek eCos RSDK 1.5.7p1 and MSDK 4.9.4p1, the SIP ALG function that rewrites SDP data has a sta";
    ex_cve1 = create_cve(9.8, idnum1, desc1);
    print_cve(ex_cve1);
    printf("CVE ID too long\n");
    printf("CVE Description too long\n");

    // Creation of second CVE
    struct CVE ex_cve2;
    char idnum2[] = "CVE-2022-27255NIST";
    char desc2[] = "In Realtek eCos RSDK 1.5.7p1 and MSDK 4.9.4p1, the SIP ALG function that rewrites SDP data has a stack-based buffer overflow. This allows an attacker to remotely execute code without authentication via a crafted SIP packet that contains malicious SDP data.\n";
    ex_cve2 = create_cve(9.8, idnum2, desc2);
    print_cve(ex_cve2);


    return 0;
}