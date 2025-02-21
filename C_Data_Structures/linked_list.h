#ifndef LINKED_LIST_H
#define LINKED_LIST_H

// Define the structure for the linked list node
struct Node {
    int value;
    struct Node* next;
};

// Function prototypes
struct Node* create_node(int value);
void insert_node(struct Node** head, struct Node* new_node);
void print_list(struct Node* head);
void free_list(struct Node** head);

#endif // LINKED_LIST_H