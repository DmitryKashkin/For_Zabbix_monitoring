def main():
    with open('c:\ProgramData\Acronis\log\log.temp', 'r') as f:
        with open('c:\ProgramData\Acronis\log\log.log', 'r') as ff:
            log_list = ff.readlines()
        with open('c:\ProgramData\Acronis\log\log.log', 'a') as ff:
            for string in f:
                if string in log_list:
                    continue
                ff.write(string)


if __name__ == '__main__':
    main()
