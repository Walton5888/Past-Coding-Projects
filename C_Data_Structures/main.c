#include <stdio.h>
#include "linked_list.h"

int main() {
    // Create a new node
    struct Node* node = create_node(5);
    if (node == NULL) {
        printf("Failed to create node.\n");
        return -1;
    }

    // Create a head for the linked list
    struct Node* head = NULL;

    // Insert the new node into the linked list
    insert_node(&head, node);

    // Print the linked list
    printf("Linked list: ");
    print_list(head);

    // Free the linked list
    free_list(&head);

    return 0;
}