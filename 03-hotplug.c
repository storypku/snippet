#include <linux/netlink.h>
#include <sys/socket.h>
#include <sys/poll.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
    struct sockaddr_nl nls;
    struct pollfd pfd;
    char buf[512];

    // Open hotplug event netlink socket

    memset(&nls, 0, sizeof(struct sockaddr_nl));

    nls.nl_family = AF_NETLINK;
    nls.nl_pid = getpid();
    nls.nl_groups = -1;

    pfd.events = POLLIN;
    pfd.fd = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_KOBJECT_UEVENT);

    if (pfd.fd == -1)
        perror("Not ROOT\n");

    // Listen to netlink socket
    if (bind(pfd.fd, (void *)&nls, sizeof(struct sockaddr_nl)) == -1)
        perror("Bind failed\n");

    while(-1 != poll(&pfd, 1, -1)) {
        int len = recv(pfd.fd, buf, sizeof(buf), MSG_DONTWAIT);
        if (len == -1)
            perror("recv\n");
        // Print the data to stdout
        int i = 0;
        while(i < len) {
            printf("== %s ==\n", buf + i);
            i += strlen(buf + i) + 1;
        }
    }
    
    perror("poll\n");
    return 0;
}
