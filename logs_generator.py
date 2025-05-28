import requests
import time
import random
from icmplib import ping
import threading
import dns.resolver
from dns.reversename import from_address

class Logs:
    
    def _generate_logs(self):
        pass

    def run(self):
        """Method to start generating logs"""
        self._generate_logs()


class HTTP_logs(Logs):
    """Class to generate HTTP data"""
    def __init__(self, get_resources=0, post_resources=0, time_sleep=0.5, number_logs = 20):
        if get_resources != 0:
            self.GET_resources = get_resources
        else:
            self.GET_resources = ["https://httpbin.org/get","https://picsum.photos/200/300", "https://jsonplaceholder.typicode.com/posts", "https://postman-echo.com/get", "https://8.8.8.8" ]
        
        if post_resources != 0:
            self.POST_resources = post_resources
        else:
            self.POST_resources = ["https://httpbin.org/post", "https://jsonplaceholder.typicode.com/posts"]
        self.time_sleep = time_sleep
        self.number_logs = number_logs

    def _generate_logs(self):
        """Function to generate request with random resources"""

        choice_pair = ['GET', 'POST']
        for i in range(self.number_logs):
            choice = random.choice(choice_pair)
            if choice == "GET":
                url = random.choice(self.GET_resources)
                gen = requests.get(url)
            else:
                url = random.choice(self.POST_resources)
                gen = requests.post(url)
            print(f"[HTTP][{choice}] {url} → {gen.status_code}")
            time.sleep(self.time_sleep)


class ICMP_logs(Logs):
    """Class to generate ICMP data"""
    def __init__(self, resources=0, number_logs = 20):

        if resources != 0:
            self.PING_resources = resources
        else:
            self.PING_resources = ["8.8.8.8", "1.0.0.1", "8.8.4.4", "cloudflare-dns.com", "google.com"]
        self.number_logs = number_logs

    def _generate_logs(self):
        """Function to generate logs with  resources"""

        for i in range(self.number_logs):
            random_res = random.choice(self.PING_resources)
            host = ping(random_res,privileged=False)
            print(f"ICMP data to {random_res} : Sent:{host.packets_sent} Received : {host.packets_received} Loss : {host.packet_loss}")



class DNS_logs(Logs):
    """Class to generate DNS logs"""
    def __init__(self, domain_resources = None, ip_resources = None, number_logs = 20, time_sleep = 0.5):
        self.number_logs = number_logs
        self.time_sleep = time_sleep
        if domain_resources:
            self.domain_res = domain_resources
        else:
            self.domain_res = ["cloudflare-dns.com", "google.com","facebook.com"]
        
        if ip_resources:
            self.ip_res = ip_resources
        else : 
            self.ip_res = ["8.8.8.8", "1.0.0.1", "8.8.4.4"]
    def _generate_logs(self):
        """Function to generate DNS logs with resources"""

        for i in range(self.number_logs):
            log_type = random.choice(["IP", "DNS"])
            try:
                if log_type == "IP":
                    ip = random.choice(self.ip_res)
                    rev = from_address(ip)
                    answer = dns.resolver.resolve(rev, "PTR")
                    print(f"[DNS][PTR] {ip} → {answer[0]}")
                else:
                    domain = random.choice(self.domain_res)
                    answers = dns.resolver.resolve(domain, "A")
                    for rdata in answers:
                        print(f"[DNS][A] {domain} → {rdata.address}")
            except dns.resolver.NoAnswer:
                print(f"[DNS][{log_type}] NoAnswer for resource")
            except dns.resolver.NXDOMAIN:
                print(f"[DNS][{log_type}] NXDOMAIN (domain does not exist)")
            except dns.resolver.Timeout:
                print(f"[DNS][{log_type}] Timeout occurred")
            except dns.resolver.NoNameservers:
                print(f"[DNS][{log_type}] NoNameservers available")
            except Exception as e:
                print(f"[DNS][{log_type}] Unexpected error: {e}")
            
            time.sleep(self.time_sleep)



if __name__ == "__main__":
    
    http = HTTP_logs()
    icmp = ICMP_logs()
    dns1 = DNS_logs()
    t1 = threading.Thread(target=http.run)
    t2 = threading.Thread(target=icmp.run)
    t3 = threading.Thread(target=dns1.run)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()