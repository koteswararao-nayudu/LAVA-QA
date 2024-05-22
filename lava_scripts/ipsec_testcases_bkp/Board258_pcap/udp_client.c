
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <assert.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/time.h>
#include <sys/select.h>
#include <math.h>

#define PORT 2152

char* dummy_hex_dump;

int main() {
   int sockfd;
   struct sockaddr_in     servaddr;
   char buffer[]={0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
	 ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed ,0xde ,0xad ,0xfe ,0xed 
         ,0x00 ,0x00 ,0x17 ,0x89 ,0x00 ,0x00 ,0x00 ,0x00 ,0xde, 0xad, 0xfe, 0xed, 0xde, 0xad, 0xfe, 0xed
         ,0x00 ,0x00 ,0x00 ,0x01 ,0x00 ,0x00 ,0x23 ,0x28 ,0x00 ,0x00 ,0x04 ,0x7e ,0x44 ,0x8b ,0x9b ,0x80
         ,0xff ,0xf0 ,0xbe ,0x24 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
         ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31
         ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37
         ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33
         ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39
         ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35 ,0x36 ,0x37 ,0x38 ,0x39 ,0x30 ,0x31 ,0x32 ,0x33 ,0x34 ,0x35
   };


   //create socket
   if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
      perror("socket creation failed");
      exit(EXIT_FAILURE);
   }

   memset(&servaddr, 0, sizeof(servaddr));

   servaddr.sin_family = AF_INET;
   servaddr.sin_port = htons(PORT);
   servaddr.sin_addr.s_addr = inet_addr("192.168.251.12"); //host ip address
   if ( bind(sockfd, (const struct sockaddr *)&servaddr,
            sizeof(servaddr)) < 0 )
   {
      perror("bind failed");
      exit(EXIT_FAILURE);
   }

   servaddr.sin_addr.s_addr = inet_addr("192.168.251.58"); //destination address

   uint64_t packet_size;

   printf("enter packet size in bytes:\n");
   scanf("%lu",&packet_size);

   while(packet_size<100)
   {
      printf("Warning:increase packet size\nEnter packet size in bytes:\n");
      scanf("%lu",&packet_size);
   }

  uint64_t cnt = 1;
   printf("no. of times, packets are sent to dest. in a second= %lu\n",cnt);


   char sendc[packet_size];
   for(int i=0;i<packet_size;i++)
      sendc[i]=buffer[i];


   dummy_hex_dump=(char *)malloc(sizeof(sendc));
   memcpy(dummy_hex_dump,sendc,sizeof(sendc));

   printf("size of a packet sent: %lu\n",sizeof(sendc));

   uint64_t i, j = 1;

   struct timeval start, stop;
   double secs = 0;

   uint64_t one_sec_boundary_time_stamp_us;
   uint64_t current_time_us;
   uint32_t data_rate;

   while(j > 0)
   {
      i = 0;
      data_rate = 0;

      gettimeofday(&start, NULL);

      printf("Next iteration : %ld\n", j);

      while (i < cnt)
      {
         sendto (sockfd, (const char *)dummy_hex_dump, (packet_size),
               MSG_CONFIRM, (const struct sockaddr *) &servaddr,
               sizeof(servaddr));
         i++;
      }

      gettimeofday(&stop, NULL);

	j--;
   }
   close(sockfd);
   return 0;
}
