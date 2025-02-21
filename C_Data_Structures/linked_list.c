#include "linked_list.h"
#include <stdlib.h>
#include <stdio.h>

struct Node* create_node(int value) {
    // Function to create a new node
    // TODO: Implement this function
    struct Node* new_node = (struct Node*)malloc(sizeof(struct Node*));
    if(new_node != NULL) {
        new_node->value=value; // Assign a value to the node. 
        new_node->next=NULL;
    }
    return new_node; // finish the creation of the node. 
}

void insert_node(struct Node** head, struct Node* new_node) {
    // Function to insert a new node at the end of the linked list
    // TODO: Implement this function
    if (*head == NULL) {
        *head=new_node; //establish the creation of a new node. 
    } else {
        struct Node* present_node = *head; //establish the head as the starting position. 
        while (present_node->next != NULL) {
            present_node=present_node->next; //ensure nodes are added.
        }
        present_node->next=new_node; //point the current node to the new node. 
    }
}

void print_list(struct Node* head) {
    // Function to print all the values in the linked list
    // TODO: Implement this function
    struct Node* present_node = head;
    while(present_node!=NULL) {
        printf("%d ", present_node->value); //format how the values will be returned in the print statement. 
        present_node=present_node->next;
    }
    printf("\n");
}

void free_list(struct Node** head) {
    // Function to free all the memory allocated for the linked list
    // TODO: Implement this function
    struct Node* present_node=*head;
    while(present_node!=NULL) {
        struct Node* plc_hldr = present_node; //establish the location of the memory that will be freed. 
        present_node = present_node->next;
        free(plc_hldr); //free the memory. 
    }
    *head = NULL;



}