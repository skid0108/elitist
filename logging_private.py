import datetime

class Logging:
    path = str
    append = str

    def __init__(self, path: str, append="a"):
        self.path = path
        self.append = append
    
    def __del__(self):
        #Add something if neccessary
        pass

    def log(self, information):
        try:
            with open(self.path, self.append) as input:
                input.write(f"{datetime.datetime.now()} - {information}\n")
        except Exception as exc:
            print(f"Error accessing logging file: {exc}")

    def logerr(self, func, err):
        try:
            with open(self.path, self.append) as input:
                input.write(f"{datetime.datetime.now()} - Error in {func}: {err}\n")
        except Exception as exc:
            print(f"Error accessing logging file: {exc}")

    def logst(self, func):
        try:
            with open(self.path, self.append) as input:
                input.write(f"{datetime.datetime.now()} - Function {func} initialized\n")
        except Exception as exc:
            print(f"Error accessing logging file: {exc}")

    def logend(self, func):
        try:
            with open(self.path, self.append) as input:
                input.write(f"{datetime.datetime.now()} - Function {func} finished\n")
        except Exception as exc:
            print(f"Error accessing logging file: {exc}")
        