import unittest
from log_analysis import getUserAuthTimes, getInvalidLogins, extractLogFiles, compareInvalidIPs


class log_analysis_test(unittest.TestCase):
    # See if appropriate user login times are being returned.
    def test_getUserAuthTimes(self):
        username = "tmoore"
        getUserAuthTimes(username)
        input = getUserAuthTimes(username)
        output = getUserAuthTimes("tmoore")
        self.assertEqual(input, output)

    # Check if appropriate amount of login attempts are associated with the listed users by picking a random listed user.
    def test_getInvalidLogins(self):
        getInvalidLogins()
        with open("./log/auth.log.all", "r") as f:
            lines = f.readlines()
            denied_users = {}
        for line in lines:
            if "Invalid user" in line:
                user = line.split("Invalid user ")[1].split(" ")[0]
                if user in denied_users:
                    denied_users[user] += 1
                else:
                    denied_users[user] = 1
        input = denied_users.get('zabbix')
        output = 62
        self.assertEqual(input, output)

    # See if combined auth.log file equals the sum of the length of the four auth.log files.
    def test_combinedLogs(self):
        extractLogFiles("auth.log.all")
        with open("./log/auth.log.all", "r") as f:
            lines = f.readlines()
            num_lines = len(lines)
        with open("./log/auth.log.1", "r") as f:
            lines1 = f.readlines()
            num_lines1 = len(lines1)
        with open("./log/auth.log.2", "r") as f:
            lines2 = f.readlines()
            num_lines2 = len(lines2)
        with open("./log/auth.log.3", "r") as f:
            lines3 = f.readlines()
            num_lines3 = len(lines3)
        with open("./log/auth.log.4", "r") as f:
            lines4 = f.readlines()
            num_lines4 = len(lines4)
            auth_log_lengths = [num_lines1, num_lines2, num_lines3, num_lines4]
            input = sum(auth_log_lengths)
            output = num_lines
            self.assertEqual(input, output)

    # Make sure that the ip intersection is returning appropriate amount of mutual ips.
    def test_IPIntersection(self):
        compareInvalidIPs()
        with open("./log/auth.log.all", "r") as f:
            denied_ips = set()
            lines = f.readlines()
            for line in lines:
                if "Invalid" in line:
                    ip = line.split(" from ")[1].split(" ")[0].strip()
                    denied_ips.add(ip)
    # print(denied_ips)
            ip_scan = set()
            with open("./log/ufw.log.all", "r") as f:
                lines = f.readlines()
            for line in lines:
                if "BLOCK" in line:
                    ip = line.split("SRC=")[1].split(" ")[0]
                    ip_scan.add(ip)
    # print(ip_scan)
            mutual_ips = denied_ips.intersection(ip_scan)
            input = len(mutual_ips)
            output = 51
            self.assertEqual(input, output)

    # Verify that ufw.log.all length matches the sum of the four ufw.log files' length.
    def test_ufw_log_all_lengths(self):
        extractLogFiles("ufw.log.all")
        with open("./log/ufw.log.all", "r") as f:
            lines = f.readlines()
            num_lines = len(lines)
        with open("./log/ufw.log.1", "r") as f:
            lines1 = f.readlines()
            num_lines1 = len(lines1)
        with open("./log/ufw.log.2", "r") as f:
            lines2 = f.readlines()
            num_lines2 = len(lines2)
        with open("./log/ufw.log.3", "r") as f:
            lines3 = f.readlines()
            num_lines3 = len(lines3)
        with open("./log/ufw.log.4", "r") as f:
            lines4 = f.readlines()
            num_lines4 = len(lines4)
            ufw_log_lengths = [num_lines1, num_lines2, num_lines3, num_lines4]
            input = sum(ufw_log_lengths)
            output = num_lines
            self.assertEqual(input, output)


if __name__ == '__main__':
    unittest.main()
