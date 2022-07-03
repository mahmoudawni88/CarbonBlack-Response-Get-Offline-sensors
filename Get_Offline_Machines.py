import sys
import requests
import urllib3
import csv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}  # used to debug using BurpSuite
# function for getting all (active & inactive) sesnors for a specific group
def get_sensor_list(hostname,port,group_id,number_of_inactive,apikey):
    url = 'https://{0}:{1}/api/v1/sensor?inactive_filter_days={2}&groupid={3}'.format(hostname, port,number_of_inactive, group_id)
    header = {'X-Auth-Token': apikey}
    sensor_list = requests.get(url=url, headers=header, verify=False)
    if sensor_list.status_code != 200:
        print(f'[-] not able to connect to CB. the status code is {str(sensor_list.status_code)} Please check the connectitvity')
        sys.exit(-1)
    else:
        return sensor_list.json()  # the output is list of dictionary [computer_name,status]


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('[-] Usage: {0} <hostname> <port> <group_id> <number_of_inactive> <apikey>'.format(sys.argv[0]))
        print('[-] Example: {0} x.x.x.x xxxx x xx xxxxxxxxxxxxxxxxxxxxxxxxxxxx'.format(sys.argv[0]))
        sys.exit(-1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    group_id = int(sys.argv[3])
    number_of_inactive = int(sys.argv[4])
    apikey = sys.argv[5]
    print('[+] getting the list of sensors')
    sensors = get_sensor_list(hostname, port, group_id, number_of_inactive, apikey)  # the output of list of dictionary
    if len(sensors) != 0:
        print('[+] Checking if there is an offline senors or not')
        with open('offline_sensor.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['computer_name', 'status', 'os_environment_display_string', 'last_update'])
            for endpoint in sensors:
                if endpoint['status'] == 'Offline':
                    writer.writerow([endpoint['computer_name'],endpoint['os_environment_display_string'],endpoint['status'],endpoint['last_update']])
    else:
        print('[+] All the servers are online :)')