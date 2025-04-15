
# SQL Injection Vulnerability in Advaya GEMS ERP Portal v2.1

⚠️ For **educational and authorized security research** only. Unauthorized testing is strictly prohibited.

## 📌 Overview

This repository contains a **Proof of Concept (PoC)** for a **high-severity SQL Injection vulnerability** (Boolean- and Time-Based Blind) in the `userId` parameter of the Advaya GEMS ERP Portal, developed by Advaya Softech.

- **Vulnerability Type**: SQL Injection (Boolean-Based Blind, Time-Based Blind)
- **Severity**: High
- **Affected Endpoint**: `/studentLogin/studentLogin.action`
- **Vulnerable Parameter**: `userId`
- **Target Example**: `https://<target_domain>/studentLogin/studentLogin.action`
- **Discovered By**: Kuppam Johari
- **Reported To Vendor**: October 1, 2024

---

## 🛡️ Ethical Notice

This PoC is provided for educational and authorized penetration testing only. Testing without **explicit permission** is illegal and unethical. Do not use this tool on unauthorized systems.

---

## Vulnerability Details

The `userId` parameter is vulnerable to SQL injection, allowing database query manipulation.

### Techniques Used
- **Boolean-Based Blind**: Evaluate conditions such as `4601=4601`
- **Time-Based Blind**: Use SQL `SLEEP()` to infer query success via delay

### Example Payloads

**Boolean-Based**:
```
userId=testCSC2024' AND 4601=4601-- KCOJ&password=testCSC2024
```

**Time-Based (in script)**:
```
' AND (SELECT 1 FROM (SELECT(SLEEP(0.6-(IF(ORD(MID((<query>)),<pos>,1))=<char_code>,0,0.6)))))a) AND '1'='1
```

---

## 💥 Impact

- **Data Exposure**: Read sensitive data from databases
- **Data Manipulation**: Insert, update, or delete records

---

## 🛠️ Proof of Concept

- [`GEMS_POC.py`](./GEMS_POC.py): Automates time-based SQL injection to extract DB data
- [`ADVAYA-GEMS-Vulnerability-Report.pdf`](./ADVAYA-GEMS-Vulnerability-Report.pdf): Full vulnerability disclosure, PoC, and mitigation guidance

### Script Features

- ✅ Multi-threaded Enumeration (6 threads)
- ✅ Character Confirmation (double-checks each character)
- ✅ Interactive Menu
- ✅ Customizable delays, charsets, thresholds

---

## 🚀 Usage

### Requirements

- Python 3.x
- Dependencies:
```bash
pip install requests
```

### Run the PoC

```bash
git clone https://github.com/kuppamjohari/advaya-gems-sql-injection-poc.git
cd advaya-gems-sql-injection-poc
python GEMS_POC.py
```

### Menu Options

- Change target domain (default: `https://pesgems.in/`)
- Extract current DB name
- List all DBs
- Enumerate tables in a DB
- Exit

---

## ⚠️ Additional Vulnerabilities Referenced

- CVE-2015-9251 – Directory traversal
- CVE-2020-11022 – XSS
- CVE-2020-7656 – DoS (websocket)
- CVE-2020-11023 – API access bypass
- CVE-2019-11358 – DoS (APC)
- CVE-2012-6708 – Code injection (JSON)

---

## References

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- Watch the PoC video: [SQL Injection Vulnerability in Advaya GEMS ERP Portal](https://www.youtube.com/watch?v=bs6WT-zCAmo)
  [![Video Thumbnail](https://img.youtube.com/vi/bs6WT-zCAmo/0.jpg)](https://www.youtube.com/watch?v=bs6WT-zCAmo)
---

## CVE Status

- Not yet assigned
- Submitted to:
  - Advaya Softech (Disclosure Contact Pending)
  - CVE assignment (Pending)

---

## 📝 Disclaimer

This project is for **authorized security testing and research** only. The author and contributors are not responsible for misuse or unauthorized access. Always obtain written permission before testing.
