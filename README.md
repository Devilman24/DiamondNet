# 💎 DiamondNet  

**DiamondNet** is a powerful and flexible tool for brute-forcing paths and subdomains. Designed with performance and usability in mind, DiamondNet combines speed, precision, and simplicity to help security professionals and enthusiasts perform web reconnaissance.  

🌟 *For all adventurers with a desire for something new 🎭!*  

---

## ✨ Features  

- 🔍 **Path Bruteforce**: Identify hidden directories on target websites.  
- 🌐 **Subdomain Bruteforce**: Discover subdomains using a wordlist.  
- ⚡ **Multithreading**: Perform fast scans with configurable threads.  
- 🎯 **Custom HTTP Status Code Filtering**: Display only the status codes you care about.  
- 📊 **Progress Tracking**: Real-time updates on scan progress and estimated time remaining.  
- 🔒 **Flexible Protocols**: Supports both HTTP and HTTPS protocols.  

---

## 🛠️ Installation  

Clone the repository to your local machine:  

```bash  
git clone https://github.com/Devilman24/DiamondNet.git  
cd DiamondNet  
````

Install the required dependencies (Python 3.7+ recommended):

```bash
pip install -r requirements.txt  
```

---

## 🚀 Usage

Run DiamondNet with the following syntax:

```bash
python diamondnet.py -u <URL> -w <WORDLIST> -m <MODE> [OPTIONS]  
```

### Arguments

* `-u`, `--url`: Target URL or domain (e.g., `http://example.com` or `example.com`).
* `-w`, `--wordlist`: Path to the wordlist file (e.g., `wordlist.txt`).
* `-m`, `--mode`: Scanning mode:

  * `paths` for directory bruteforcing.
  * `subdomains` for subdomain bruteforcing.

### Options

* `-t`, `--threads`: Number of threads to use (default: `10`).
* `-to`, `--timeout`: Request timeout in seconds (default: `5`).
* `-c`, `--codes`: HTTP status codes to display (comma-separated, e.g., `200,301,403`; default: `200`).
* `-p`, `--protocol`: Protocol to use in subdomain mode (`http` or `https`; default: `https`).

---

## 🧪 Examples

### Directory Bruteforce

```bash
python diamondnet.py -u http://example.com -w directories.txt -m paths -t 20 -c 200,403  
```

### Subdomain Bruteforce

```bash
python diamondnet.py -u example.com -w subdomains.txt -m subdomains -p https  
```

---

## 🌟 Features Overview

1. 📈 **Progress Updates**: Get real-time feedback on scan progress, including average time per request and estimated time remaining.
2. 🚨 **Error Handling**: Gracefully handles network errors and timeouts.
3. ⚙️ **Customizable**: Easily configure threads, timeout, and other parameters to suit your needs.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues, submit pull requests, or suggest features.

1. 🍴 Fork the repository.
2. 🛠️ Create your feature branch: `git checkout -b feature-name`.
3. 💾 Commit your changes: `git commit -m "Add feature description"`.
4. 🔄 Push to the branch: `git push origin feature-name`.
5. 🔗 Open a pull request.

---

## 📜 License

DiamondNet is open-source software licensed under the [ABSTRACTDIAMOND](LICENSE).

---

**Created with ❤️ by [Devilman24](https://github.com/Devilman24)**
💎 **DiamondNet – The sharpest tool for web reconnaissance.**

```
My goal is to turn everything off 🎭!
```
