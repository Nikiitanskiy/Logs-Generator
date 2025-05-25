import requests
import time
import random
from icmplib import ping
import threading


class Logs:
    
    def __generate_logs(self):
        pass

    def run(self):
        """Method to start generating logs"""
        self.generate_logs()


class HTTP_logs(Logs):
    """Class to generate HTTP data"""
    def __init__(self):
        pass


    def __generate_logs(self):
        """Function to generate request with random resources"""
        GET_resources = ["https://httpbin.org/get","https://picsum.photos/200/300", "https://jsonplaceholder.typicode.com/posts", "https://postman-echo.com/get", "https://8.8.8.8" ]
        POST_resources = ["https://httpbin.org/post", "https://jsonplaceholder.typicode.com/posts"]
        choice_pair = ['GET', 'POST']
        while True:
            choice = random.choice(choice_pair)
            if choice == "GET":
                gen = requests.get(random.choice(GET_resources))
            else:
                gen = requests.post(random.choice(POST_resources))
            print(gen.status_code)
            time.sleep(0.2)


class ICMP_logs(Logs):
    """Class to generate ICMP data"""
    def __init__(self):
        pass

    def __generate_logs(self):
        """Function to generate request with random resources"""

        PING_resources = ["8.8.8.8", "1.0.0.1", "8.8.4.4", "cloudflare-dns.com", "google.com"]
        
        while True:
            random_res = random.choice(PING_resources)
            host = ping(random_res,privileged=False)
            print(f"ICMP data to {random_res} : Sent:{host.packets_sent} Received : {host.packets_received} Loss : {host.packet_loss}")


# if __name__ == "__main__":
    
#     http = HTTP_logs()
#     icmp = ICMP_logs()
#     t1 = threading.Thread(target=http.run)
#     t2 = threading.Thread(target=icmp.run)

#     t1.start()
#     t2.start()

#     t1.join()
#     t2.join()