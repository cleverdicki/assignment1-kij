#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SIZE 1024
#define PORT 8080

int main(int argc, char const *argv[]) {
    struct sockaddr_in server_addr;
    struct sockaddr_in address;
    int sock = 0, valread;
    char buffer[SIZE] = {0};
    char *filename = "testing.txt";
    FILE *fp;

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return -1;
    }

    memset(&server_addr, '0', sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);

    if (inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        printf("\nConnection Failed \n");
        return -1;
    }

    fp = fopen(filename, "r");
    if (fp == NULL) {
        printf("File error!");
        return -1;
    }

    while (fgets(buffer, SIZE, fp) != NULL) {
        if (send(sock, buffer, sizeof(buffer), 0) == -1) {
            perror("\nError while sending file!");
            return -1;
        }
        bzero(buffer, SIZE);
    }

    printf("File data has been sent\n");
    close(sock);
}